import json
import sys

MID_LIST = [ '00', '01', '05', '07', '09', '12', '17']
VALID_BIN_TYPES = ['BLNK','PS32','SHA1']

class MSLfile:
    # helper class for MSL file
    def __init__(self, line):
        fields = str(line).split(',')
        
        self.year = int(fields[0])
        valid_year = list(range(2017,9999))
        assert(self.year in valid_year) # verify year field is 2017-9999
       
        self.month = int(fields[1])
        valid_months = list(range(1,13))
        assert(self.month in valid_months) # verify months fields is 1-12
        
        included_cols = list(range(2, 33))
        self.seed_list = list(fields[i] for i in included_cols)
        assert(len(self.seed_list) == 31) # verify 31 seeds
        for seed in self.seed_list: 
            assert(len(seed) == 8)  # verify each seed has 8 characters

class PSLfile:
    # helper class for PSL file
    def __init__(self, line):
        fields = str(line).split(',')
        input_line = str(line).strip(',') # remove trailing comma

        self.game_name = fields[0].strip() # strip spaces
        
        assert(len(self.game_name) < 31)
       
        self.manufacturer = fields[1]
        assert(self.manufacturer in MID_LIST)
        
        self.year = int(fields[2])
        valid_year = list(range(2017,9999))
        assert(len(fields[2]) == 4)
        assert(self.year in valid_year)
        
        self.month = int(fields[3])
        valid_months = list(range(1,13))
        assert(self.month in valid_months)
        
        assert(len(fields[4]) == 10)
        self.ssan = int(fields[4].strip())

        # included_cols = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
        included_cols_v2 = list(range(5,36))
        self.hash_list = list(fields[i] for i in included_cols_v2)
        assert(len(self.hash_list) == 31)
        
        self.psl_entry_str = self.toString()
        if self.psl_entry_str != input_line:
            self.identifyDifference(self.psl_entry_str, input_line)
        
        assert(self.psl_entry_str == input_line)
        
    def toString(self): 
        self.psl_entry_str = "%(game_name)-30s,%(mid)02d,%(year)4s,%(month)02d,%(ssan)010d," % {'game_name': self.game_name, 'mid': int(self.manufacturer), 'year': self.year, 'month': int(self.month), 'ssan': int(self.ssan)}
        for hash_item in self.hash_list: 
            self.psl_entry_str += hash_item + ","
        return self.psl_entry_str.strip(',')
        
    def identifyDifference(self, str1, str2): 
        cases = [(str1, str2)] 
        for a,b in cases:     
            print('{} => {}'.format(a,b))  
            for i,s in enumerate(difflib.ndiff(a, b)):
                if s[0]==' ': continue
                elif s[0]=='-':
                    print(u'Delete "{}" from position {}'.format(s[-1],i))
                elif s[0]=='+':
                    print(u'Add "{}" to position {}'.format(s[-1],i))    
    
    def toJSON(self): 
        return (json.dumps(self, default=lambda o: o.__dict__, sort_keys = True, indent=4))
        
class TSLfile:
    # helper class for TSL file
    def __init__(self, line):
        
        fields = str(line).split(',')
        self.mid = fields[0]
        assert(self.mid in MID_LIST)
        
        assert(len(fields[1]) == 10)
        self.ssan = int(fields[1])
        
        self.game_name = fields[2].strip()
        assert(len(self.game_name) < 61)
        
        self.bin_file = fields[3].strip()
        assert(len(self.bin_file) < 21)
        
        self.bin_type = fields[4].strip()
        assert(self.bin_type in VALID_BIN_TYPES)
    
    def toJSON(self): 
        return (json.dumps(self, default=lambda o: o.__dict__, sort_keys = True, indent=4))

    def toJSON_oneline(self): 
        return (json.dumps(self, default=lambda o: o.__dict__, sort_keys = True))