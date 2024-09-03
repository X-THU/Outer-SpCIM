import numpy as np
import math


def cnt_length (a:np.array)->int:
    H,W = a.shape
    len_max = 0
    for h in range(0,H):
        len = 0
        for w in range(0,W):
            if a[h,w] != 0 :
                len = w
        if len > len_max:
            len_max = len
    return len_max+1
def cnt_nz (a): # Count the number of non-zeros in a row
    sum = 0
    for i in a:
        if i != 0 :
            sum += 1
    return sum

def shift_down(matrix,row_index,shift_down_num):
    row  = matrix[row_index,:]
    nz_num_row = cnt_nz(row)
    row_above = matrix[row_index-1, :]
    nz_num_row_above = cnt_nz(row_above)
    #Row Transformation
    for i in range(0,shift_down_num):
        row[nz_num_row+shift_down_num-1-i] = row_above[nz_num_row_above-1-i]
        row_above[nz_num_row_above-1-i] = 0
    matrix[row_index,:] = row
    matrix[row_index-1,:] = row_above
    return  matrix



def Temporal_Stealing(input_array:np.array)->np.array:
    row,col  = input_array.shape
    random_csr_temporal_stealing = np.zeros((row, col), dtype=int)
    for i in range(0, row):
        row_array = input_array[i, :]
        nz_index = 0
        for j in range(0, col):
            if row_array[j] != 0:
                random_csr_temporal_stealing[i, nz_index] = row_array[j]
                nz_index += 1
    return random_csr_temporal_stealing

def Spatial_Stealing(input_array:np.array)->np.array:
    # SS-Step1: Count lower bound ceil(nz_num/row)
    # Count non-zero number
    Optimum_Solution = input_array.copy()
    nz_num = 0
    row,col = input_array.shape
    for i in range(0, row):
        for j in range(0, col):
            if input_array[i, j] != 0:
                nz_num += 1
    # print(nz_num)
    lower_bound = math.ceil(nz_num / row)

    # SS-step2: find Optimal Solution
    for length in range(lower_bound, col + 1):
        # Step2.1 Find Slack row_index
        slack_index = []
        for i in range(row - 1, -1, -1):  # Search from Bottom to Up
            if cnt_nz(input_array[i, :]) <= length:
                slack_index.append(i)

        Final_Solution = input_array.copy()
        next_length = 1
        # Step2.2 Find Possible Solution
        for i in slack_index:
            Solution = input_array.copy()
            find_flag = 1
            row_index = i
            for j in range(0, row - 1):
                slack_row = Solution[row_index, :]
                slack_row_above = Solution[row_index - 1, :]
                slack = length - cnt_nz(slack_row)
                shift_down_num = min(slack, cnt_nz(slack_row_above))
                Solution = shift_down(Solution, row_index, shift_down_num)
                if cnt_nz(Solution[row_index - 1, :]) > length:
                    find_flag = 0
                    break
                else:
                    row_index -= 1
            if find_flag == 1:
                Final_Solution = Solution
                next_length = 0
                break
        if next_length == 0:
            #print("Find Solution")
            #print(Final_Solution)
            Optimum_Solution = Final_Solution
            break
    return Optimum_Solution


def schedule (a:np.array)->np.array:
    TS = Temporal_Stealing(a)
    SS = Spatial_Stealing(TS)
    return SS
