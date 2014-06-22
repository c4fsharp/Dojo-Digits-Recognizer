import csv
import argparse
import datetime
import sys
import multiprocessing

def Data(row):
    return {'label': int(row[0], 10), 'pixels': list(map(int, row[1:]))}

def load_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader) #skip header
        return [Data(row) for row in reader]

class FindMatch(object):
    def __init__(self, train_samples):
        self.train_samples = train_samples

    def __call__(self, data):
        pixels = data['pixels']
        min_distance = sys.maxsize
        match = None
        for sample in self.train_samples:
            distance = sum((x-y)*(x-y) for x,y in zip(pixels, sample['pixels']))
            if distance < min_distance:
                min_distance = distance
                match = sample
        
        if data['label'] == match['label']:
            return 1
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default='trainingsample.csv', help='train sample csv [%(default)s]')
    parser.add_argument('--validation', default='validationsample.csv', help='validation csv [%(default)s]')
    parser.add_argument('--concurrent', type=int, default=multiprocessing.cpu_count(), help='number of parallel processes [%(default)s]')
    args = parser.parse_args()

    train_samples = load_data(args.train)
    validation_samples = load_data(args.validation)

    find_match = FindMatch(train_samples)
    pool = multiprocessing.Pool(processes=args.concurrent)

    t = datetime.datetime.now()
    
    match_count = sum(pool.map(find_match, validation_samples))
    
    print('count: %s match: %s' % (len(validation_samples), match_count))
    print('%s%% Took: %s' % (float(match_count)/len(validation_samples)*100, datetime.datetime.now() - t))
