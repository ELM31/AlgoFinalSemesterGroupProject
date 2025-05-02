import sys
sys.path.append("./algo")
import time
import os
import MergeSortModified

def sortByTitle(filePaths):
    """
    Sorts a list of file paths by the title property of the files, returns list.
    """
    filetitles = []
    for filePath in filePaths:
        filetitles.append(os.path.basename(filePath))
    # Sort the file titles using merge_sort_string
    return MergeSortModified.merge_sort_string(filetitles)

def sortByDateModified(filePaths):
    """
    Sorts a list of file paths by the date property of the files, oldest to newest, returns tuple.
    """
    filedates = []
    for filePath in filePaths:
        # Get the last modified time of the file
        filedates.append((os.path.basename(filePath), os.path.getmtime(filePath)))
    # Sort the file dates using merge_sort_date
    sorted_dates = MergeSortModified.merge_sort_date(filedates)
    #convert to normal time
    for i in range(len(sorted_dates)):
        sorted_dates[i] = (sorted_dates[i][0], time.ctime(sorted_dates[i][1]))
    return sorted_dates
    
def sortByDateCreated(filePaths):
    """
    Sorts a list of file paths by the date property of the files, oldest to newest, returns tuple.
    """
    filedates = []
    for filePath in filePaths:
        # Get the last modified time of the file
        filedates.append((os.path.basename(filePath), os.path.getctime(filePath)))
    # Sort the file dates using merge_sort_date
    sorted_dates = MergeSortModified.merge_sort_date(filedates)
    #convert to normal time
    for i in range(len(sorted_dates)):
        sorted_dates[i] = (sorted_dates[i][0], time.ctime(sorted_dates[i][1]))
    return sorted_dates

#user input

filepaths = ("Samples/plag.txt", "Samples/frankcopy.txt", "Samples/Frankenstein.txt", "Samples/Romea and Juliet.txt", "Samples/example", "Samples/Moby Dick.txt")
#title sort
#print(sortByTitle(filepaths))
#print(sortByDateCreated(filepaths))
print(sortByDateModified(filepaths))


