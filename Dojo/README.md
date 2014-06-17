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


# python

    $ python knn.py --concurrent 6
    95.4% Took: 0:00:37.439134
    python knn.py --concurrent 6  211.48s user 0.62s system 542% cpu 39.108 total
    
# rust

    $ rustc -O knn.rs
    $ ./knn
    Percentage correct: 94.4% Took: 0.754412
    ./knn  4.48s user 0.06s system 486% cpu 0.934 total
    
