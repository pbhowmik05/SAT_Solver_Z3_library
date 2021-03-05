

#include <stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>

#define n 9
int loc_x, loc_y;


//checks the elements in the suduko for redundancies in the column, row and the associate box
int placement_check(int matrix[n][n], int x, int y, int data){

    int row_checker, col_checker, box_checker;

    int box_row_st = x - x%3;
    int box_col_st = y - y%3;

    for(int i = 0; i<n; i++){     //row check
        if(i!=y && matrix[x][i]== data)
            return 1;
    }

    for(int j = 0; j<n; j++){   //column check
        if(j!=x && matrix[j][y]== data)
          return 1;
    }

    for(int p=box_row_st; p < box_row_st+3; p++)   //box check
    for(int q=box_col_st; q < box_col_st+3; q++)
    {
        //printf("%s ", "test");
        //printf("element: %d ", matrix[p][q]);
        if(matrix[p][q]== data && p!=x && q!=y) return 1;
    }
    return 0;
}




//returns 1 when the placement is routable in the sudoko board
bool valid_route(int matrix[n][n], int x, int y, int data){
  _Bool placement = placement_check(matrix, x, y, data);
  if(placement==1){
      return false;
  }else{
      return true;
  }
}

int preplacement_check(int matrix[n][n], int x, int y){
    int counter=0;
    for(int i=0; i<x; i++){

        for(int j=0; j<y; j++)
        {
            //debug
            //printf("%d ", matrix[i][j]);
            //endDebug

            int data_val = matrix[i][j];
            //printf("data_val: %d\n", data_val);
            if(data_val>0){
                //printf("valid_route: %d\n", valid_route(matrix, i, j, data_val)); //debug
                if(!valid_route(matrix, i, j, data_val)){
                    counter++;
                    if(counter>0){
                        printf(" The sudoku has redundancies at locations: (%d, %d)\n",  i, j);
                    }
                }

              }

        }


    }
    printf("\n Number of conflicting numbers are =%d \n", counter);
    return counter;
}


int find_empty_place(int matrix[n][n], int *x, int *y){
    for(*x=0; *x<n; (*x)++)
    for(*y=0; *y<n; (*y)++ ){
        if(matrix[*x][*y] == 0)
            return 1;
    }
    return 0;
}


//suduko engine checkes the matrix whether we can place a data in the box in a recursive way
int sudoku_engine(int matrix[n][n]){
    int x ;
    int y ;
    _Bool place_validator = find_empty_place(matrix, &x, &y);

    if(place_validator==0)
        return 1;

    for(int data=1; data <=n; data++){
        if(valid_route(matrix, x, y, data)){
            matrix[x][y] = data;
            if(sudoku_engine(matrix))
                return 1;
            matrix[x][y] = 0;
        }
    }
    return 0;
}



int main() {
int matrix[9][9];
char *line_buf = NULL;
  size_t row_buf_size = 0;
  int rowcounter = 0;
  ssize_t rowsize;


    FILE *fp = fopen("sudoku1.txt","r");
    if(fp == 0)
    {
      printf("Unable to open the file\n" );
      return 1;
    }

    rowsize = getline(&line_buf, &row_buf_size, fp);

    while (rowsize >= 0)
    {
    int column = 0;
    /* Increment our line count */

    char* data_value = strtok(line_buf, ",");

    while (data_value != NULL) {
    matrix[rowcounter][column] = atoi(data_value);
    data_value = strtok(NULL, ",");
    column++;
    }

    rowsize = getline(&line_buf, &row_buf_size, fp);
    rowcounter++;
    }




    //debug
    //int test = preplacement_check(matrix, 9, 9);
    //printf("result_Placement_check: %d ",placement_check(matrix, 0, 1, 3));
    //endDebug
    printf("Here is the given sudoku challenge!!!\n");
    for(int ii=0; ii<9; ii++){
      for(int jj=0; jj<9; jj++){
        printf("%3d", matrix[ii][jj]);
      }
      printf("\n");
    }


    if(preplacement_check(matrix, 9, 9)>0){
      printf("Inconsistent board, Program terminatting!!\n");
      exit(1);

    }

    if(sudoku_engine(matrix)==1){
        printf("This sudoku has solution\n" );

        printf("-----------------------------\n");
        for(int row=0; row<n; row++){
            printf("|");
            for(int col=0; col<n; col++){
                printf("%3d", matrix[row][col]);
            }
            printf("|\n");
        }
        printf("-----------------------------\n");
    } else {
        printf("there is no solution for the given soduko");
    }

    fclose(fp);
    return 0;
}
