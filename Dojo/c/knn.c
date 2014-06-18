#include <stdio.h>
#include "opts.h"
#include "data.h"
#include "maths.h"


int main(int argc, char *argv[]) {
  Options opts;
  Data train_data;
  Data valid_data;
  double percent;

  Options_set(&opts, argc, argv);
  Options_show(opts);

  Data_read_file(&train_data, opts.training_samples);
  Data_read_file(&valid_data, opts.validation_samples);


  long start = now();
  percent = compute(valid_data, train_data);
  long end = now();


  printf("%4.2f%% Took %4.2f s\n", percent, millis2seconds(end-start));

  return 0;
}
