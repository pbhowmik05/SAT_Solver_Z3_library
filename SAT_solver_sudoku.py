from z3 import *
import numpy as np

## Read the sudoku board values from a comma separated value file
with open('sudoku.txt', 'r') as f:
    board = [[int(num) for num in line.split(',')] for line in f]

# convert the values to integer on the matrix
for row, i in enumerate(board):
    for col, j in enumerate(i):
        board[row][col] = int(j)

print(board)
initialMatrix = []

for row in range(9):
    tempCell = []
    for col in range(9):
        tempCell.append(BoolVector("a_{}_{}".format(row, col), 4))
    initialMatrix.append(tempCell)

s = Solver()

# parameters to check the non zero cells and the numbers from 1~9. The number logic
# is obtained by simplifing the karnot  for 4-binary variables. The binary variables
# represent the numbers from 0~15 and the  num_limit_sat1 checkes whether the number
#is in the range
num_limit_sat1 = []
zore_cell_sat2 = []

for row in range(9):
    for col in range(9):
        num_limit_sat1.append(Or(And(Not(initialMatrix[row][col][0]),initialMatrix[row][col][1]),And(initialMatrix[row][col][0],Not(initialMatrix[row][col][1]),Not(initialMatrix[row][col][2])),And(Not(initialMatrix[row][col][0]),initialMatrix[row][col][3]),And(Not(initialMatrix[row][col][0]),initialMatrix[row][col][2])))
        zore_cell_sat2.append(Or(initialMatrix[row][col][0],initialMatrix[row][col][1],initialMatrix[row][col][2],initialMatrix[row][col][3]))

s.add(num_limit_sat1)
s.add(zore_cell_sat2)


# the given sudoku board is converted to bianary form
board_con_sat3 = []

for row in range(9):
    for col in range(9):
        if board[row][col] != 0:
            bin_value = '{0:04b}'.format(board[row][col])

            constraint = []
            for k in range(4):
                if bin_value[k]=='1':
                    constraint.append(initialMatrix[row][col][k])
                else:
                    constraint.append(Not(initialMatrix[row][col][k]))

            tempConstraint = [And([constraint[elem] for elem in range(len(constraint))])]

            for k in range(len(tempConstraint)):
                board_con_sat3.append(tempConstraint[k])

s.add(board_con_sat3)



# row wise redundancy checking

row_con_sat4 = []
for row in range(9):
    for col in range(8):
        for k in range(col+1,9,1):
            row_con_sat4.append(Or(
                                        Or(And(Not(initialMatrix[row][col][0]),initialMatrix[row][k][0]),And(initialMatrix[row][col][0],Not(initialMatrix[row][k][0]))),
                                        Or(And(Not(initialMatrix[row][col][1]),initialMatrix[row][k][1]),And(initialMatrix[row][col][1],Not(initialMatrix[row][k][1]))),
                                        Or(And(Not(initialMatrix[row][col][2]),initialMatrix[row][k][2]),And(initialMatrix[row][col][2],Not(initialMatrix[row][k][2]))),
                                        Or(And(Not(initialMatrix[row][col][3]),initialMatrix[row][k][3]),And(initialMatrix[row][col][3],Not(initialMatrix[row][k][3])))
                                        ))

#temp = [And([row_con_sat4[i] for i in range(len(row_con_sat4))])]
#s.add(temp)
s.add([And([row_con_sat4[i] for i in range(len(row_con_sat4))])])

# column wise redundancy checking
col_con_sat5 = []
for col in range(9):
    for row in range(9-1):
        for k in range(row+1,9,1):
            col_con_sat5.append(Or(
                                        Or(And(Not(initialMatrix[row][col][0]),initialMatrix[k][col][0]),And(initialMatrix[row][col][0],Not(initialMatrix[k][col][0]))),
                                        Or(And(Not(initialMatrix[row][col][1]),initialMatrix[k][col][1]),And(initialMatrix[row][col][1],Not(initialMatrix[k][col][1]))),
                                        Or(And(Not(initialMatrix[row][col][2]),initialMatrix[k][col][2]),And(initialMatrix[row][col][2],Not(initialMatrix[k][col][2]))),
                                        Or(And(Not(initialMatrix[row][col][3]),initialMatrix[k][col][3]),And(initialMatrix[row][col][3],Not(initialMatrix[k][col][3])))
                                        ))

#temp2 = [And([col_con_sat5[i] for i in range(len(col_con_sat5))])]
#s.add(temp2)
s.add([And([col_con_sat5[i] for i in range(len(col_con_sat5))])])

#3x3 box wise redundancy checking
box_con_sat6 = []

for ii in range(3):
    for jj in range(3):
        box_vec = []
        for i in range(3):
            for j in range(3):
                box_vec.append(initialMatrix[3*ii + i][3*jj + j])
                #print(initialMatrix[3*i0 + i][3*j0 + j])
        for i in range(len(box_vec)-1):
            for j in range(i+1,len(box_vec),1):
                box_con_sat6.append(Or(
                                            Or(And(Not(box_vec[i][0]),box_vec[j][0]),And(box_vec[i][0],Not(box_vec[j][0]))),
                                            Or(And(Not(box_vec[i][1]),box_vec[j][1]),And(box_vec[i][1],Not(box_vec[j][1]))),
                                            Or(And(Not(box_vec[i][2]),box_vec[j][2]),And(box_vec[i][2],Not(box_vec[j][2]))),
                                            Or(And(Not(box_vec[i][3]),box_vec[j][3]),And(box_vec[i][3],Not(box_vec[j][3])))
                                            ))

#        temp3 = [And([box_con_sat6[i] for i in range(len(box_con_sat6))])]

#s.add(temp3)
s.add([And([box_con_sat6[i] for i in range(len(box_con_sat6))])])



if s.check() == sat:
    print("The given sudoku board is satisfied\n")
    my_model = s.model()

    r = []

    for row in range(9):
        for col in range(9):
            tempList = []
            for k in range(4):
                tempList.append(my_model.evaluate(initialMatrix[row][col][k]))
            r.append(tempList)

    bit_wise_val = []
    for row in range(len(r)):
        concatinate = ""
        for col in range(len(r[row])):
            if r[row][col]==True:
                concatinate = concatinate+"1"
            else:
                concatinate = concatinate+"0"
        bit_wise_val.append(concatinate)

    con_decimal = []
    for row in range(len(bit_wise_val)):
        con_decimal.append(int(bit_wise_val[row],2))


    List_array = np.array(con_decimal)


    sudoku_board = List_array.reshape(9,9)
    print(sudoku_board)

else:
    print("There is no solution found!!")
