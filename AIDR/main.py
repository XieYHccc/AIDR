import numpy as np

# 创建一个二维数组
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 创建一个数组，包含要寻找的元素
elements = np.array([2, 5, 9])

# 寻找第二维中包含任何一个要寻找的元素的索引
idx = np.where(np.isin(arr, elements))

# 输出结果
print(idx)
print(np.isin(arr, elements))

