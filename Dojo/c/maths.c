#include "maths.h"
#include <sys/time.h>
#include <stdlib.h>

int distance_sqr(Data valid, int vrow, Data sample, int srow) {
  int result = 0;
  for (int c=1; c<valid.num_cols; c++) {
    int x = Data_get(valid, vrow, c);
    int y = Data_get(sample, srow, c);
    result += ((x-y) * (x-y));
  }
  return result;
}

int find_match(Data valid, Data sample, int srow) {
  int best_valid_label = 0;
  int min = 9999999;
  for (int vrow=0; vrow<valid.num_rows; vrow++) {
    int dist = distance_sqr(valid, vrow, sample, srow);
    if (dist < min) {
      best_valid_label = Data_get(valid, vrow, 0);
      min = dist;
    }
  }
  return best_valid_label;
}

double compute(Data valid, Data sample) {
  int matches = 0;
  for (int srow=0; srow<sample.num_rows; srow++) {
     int vlabel = find_match(valid, sample, srow);
     int slabel = Data_get(sample, srow, 0);
     if (vlabel == slabel) {
       matches++;
     }
  }
  double percent = ((double)matches / (double)valid.num_rows) * 100;
  return percent;
}

long now() {
  struct timeval time;
  gettimeofday(&time, NULL);
  return (time.tv_sec * 1000) + (time.tv_usec / 1000);
}

double millis2seconds(long millis) {
	return (double)millis / 1000;
}
