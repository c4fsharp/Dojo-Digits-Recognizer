#ifndef DATA_H
#define DATA_H

typedef struct {
  int num_cols;
  int num_rows;
  int *data;
} Data;

void Data_show_dims(Data data);
void Data_read_file(Data *data, char *filename);
int Data_get(Data data, int row, int col);

#endif
