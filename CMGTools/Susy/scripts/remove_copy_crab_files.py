#!/usr/bin/env python"""This module takes a txt as input, with the names (with full paths) ofroot files; it returns a list of which files are duplicates and should bedeleted"""import osimport sysimport ROOT as rtfrom itertools import groupbyfrom itertools import chainimport redef flatten(list_of_lists):    """Flatten one level of nesting"""    return chain.from_iterable(list_of_lists)def find_duplicate_numbers(my_file):    """Takes as input a txt file with all the cmgTuples;    Returns a list with all the duplicate files"""    numbers_list = set()    duplicates = []    for line in my_file:        cmg_tuple = re.sub(r'.+cmgTuple', 'cmgTuple', line)        jobs_number = cmg_tuple[9:-12]        # cmg_tuple = re.sub(r'.+susy_tree_', '', line).rstrip('.root\n')        # jobs_number = int(cmg_tuple)        if jobs_number.endswith('_'):            jobs_number = jobs_number.rstrip('_')            print cmg_tuple, jobs_number        if jobs_number in numbers_list:            duplicates.append(jobs_number)        else:            numbers_list.add(jobs_number)    print "There are these many duplicates", len(duplicates)    print "There are these many to keep", len(numbers_list)    return duplicatesdef match_file_to_number(the_list, thefile):    """returns a list of tuples with all the duplicate files    need to give a list of duplicate numbers"""    files_list = []    for line in thefile:        cmg_tuple = re.sub(r'.+cmgTuple', 'cmgTuple', line)        job_number = cmg_tuple[9:-12]        # cmg_tuple = re.sub(r'.+susy_tree_', '', line).rstrip('.root\n')        # job_number = int(cmg_tuple)        if job_number.endswith('_'):            job_number = job_number.rstrip('_')        if job_number in the_list:            print job_number            file_tuple = (int(job_number), line.rstrip('\n'))            files_list.append(file_tuple)    return files_listdef createSets(fileTuplesList):    """returns a list of sets of duplicate files; takes as input    the list of tuples: numbers and corresponding files"""    groups_list = []    for key, group in groupby(fileTuplesList, lambda x: x[0]):        tmp_list = set()        for thing in group:            tmp_list.add(thing[1])        groups_list.append(tmp_list)    return groups_listdef check_root_file(rootfile, is_edm):    """tells me whether the root file is good or not, returns True if good"""    if is_edm is True:        rt.gROOT.ProcessLine(".x ~/tmp/rootlogon.C")    root_file = rt.TFile(rootfile)    if root_file.TestBit(rt.TFile.kRecovered):        print "file recovered", root_file    return not root_file.IsZombie() and not\        root_file.TestBit(rt.TFile.kRecovered)def makeSizeDictionary(fileSet):    """Takes a set of files as input;    Returns a dictionary (file: size)"""    file_dict = {}    for line in fileSet:        statinfo = os.stat(line)        file_dict[line] = statinfo.st_size    return file_dictdef compareFileSizes(fileDict):    """Takes a dictionary (file: size) as input;    returns the string name of the good root file with highest size"""    finalSize = 0    fileName = []    fileName.append('')    for file in fileDict:        statinfo = os.stat(file)        if statinfo.st_size > finalSize and check_root_file(file, True):            finalSize = statinfo.st_size            fileName[0] = file    return str(fileName[0])if __name__ == '__main__':    ARGS = sys.argv[1:]    if not ARGS:        print 'usage: ./remove_copy_crab_files.py <txt-file>'        sys.exit(1)    INPUT_FILE = open(ARGS[0], 'r')    NUM_LIST = find_duplicate_numbers(INPUT_FILE)    INPUT_FILE.close()    MY_FILE_AGAIN = open(ARGS[0], 'r')    FILE_LIST = match_file_to_number(NUM_LIST, MY_FILE_AGAIN)    # Initiate the lists with good and bad files    FILES_TO_KEEP = []    FILES_TO_TRASH = []    # Loop over the list of GROUPS of cmgTuples to find the good files    GROUPS = createSets(FILE_LIST)    for group in GROUPS:        fileDict = makeSizeDictionary(group)        FILES_TO_KEEP.append(compareFileSizes(fileDict))    LIST_OF_LISTS = flatten(GROUPS)    for element in LIST_OF_LISTS:        if element in FILES_TO_KEEP:            pass        else:            FILES_TO_TRASH.append(element)    OUT_FILE = open('listToTrash.src', 'w')    TRASH_STRING = '\nrm -f '.join(FILES_TO_TRASH)    OUT_FILE.write('rm -f ')    OUT_FILE.write(TRASH_STRING)    OUT_FILE.close()    print len(FILES_TO_KEEP)    print len(FILES_TO_TRASH)