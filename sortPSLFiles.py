# input: TSL file that is unordered
# output: Filename for Single TSL file that is ordered.
# Assumptions: File input must end with "_unsorted.psl" and input file exists

import csv
import sys
import operator
import os

class SortPSLFiles:

    def __init__(self, f1):

        self.filename = f1
        # Verify correct filename format
        if self.filename.endswith("_unsorted.psl"): 
            self.sortFile()
        else:   
            print("\nERROR: Filename format does not end with '_unsorted.psl' rename the file and try again")
            sys.exit(1)
    
    def sortFile(self):
        # remove last 13 characters from string. 
        outfilename = self.filename[:-13] + ".psl"
        try:
            outfile = open(outfilename, "w+")
            infile = open(self.filename, 'r')
            reader = csv.reader(infile, delimiter=",")

            # Sort PSL column 1, 0, 4: MID, Game Name, Approval Number
            sortedlist = sorted(reader, key=operator.itemgetter(1,0,4))
  
            # To print a list
            for item in sortedlist:
                # Uncomment next line to print to screen. 
                # print (",".join(item))
                outfile.writelines([",".join(item), '\n'])

            outfile.close()

        except csv.Error as e: 
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
        self.filename = outfilename

def main():
    # Run Class with arg[1] (filename) as input
    app = SortPSLFiles(sys.argv[1])    
    
if __name__ == "__main__": main()
