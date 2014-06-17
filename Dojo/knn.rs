
extern crate time;

use std::io::{File, BufferedReader};


struct LabelPixel {
    label: int,
    pixels: Vec<int>
}


fn slurp_file(file: &Path) -> Vec<LabelPixel> {
    BufferedReader::new(File::open(file).unwrap())
        .lines()
        .skip(1)
        .map(|line| {
            let line = line.unwrap();
            let mut iter = line.as_slice().trim()
                .split(',')
                .map(|x| from_str(x).unwrap());

            LabelPixel {
                label: iter.next().unwrap(),
                pixels: iter.collect()
            }
        })
        .collect()
}

fn distance_sqr(x: &[int], y: &[int]) -> int {
    // run through the two vectors, summing up the squares of the differences
    x.iter()
        .zip(y.iter())
        .fold(0, |s, (&a, &b)| s + (a - b) * (a - b))
}

fn classify(training: &[LabelPixel], pixels: &[int]) -> int {
    training
        .iter()
        // find element of `training` with the smallest distance_sqr to `pixel`
        .min_by(|p| distance_sqr(p.pixels.as_slice(), pixels)).unwrap()
        .label
}

/*
fn main() {
    let training_set = slurp_file(&Path::new("trainingsample.csv"));
    let validation_sample = slurp_file(&Path::new("validationsample.csv"));

    let t = time::precise_time_s();

    let num_correct = validation_sample.iter()
        .filter(|x| {
            classify(training_set.as_slice(), x.pixels.as_slice()) == x.label
        })
        .count();

    println!("Percentage correct: {}% Took: {}",
             num_correct as f64 / validation_sample.len() as f64 * 100.0, time::precise_time_s() - t);
}
*/

// how many chunks should the validation sample be divided into? (==
// how many futures to create.)
static NUM_CHUNKS: uint = 32;

fn main() {
    use std::sync::Arc;
    use std::sync::Future;
    use std::cmp;

    // "atomic reference counted": guaranteed thread-safe shared
    // memory. The type signature and API of `Arc` guarantees that
    // concurrent access to the contents will be safe, due to the `Share`
    // trait.
    let training_set = Arc::new(slurp_file(&Path::new("trainingsample.csv")));
    let validation_sample = Arc::new(slurp_file(&Path::new("validationsample.csv")));

    let chunk_size = (validation_sample.len() + NUM_CHUNKS - 1) / NUM_CHUNKS;

    let t = time::precise_time_s();

    let mut futures = range(0, NUM_CHUNKS).map(|i| {
        // create new "copies" (just incrementing the reference
        // counts) for our new future to handle.
        let ts = training_set.clone();
        let vs = validation_sample.clone();

        Future::spawn(proc() {
            // compute the region of the vector we are handling...
            let lo = i * chunk_size;
            let hi = cmp::min(lo + chunk_size, vs.len());

            // ... and then handle that region.
            vs.slice(lo, hi)
                .iter()
                .filter(|x| {
                    classify(ts.as_slice(), x.pixels.as_slice()) == x.label
                })
                .count()
        })
    }).collect::<Vec<Future<uint>>>();

    // run through the futures (waiting for each to complete) and sum the results
    let num_correct = futures.mut_iter().map(|f| f.get()).fold(0, |a, b| a + b);

    println!("Percentage correct: {}% Took: {}",
             num_correct as f64 / validation_sample.len() as f64 * 100.0, time::precise_time_s() - t);
}
