# About

Originally from: http://huonw.github.io/2014/06/10/knn-rust.html

There are two csv files:

* trainingsample.csv
* validationsample.csv

Format is:

* First row is header.
* Given a data row (not header),
    * First column is number that the image is representing.
    * The rest of columns are pixels of the image.

For each image (row) in `trainingsample.csv`, find the best matching image in `validationsample.csv`.
And compare the number (first column).

For example, 5th image of `trainingsample.csv` is 0. And if you found the best matching image from `validationsample.csv`, 
it should be 0.

Correct answer should be `94.4%`. There are 500 images in `validationsample.csv`. 472 of them are _correctly_ matched against 5000 images in `trainingsample.csv`.

# pseudo code

    validationsample.csv = parsed from file
    trainingsample.csv = parsed from file

    t = now()
    good_match_count = 0
    for unknown in validationsample.csv:
        match = null
        min_distance = MAX_DISTANCE
        for known in trainingsample.csv:
            d = distance(unknown, known)
            if d < min_distance:
                min_distance = d
                match = known
        if match.label == unknown.label:
            good_match_count++

    print(good_match_count/validationsample.csv.length)
    print(now() - t)


    function distance(pixels1, pixels2):
        result = 0
        for i in 0 to pixels1.length:
            d = pixels1[i]-pixels2[i]
            result += d*d
        return result


# python

    $ python knn.py
    count: 500 match: 472
    94.4% Took: 0:00:48.740370
    python knn.py  271.71s user 0.90s system 540% cpu 50.430 total
    
# rust

    $ rustc -O knn.rs
    $ ./knn
    Percentage correct: 94.4% Took: 0.754412
    ./knn  4.48s user 0.06s system 486% cpu 0.934 total
    
# c

    $ cd c
    $ ./knn -t ../trainingsample.csv -v ../validationsample.csv -n 6
    Training Samples ../trainingsample.csv
    Validation Samples ../validationsample.csv
    Number of CPUs 6
    846.00% Took 6.71 s
    ./knn -t ../trainingsample.csv -v ../validationsample.csv -n 6  6.90s user 0.01s system 99% cpu 6.924 total

# go

    $ go build -o knn knn_hfaafb.go
    $ ./knn
    94.000000Duration: 4.147326635./knn  4.11s user 0.05s system 100% cpu 4.159 total
    
