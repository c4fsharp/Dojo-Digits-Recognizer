import csv
import argparse
import datetime
import sys
import multiprocessing

def distance_sqr(xs, ys):
    result = 0
    for x,y in zip(xs, ys):
        result += ((x - y) ** 2)
    return result

def Data(row):
    return {'label': int(row[0], 10), 'pixels': list(map(int, row[1:]))}

def load_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader) #skip header
        return [Data(row) for row in reader]

def find_match(valid_pixels, train_samples):
    min_distance = sys.maxsize
    result = None

    for sample in train_samples:
        if min_distance > distance_sqr(valid_pixels, sample['pixels']):
            result = sample

    return result

class FindMatch(object):
    def __init__(self, validation_samples):
        self.validation_samples = validation_samples

    def __call__(self, data):
        answer = find_match(data['pixels'], self.validation_samples)
        if data['label'] == answer['label']:
            return 1
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default='trainingsample.csv', help='train sample csv [%(default)s]')
    parser.add_argument('--validation', default='validationsample.csv', help='validation csv [%(default)s]')
    parser.add_argument('--concurrent', type=int, default=1, help='number of parallel processes [%(default)s]')
    args = parser.parse_args()

    train_samples = load_data(args.train)
    validation_samples = load_data(args.validation)

    buff = []
    sample_count = len(train_samples)
    split_count = sample_count / args.concurrent
    worker = FindMatch(validation_samples)
    pool = multiprocessing.Pool(processes=args.concurrent)

    t = datetime.datetime.now()
    match_count = 0

    for i,train_data in enumerate(train_samples, 1):
        buff.append(train_data)
        if i % split_count == 0:
            match_count += sum(pool.map(worker, buff))
            buff = []
    
    if len(buff) > 0:
        match_count += sum(pool.map(worker, buff))
    
    print('%s%% Took: %s' % (float(match_count)/len(validation_samples)*100, datetime.datetime.now() - t))
