import time

def isSmallerString(str1, str2):
    # Compare two strings
    str1 = str1.lower()
    str2 = str2.lower()
    if str1 < str2:
        return True
    else:
        return False

def merge_sort_string(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Find the middle index
        left_half = arr[:mid]  # Divide list into halves
        right_half = arr[mid:]

        # Recursively sort both halves
        merge_sort_string(left_half)
        merge_sort_string(right_half)

        i = j = k = 0

        # Merge the sorted halves
        while i < len(left_half) and j < len(right_half):
            if isSmallerString(left_half[i], right_half[j]):  # Use isSmaller for comparison
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Copy remaining elements of left_half, if any
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        # Copy remaining elements of right_half, if any
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            
    return arr

def isSmallerDate(left, right):
    # Compare two dates, left and right are tuples (filename, timestamp)
    left = left[1]  # Extract the timestamp from the tuple
    right = right[1]
    if left < right:
        return True
    else:
        return False

def merge_sort_date(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Find the middle index
        left_half = arr[:mid]  # Divide list into halves
        right_half = arr[mid:]

        # Recursively sort both halves
        merge_sort_date(left_half)
        merge_sort_date(right_half)

        i = j = k = 0

        # Merge the sorted halves
        while i < len(left_half) and j < len(right_half):
            if isSmallerDate(left_half[i], right_half[j]):  # Use isSmaller for comparison
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Copy remaining elements of left_half, if any
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        # Copy remaining elements of right_half, if any
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            
    return arr
