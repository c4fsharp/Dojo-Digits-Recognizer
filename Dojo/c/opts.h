#ifndef OPTS_H
#define OPTS_H

typedef struct {
  char *training_samples;
  char *validation_samples;
  int num_cpus;
} Options;

void Options_set(Options *opts, int argc, char *argv[]);
void Options_show(Options opts);

#endif
