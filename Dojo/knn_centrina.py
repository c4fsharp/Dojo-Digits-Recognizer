# http://codepad.org/d15cDg7B

import datetime
import multiprocessing

def read_file(filename):
    with open(filename,'r') as v:
        v.readline()
        values = []
        for line in v:
            xs = [int(x) for x in line.split(',')]
            label = xs[0]
            xs = xs[1:]
            values += [(label,xs)]
    return values

def is_good(tupl):
    x_label,xs = tupl
    minimum_sum = None
    minimum_label = None
    for y_label,ys in train_sample:
        s = 0
        for x,y in zip(xs,ys):
            t = x-y
            s += t*t
        if minimum_sum is None or s < minimum_sum:
            minimum_sum = s
            minimum_label = y_label
    if minimum_label == x_label:
        return 1
    return 0



if __name__ == '__main__':

    validation_sample = read_file('validationsample.csv')
    train_sample = read_file('trainingsample.csv')

    worker_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=worker_count)

    start_time = datetime.datetime.now()

    num_correct = sum(pool.map(is_good, validation_sample))

    print(num_correct * 100.0 / len(validation_sample))
    print('Took: %s' % (datetime.datetime.now() - start_time))
