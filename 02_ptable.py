import numpy as np

arr = np.zeros((7,18,15),dtype=int) # Periodic table
# Period 1
arr[0,0,0] = 1
arr[0,17,0] = 2
# Period 2
arr[1,0:2,0] = [3,4]
arr[1,12:,0] = range(5,10+1)
# Period 3
arr[2,0:2,0] = [11,12]
arr[2,12:,0] = range(13,18+1)
# Period 4
arr[3,:,0] = range(19,36+1)
# Period 5
arr[4,:,0] = range(37,54+1)
# Period 6
arr[5,0:2,0] = [55,56]
arr[5,3:,0] = range(72,86+1)
# Period 7
arr[6,0:2,0] = [87,88]
arr[6,3:,0] = range(104,118+1)
# Lanthinide series
arr[5,2,:] = range(57,71+1)
# Actinide series
arr[6,2,:] = range(89,103+1)

np.save('./data/ptable.npy', arr)
