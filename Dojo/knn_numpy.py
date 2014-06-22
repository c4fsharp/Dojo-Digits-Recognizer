# http://codepad.org/ExjayzZe

import time
import numpy as np
#from multiprocessing import Pool


def read_file(filename):
	with open(filename,'r') as v:
		v.readline()
		values = []
		for line in v:
			xs = [int(x) for x in line.split(',')]
			label = xs[0]
			xs = np.array(xs[1:],dtype=np.int32)
			values += [(label,xs)]
	return values

def make_sqs(sample):
	for i in range(len(sample)):
		label,xs = sample[i]
		sample[i] = (label,xs,np.sum(xs*xs))



validation_sample = read_file('validationsample.csv')
testing_sample = read_file('trainingsample.csv')

start_time = time.time()


num_correct = 0

make_sqs(validation_sample)
make_sqs(testing_sample)


vmat = np.zeros((len(validation_sample),len(validation_sample[0][1])))
tmat = np.zeros((len(testing_sample[0][1]),len(testing_sample)))

for i,(_,xs,_) in enumerate(validation_sample):
	vmat[i,:] = xs

for i,(_,ys,_) in enumerate(testing_sample):
	tmat[:,i] = ys

abmat = -2*np.dot(vmat,tmat)
for i,(x_label,xs,xsq) in enumerate(validation_sample):
	abmat[i,:] += xsq
for j,(y_label,ys,ysq) in enumerate(testing_sample):
	abmat[:,j] += ysq

for i,(x_label,xs,xsq) in enumerate(validation_sample):
	#sums = [0] * len(testing_sample)
	#for i,(y_label,ys,ysq) in enumerate(testing_sample):
	#	s = 0
	#	for x,y in zip(xs,ys):
	#		s += (x-y)*(x-y)
	#	sums[i] = s
	#print(sums)

	sums = abmat[i,:]

	minimum_sum = None
	minimum_label = None
	for s,(y_label,_,_) in zip(sums,testing_sample):
		if minimum_sum is None or s < minimum_sum:
			minimum_sum = s
			minimum_label = y_label
	if minimum_label == x_label:
		num_correct += 1

print(num_correct * 100.0 / len(validation_sample))

elapsed = time.time() - start_time
print("elapsed time: {}".format(elapsed))
