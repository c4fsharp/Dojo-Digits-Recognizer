all: clean build
	./knn -t ../trainingsample.csv -v ../validationsample.csv -n 1
	#./knn -t ../tiny.csv -v ../tiny.csv -n 1

debug:
	gcc -o knn -O0 -g -std=gnu99 -Wall -Werror --pedantic  knn.c opts.c data.c maths.c
	gdb ./knn

build:
	gcc -o knn -O2 -std=gnu99 -Wall -Werror --pedantic  knn.c opts.c data.c maths.c

clean:
	rm -rf knn
