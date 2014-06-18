
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

