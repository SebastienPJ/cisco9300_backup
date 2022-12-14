def removeSpaces(filepath, filename):
    with open(filepath) as infile, open(f'BackupOutput/{filename}_Staged.txt', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output




def removeCommasQuotesColons(arr):
    endArr = []

    for line in arr:
        newLine = []
        for item in line:

            remove_comma = item.replace(',', '')
            remove_quotes = remove_comma.replace('"', '')
            remove_colon = remove_quotes.replace(':', '')
            
            newLine.append(remove_colon)
        
        while('' in newLine):
            newLine.remove('')
            
        endArr.append(newLine)
    
    return endArr
