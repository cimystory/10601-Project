import sys
from collections import Counter
from math import log
from random import randint

# Read a file
# filename is the path of the file, string type
# returns the content as a string
def readFile(filename, mode="rt"):
    # rt stands for "read text"
    fin = contents = None
    try:
        fin = open(filename, mode)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents



def main(argv):
    filepath = "download/training_set/" + argv[0]
    content = readFile(filepath).split('\n')[1:]
    score = []
    total = 0
    average = 0

    for line in content:
        if line != "":
            stat = line.split(',')
            score.append(int(stat[1]))
            total += 1
    counter = Counter(score)

    for i in range(1,6):
        proportion = float(counter[i]) / total
        average += i * proportion
        print ("Rating %d: %0.2f of the users." % (i, proportion))

    print ("Average Rating: %0.1f" % average)
    print





if __name__ == '__main__':
    main(sys.argv[1:])
