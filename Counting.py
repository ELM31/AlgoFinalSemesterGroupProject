#Radix Sort

import random

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    #Count occurences of each digit in the current place value
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    #update count[i] so that it contains actual position in the output[]
    for i in range(1, 10):
        count[i] += count[i - 1] # Cumulative sum for stable sorting

    #Build the output array by placing elements in correct order    
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1 #Decrement count to handle duplicates

    #Copy sorted output back to the original array
    for i in range(n):
        arr[i] = output[i] #overwrite original array with sorted values




















        
