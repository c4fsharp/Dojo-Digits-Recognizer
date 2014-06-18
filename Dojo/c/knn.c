#include <stdio.h>
#include "opts.h"
#include "data.h"
#include "maths.h"

int main(int argc, char *argv[]) {
  Options opts;
  Data train_data;
  Data valid_data;

  Options_set(&opts, argc, argv);
  Options_show(opts);

  Data_read_file(&train_data, opts.training_samples);

  Data_read_file(&valid_data, opts.validation_samples);

  compute(valid_data, train_data);

  return 0;
}
