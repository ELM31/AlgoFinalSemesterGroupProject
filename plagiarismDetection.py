import sys
from difflib import SequenceMatcher
from algo.KMP_test import kmp_search


#gives a ration of similarity between two files in percentage
def simpleSimilarity(file1, file2, format='CP1252'):
    #open the files with correct encoding
    if format == 'utf8':
        with open(file1, encoding = 'utf8') as f1, open(file2, encoding = 'utf8') as f2:
            read1 = f1.read()
            read2 = f2.read()
    else:
        with open(file1) as f1, open(file2) as f2:
            read1 = f1.read()
            read2 = f2.read()
    #return ratio of similarity using Ratcliff/Obershelp
    #2 * matching char / total char
    return SequenceMatcher(None, read1, read2).ratio() * 100

#finds the exact duplicate lines in two files using Rabin-Karp hashing
def rabin_karp_duplicate(file1, file2, q=101):
    d = 256  #Number of characters in the ASCII alphabet (256 ASCII)
    line_hashes = set()  #store line hashes in set
    
    with open(file1, 'r', encoding = 'utf8') as f1, open(file2, 'r', encoding = 'utf8') as f2:
        file1Lines = [line.strip() for line in f1.readlines()]
        file2Lines = [line.strip() for line in f2.readlines()]
    
    #we need the hash of each line to compare
    def get_hash(line, q):
        h = 0
        for char in line:
            h = (d * h + ord(char)) % q
        return h

    #get has for each line and add to the set
    for phrase in file1Lines:
        line_hash = get_hash(phrase, q)
        line_hashes.add(line_hash)
        
    duplicates = [] #store the lines that are found to be duplicates

    #check for duplicate hashes in the second file
    for phrase in file2Lines:
        line_hash = get_hash(phrase, q)
        if line_hash in line_hashes:
            duplicates.append(phrase)

    return duplicates

def KMPDuplicate(file1, file2, ignore_case=False):
    #KMP algorithm to find duplicates in two files, file 1 acts as the pattern to search for
    #only using utf8 encoding for now so maybe change it
    positions = dict()
    patterns = []

    for line in patterns:
        if ignore_case:
            line = line.lower()
            text = text.lower()

    with open(file1, 'r', encoding='utf8') as f1, open(file2, 'r', encoding='utf8') as f2:
        patterns = [line.strip() for line in f1.readlines()]
        text = f2.read().strip()
        #check if file is empty
        if not patterns:
            raise ValueError("The first file (pattern file) is empty.")
        
        if not text:
            raise ValueError("The second file is empty.")
        
        for line in patterns:
            #skip blank lines
            if not line:
                continue
            
            positions[line] = []  # Initialize the line in the dict
            positions[line] = kmp_search(text, line)
    #returns a dict{line: position}, position is the index of the line in the text from file 2
    return positions

#helper for getting only the duplicates from the dict returned by KMPDuplicate
def getDuplicatesFromDict(dictionary):
    """
    Get the key from the value in a dictionary.
    if value is empty return the key
    key is the line, value is the position in the text
    """
    duplicates = dict()
    for key, val in dictionary.items():
        if val != []:
            duplicates[key] = val
    return duplicates

def plagiarism_summary(file1, file2, encoding='utf8', q=101, ignore_case=False):
    summary = dict()

    # 1. Similarity Score
    similarity = simpleSimilarity(file1, file2, format=encoding)
    summary['Similarity Score (%)'] = round(similarity, 2)

    # 2. Rabin-Karp Duplicate Lines
    duplicates = rabin_karp_duplicate(file1, file2, q=q)
    summary['Exact Duplicate Lines Count'] = len(duplicates)
    summary['Exact Duplicate Lines'] = duplicates

    # 3. KMP Pattern Matches
    kmp_results = KMPDuplicate(file1, file2)  # we can add ignore_case if we upgrade KMPDuplicate
    kmp_duplicates = getDuplicatesFromDict(kmp_results)
    summary['Pattern Matches Count'] = len(kmp_duplicates)
    summary['Pattern Matches'] = kmp_duplicates

    return summary



#example use of simpleSimilarity
#print(simpleSimilarity('Samples/plag.txt', 'Samples/example', 'utf8'))

#example use of rabin_karp_lines
#duplicates = rabin_karp_duplicate('Samples/example', 'Samples/plag.txt', 101)
#print("Duplicate lines found:")
#for line in duplicates:
#    print(line)

#pos = KMPDuplicate('Samples/frankcopy.txt', 'Samples/Frankenstein.txt')
#print(pos)
#print(getDuplicatesFromDict(pos))

#result = plagiarism_summary('Documents/sample1.txt', 'Documents/sample2.txt')

#for key, value in result.items():
#    print(f"{key}: {value}")
