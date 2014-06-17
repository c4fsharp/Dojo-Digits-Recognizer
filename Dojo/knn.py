import csv
import argparse
import datetime
import sys

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default='trainingsample.csv', help='train sample csv [%(default)s]')
    parser.add_argument('--validation', default='validationsample.csv', help='validation csv [%(default)s]')
    args = parser.parse_args()

    train_samples = load_data(args.train)
    validation_samples = load_data(args.validation)

    t = datetime.datetime.now()
    match_count = 0
    for train_data in train_samples:
        answer = find_match(train_data['pixels'], validation_samples)
        if train_data['label'] == answer['label']:
            match_count += 1
    
    print('%s%% Took: %s' % (float(match_count)/len(validation_samples)*100, datetime.datetime.now() - t))
