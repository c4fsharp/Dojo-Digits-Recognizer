#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "data.h"

#define NUMBUF_SIZE 20

// row 0 is label
int Data_get(Data data, int row, int col) {
  return data.data[data.num_cols * row + col];
}

void Data_set_dims(Data *data, FILE *file) {
  int c = 0;
  memset(data, 0, sizeof(*data));

  // first line is header
  while ((c = fgetc(file)) != '\n') {
    if (c == ',') {
      data->num_cols++;
    }
  }
  // this is correct, first column is the label

  while ((c = fgetc(file)) != EOF) {
    if (c == '\n') {
      data->num_rows++;
    }
  }
}

void Data_set(Data *data, int row, int col, int value) {
  data->data[data->num_cols * row + col] = value;
}

void Data_populate(Data *data, FILE *file) {
  int c;
  int numbuf_idx = 0;
  char numbuf[NUMBUF_SIZE];
  int num;
  int done = 0;
  int row = 0;
  int col = 0;
  const int size = data->num_rows * data->num_cols * sizeof(int);

  rewind(file);

  data->data = malloc(size);

  // first line is header
  while ((c = fgetc(file)) != '\n') {
      /* empty on purpose */
  }

  memset(numbuf, 0, sizeof(NUMBUF_SIZE));
  numbuf_idx = 0;

  while (!done) {

    while (1) {
      c = fgetc(file);
      if (c == ',') {
        num = atoi(numbuf);
        Data_set(data, row, col, num);
        memset(numbuf, 0, sizeof(NUMBUF_SIZE));
        numbuf_idx = 0;
        col++;
      }
      else if (c == '\n') {
        num = atoi(numbuf);
        Data_set(data, row, col, num);
        memset(numbuf, 0, sizeof(NUMBUF_SIZE));
        numbuf_idx = 0;
        row++;
        col = 0;
        break;
      }
      else if (c == EOF) {
        done = 1;
        break;
      }
      else {
        numbuf[numbuf_idx++] = c;
      }
    }
  }
}

void Data_show_dims(Data data) {
  printf("data.cols: %d\n", data.num_cols);
  printf("data.rows: %d\n", data.num_rows);
}

void Data_read_file(Data *data, char *filename) {
  FILE *file = fopen(filename, "r");
  if (file == NULL) {
    fprintf(stderr, "Could not read %s\n", filename);
    exit(1);
  }

  Data_set_dims(data, file);
  Data_populate(data, file);
}

