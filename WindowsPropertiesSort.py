import sys
sys.path.append("./algo")

import os
import MergeSortModified

def sortByTitle(filePaths):
    """
    Sorts a list of file paths by the title property of the files.
    """
    filetitles = []
    for filePath in filePaths:
        filetitles.append(os.path.basename(filePath))
    # Sort the file titles using merge_sort_string
    return MergeSortModified.merge_sort_string(filetitles)

#user input

filepaths = ("Samples/plag.txt", "Samples/frankcopy.txt", "Samples/Frankenstein.txt", "Samples/Romea and Juliet.txt", "Samples/example", "Samples/Moby Dick.txt")
#title sort
print(sortByTitle(filepaths))

