import json
import sys
import csv
import os
import operator

from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from qcas_datafiles import PSLfile, TSLfile, MSLfile
from datetime import datetime

DF_DIRECTORY = "." 
VERSION = "0.1"
        
class QCAS_DF_RemoveGames: 

    # GUI constructor
    def __init__(self):
        self.root = Tk()
        self.setup_GUI()
        
        self.pslfile = ""
        self.tslfile = "" 
    
    def setup_GUI(self): 
        self.root.wm_title("qcas Remove Games v"+VERSION)
        self.root.resizable(0,0)
        help_text = "This script automates the removal of games from QCOM Casino Datafile PSL file.\n"
        ttk.Label(self.root, justify=LEFT,
                  text = help_text).grid(row = 0, columnspan=2, padx=3, pady=3)

        # Choose Current PSL File
        button_Choose_Current_PSL_file = ttk.Button(self.root,
                                                    text = "Choose Current PSL file...",
                                                    width = 30,
                                                    command = lambda: self.handleButtonPress('__current_psl_file__'))                                                    
        button_Choose_Current_PSL_file.grid(row=2, column=0, padx=3, pady=3, sticky='e')

        # Text Entry       
        self.current_psl_filename_tf = ttk.Entry(self.root, width = 50)
        self.current_psl_filename_tf.grid(row=2, column=1)

        
        # Choose TAB Delimited: Approval Withdrawn       
        button_Choose_TAB_file_App_Withdrawn = ttk.Button(self.root,
                                                    text = "TAB file: Remove Games...",
                                                    width = 30,
                                                    command = lambda: self.handleButtonPress('__tab_delimited_file_app_withdrawn__'))                                                    
        button_Choose_TAB_file_App_Withdrawn.grid(row=3, column=0, padx=3, pady=3, sticky='e')

        # Text Entry
        self.games_removed_tf = ttk.Entry(self.root, width = 50)
        self.games_removed_tf.grid(row=3, column=1)
        
        # New PSL fname
        ttk.Label(self.root, text = 'Enter new PSL filename: ').grid(row = 4, column=0, sticky='e', padx=3, pady=3)

        self.new_psl_fname = StringVar()
        now = datetime.now() 
        
        tmp_tsl_fname = "qcas_" + str(now.year) + "_" + "{:02}".format(now.month) + "_v01.psl"
        
        self.new_psl_fname.set(tmp_tsl_fname)
        self.new_tsl_filename_tf = ttk.Entry(self.root, width = 50, textvariable=self.new_psl_fname)
        self.new_tsl_filename_tf.grid(row=4, column=1, padx=3, pady=3)

        # Button
        button_start = ttk.Button(self.root, text = "Start...",
                                  command = lambda: self.handleButtonPress('__start__'))
        button_start.grid(row=5, columnspan=2, sticky='se', padx=5, pady=5)        
        self.root.mainloop()    
    
    def removeGame(self, tsl_game_object):
        ssan = tsl_game_object.ssan
        
        for psl_game_entry in self.PSLfile_object_list:
            if psl_game_entry.ssan == ssan: 
                self.PSLfile_object_list.remove(psl_game_entry)
                break

    def save_PSL_list_toDisk(self, fname):        
        with open(fname, 'w+') as pslfile: 
            for psl_entry in self.PSLfile_object_list: 
                pslfile.write(psl_entry.toString()+"\n")
                    
    def sort_PSL_csvfile(self, fname):
        sortedlist = list()         
        try:
            with open(fname, 'r') as infile: 
                reader = csv.reader(infile, delimiter=",")

                # Sort PSL column 1, 0, 4: MID, Game Name, Approval Number
                sortedlist = sorted(reader, key=operator.itemgetter(1,0,4))
      
            with open(fname, 'w') as outfile: 
                # To print a list
                for item in sortedlist:
                    outfile.writelines([",".join(item), '\n'])
                    
        except csv.Error as e: 
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
    
    
    def handleButtonPress(self, cmd): 
        if cmd == '__start__': 
            # Read Remove Games File
            games_to_be_removed_list = self.genTSLEntries(os.path.basename(self.tslfile))

            self.TSLfile_object_list = list() 
            for game in games_to_be_removed_list:
                self.TSLfile_object_list.append(TSLfile(game))
            
            print("Size of TSL list is: " + str(len(self.TSLfile_object_list)))            
            
            self.sort_PSL_csvfile(self.pslfile) # Sort PSL first
            
            # Read PSL file and generate PSL object list
            self.PSLfile_object_list = self.check_datafile_format(self.pslfile, 'PSL')
            print("Size of PSL list is: " + str(len(self.PSLfile_object_list)))

            # Remove SSANs in PSL list
            for game in self.TSLfile_object_list: 
                self.removeGame(game)
                
            print("Size of new PSL list is: " + str(len(self.PSLfile_object_list)))
            
            self.save_PSL_list_toDisk(self.new_tsl_filename_tf.get()) 
            self.sort_PSL_csvfile(self.new_tsl_filename_tf.get()) 
            
        elif cmd == '__current_psl_file__':
            tmp = filedialog.askopenfilename(initialdir=DF_DIRECTORY, title = "Select Current PSL File",filetypes = (("PSL files","*.PSL"),("all files","*.*")))
            
            if tmp: # Selected a PSL file
                self.current_psl_filename_tf.delete(0, END)                
                self.current_psl_filename_tf.insert(0, tmp)        
                self.pslfile = tmp
                
            # update new PSLfilename 
            self.new_psl_fname.set(self.update_fname_version(os.path.basename(self.current_psl_filename_tf.get())))
            
        
        elif cmd == '__tab_delimited_file_app_withdrawn__':         
            tmp = filedialog.askopenfilename(initialdir=DF_DIRECTORY, title = "Select Tab delimited .TXT approval withdrawn games",filetypes = (("TXT files","*.TXT"),("all files","*.*")))
            
            if tmp: # Selected a PSL file
                self.games_removed_tf.delete(0, END)                
                self.games_removed_tf.insert(0, os.path.basename(tmp)) 
                self.tslfile = tmp

    def update_fname_version(self, fname): 
        fields = fname.split('_')
        file_version = fields[3][1:-4] # remove suffix i.e. .psl/.msl/.tsl, and 'v' char        
        new_file_version = int(file_version) + 1
        
        if new_file_version < 10: 
            return fields[0] + "_" + fields[1] + "_" + fields[2] + "_" + "v0" + str(new_file_version) + ".psl"
        else: 
            return fields[0] + "_" + fields[1] + "_" + fields[2] + "_" + "v" + str(new_file_version) + ".psl"

                
    def check_datafile_format(self, file, file_format):
        item_list = list()
        
        # test PSL file format
        if file_format == 'PSL':
            with open(file, 'r') as psl:
                psl_entries = csv.reader(psl, delimiter=',')
                try:
                    for row in psl_entries:
                        item_list.append(PSLfile(",".join(row)))

                except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (file, psl_entries.line_num, e))

        # test MSL file format
        elif file_format == 'MSL':           
            with open(file, 'r') as msl:
                msl_entries = csv.reader(msl, delimiter=',')
                try:
                    for item in msl_entries:
                        item_list.append(MSLfile(",".join(item)))

                except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (file, msl_entries.line_num, e))

        # test TSL file format
        elif file_format == 'TSL':
            with open(file, 'r') as tsl:
                tsl_entries = csv.reader(tsl, delimiter=',')
                try:
                    for item in tsl_entries:
                        item_list.append(TSLfile(",".join(item)))
                except csv.Error as e: 
                    sys.exit('file %s, line %d: %s' % (file, tsl_entries.line_num, e))

        return item_list

    # input: TAB delimited file, exported from MS Excel.
    # output: list of new TSL game entries
    def genTSLEntries(self, fname):
        tsl_entries = list() 
        try:
            with open(fname, 'r') as infile: 
                next(infile) #ignore header
                
                input_fieldnames = ['game_name', 'manufacturer', 'approval_status', 
                    'approval_date', 'market','ssan','vid_type','binimage','bin_type']
                reader = csv.DictReader(infile, delimiter='\t', fieldnames=input_fieldnames)

                for row in reader:
                    # Remove commas in game name
                    # If you want to replace it with another symbol change the following 
                    #   line to: .replace(",","[INSERT SYMBOL HERE]")
                    cleaned_game_name = str(row['game_name']).replace(",", "")
                    
                    # remove non-ascii characters using re
                    cleaned_game_name = re.sub(r'[^\x00-\x7f]',r'', cleaned_game_name)
                
                    # Process Video Type & Append to game name
                    if row['vid_type'].lower() == 'video':
                        cleaned_game_name += "-V"
                    else :
                        cleaned_game_name += "-S"

                    # Process Binimage type
                    if row['bin_type'] == 'BIN LINK FILE':
                        my_bin_type = 'BLNK'
                    elif row['bin_type'] == 'PSA 32':
                        my_bin_type = "PS32"
                    elif row['bin_type'] == 'HMAC SHA1':
                        my_bin_type = "SHA1"
                    else:
                        sys.exit('Unknown binimage type %s' % row['bin_type'])         

                    game_entry = str("%02d,%010d,%-60s,%-20s,%4s\n" % 
                        (int(row['manufacturer']), int(row['ssan']), 
                        cleaned_game_name, row['binimage'], my_bin_type))
                    tsl_entries.append(game_entry)
            
        except csv.Error as e: 
            sys.exit('file %s, line %d: %s' % (fname, reader.line_num, e))
        
        return tsl_entries        
        
            
def main():      
    app = QCAS_DF_RemoveGames()    
    
if __name__ == "__main__": main()
