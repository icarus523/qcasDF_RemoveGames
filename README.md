# qcasDF_RemoveGames
QCAS Datafiles Remove Game script, used to automatically remove games from current PSL files when withdrawing approvals from game. 

Takes two input:
1. a TAB delimited file which consists of the games that are to be removed from the datafiles
2. the Current PSL file

The current PSL file is then removed of entries that exist in (1). 

Output: New PSL file which doesn't contain games from (1). 

Important: The current PSL file used must be first sorted. 
