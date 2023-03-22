# Python script to upload the history of a code using git.
# The local git repository is located in the directory name given by 'dir_git'
#  while the history is saved in the directory name given by 'dir_all'.
# The history is saved as different subdirectories inside 'dir_all', each starting
#  with an integer. A comment can be added in the directory's name as long as
#  there is a space between the integer and the comment.
# The different versions of the code will be uploaded by ascending order of. 
# This script should be placed in the same directory as the git repository 
#  directory and the directory containing all subdirectories.
# The code will erase the files in 'dir_git' except 'README.md' and '.git'.

# TL;DR: 
# You got a folder like this:
# Big_directory/1 - initial code version/file 1.txt
#                                        file 2.txt
#              /2 - second code version/file 1.txt
#                                       file 2.txt
#                                       file 3.txt
#              /4/file 2.txt
#                 file 3.txt
# And you want to upload version 1 then 2 then 4 to a repo using git.
# This code will erase whatever is in the directory specified by 'dir_git' (target repo)
# except the file 'README.md' and directory '.git'.
# The code will then iterate through the versions it finds in 'dir_all' and use
#  the subdirectory's name as commit message.

import os
import subprocess
import numpy
import shutil
import glob

# Directory for git
dir_git = 'my_cool_git_repo'
# Directory containing subdirectories for all versions we want to upload
dir_all = 'my_not_cool_manual_repo'

# To push, add an email and name:
subprocess.run(['git', 'config', '--global', 'user.email', '"your.email@domain.com"'])
subprocess.run(['git', 'config', '--global', 'user.name', '"Your Name"'])


# Obtain all subdirectories to upload
subs = os.listdir(dir_all)

# Trim directory names up to first space character and convert to integer
subs_id = [int(i.split(' ',1)[0]) for i in subs]

# Sort directories in ascending order using the integer in their name
#subs_sort = numpy.sort(subs_id)
# We only care about the indexing of the sort
subs_sort_index = numpy.argsort(subs_id)

# Use the sorted list to iterate through the subdirectories and upload a chronological history to git
for idx in subs_sort_index:
    print('=============== Now woring on folder ID: ' + str(subs_id[idx]) + '===============')
    # Clean the git directory of anything except '.git' and 'README.md'
    # (If you have more files to keep between commits, make sure to add them here to avoid erasing them)
    files = os.listdir(dir_git)
    for f in files:
        path = dir_git+'/'+f

        if ((f == 'README.md') or (f == '.git')):
            print('Not remove: ',path)
        else:
            if os.path.isdir(path):
                #print('Remove directory: ',path)
                shutil.rmtree(path)  
            elif os.path.isfile(path):  
                #print('Remove file: ',path)
                os.remove(path)
            else:  
                print('Special file not removed: ',path)

    # Copy files from the historical subdirectory to this git directory
    #print('PWD: ' + os.getcwd()) 
    #print('Copy: ' + dir_all + '/' + subs[idx] + '/* ./' + dir_git)
    # Use glob glob to wildcard files
    subprocess.run(['cp', '-r'] + glob.glob('./' + dir_all + '/' + subs[idx] + '/*') + ['./' + dir_git + '/'])

    # Move into the git directory to perform git commands
    os.chdir(dir_git)
    #print('PWD: ' + os.getcwd()) 
    
    # Ping repository for new information
    #subprocess.run(['git', 'fetch'])
    subprocess.run(['git', 'pull'])
    
    # Check status of local files with respect to our last fetch
    #subprocess.run(['git', 'status'])
    
    # Add new or modified files
    #subprocess.run(['git', 'add'] + glob.glob('./*'))
    
    # Remove removed files/directories
    #subprocess.run(['git', 'rm -r'] + glob.glob('./*'))
   
    # Stage all changes
    subprocess.run(['git', 'add', '-A', '.'])
 
    # Commit the version of the code with message taken from directory name
    subprocess.run(['git', 'commit', '-m', subs[idx]])
    #print('Commit -m "'+subs[idx]+'"')
    
    # Push the commit
    subprocess.run(['git', 'push'])
   
    # Go back to original directory 
    os.chdir('..')

    # Test for a few folders
    #if (subs_id[idx] == 1):
    #    break


print('Finished uploading all versions to git.')

