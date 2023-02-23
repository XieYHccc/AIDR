import numpy as np


arr = np.array([[ 0.87415689,  0.8273328 ,  0.40225878,  0.10238861],
                [ 0.61461853,  0.62412656,  0.6780875 ,  0.30737422],
                [ 0.92821608,  0.98625201,  0.59081017,  0.66246603]])

row_indices = [0,0,2]
col_indices = [1,2,3]
mask = np.ones_like(arr,dtype=bool)
mask[np.arange(arr.shape[0]),col_indices]=0

arr1 = arr[mask]
print(arr1.shape)