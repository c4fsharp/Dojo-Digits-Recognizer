#ifndef MATH_H
#define MATH_H

#include "data.h"

int distance_sqr(Data valid, int vrow, Data sample, int srow);
double compute(Data valid, Data sample);

long now();
double millis2seconds(long millis);

#endif
