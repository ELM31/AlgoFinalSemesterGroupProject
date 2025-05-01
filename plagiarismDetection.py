from difflib import SequenceMatcher

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
def rabin_karp_lines(file1, file2, q=101):
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

#example use of simpleSimilarity
print(simpleSimilarity('Samples/plag.txt', 'Samples/example', 'utf8'))

#example use of rabin_karp_lines
duplicates = rabin_karp_lines('Samples/example', 'Samples/plag.txt', 101)
print("Duplicate lines found:")
for line in duplicates:
    print(line)
