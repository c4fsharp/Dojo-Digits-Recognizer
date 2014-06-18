#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include "opts.h"

void Options_show(Options opts) {
  printf("Training Samples %s\n", opts.training_samples);
  printf("Validation Samples %s\n", opts.validation_samples);
  printf("Number of CPUs %d\n", opts.num_cpus);
}

void Options_set(Options *opts, int argc, char *argv[]) {
  int c;

  memset(opts, 0, sizeof(*opts));

  while ((c = getopt(argc, argv, "t:v:n:")) != -1) {
    switch (c) {
    case 't':
      opts->training_samples = optarg;
      break;
    case 'v':
      opts->validation_samples = optarg;
      break;
    case 'n':
      opts->num_cpus = atoi(optarg);
      break;
    case '?':
      if (optopt == 't' || optopt == 'v' || optopt == 'n')
        fprintf(stderr, "Option -%c requires parameter\n", optopt);
      else
        fprintf(stderr, "Unknown option %c\n", optopt);
      exit(1);
    }
  }

  if (opts->training_samples == NULL) {
    fprintf(stderr, "Traning Samples (-t) not specified\n");
    exit(1);
  } else if (opts->validation_samples == NULL) {
    fprintf(stderr, "Validation Samples (-v) not specified\n");
    exit(1);
  } else if (opts->num_cpus == 0) {
    fprintf(stderr, "Number CPUs (-n) not specified\n");
    exit(1);
  }
}
