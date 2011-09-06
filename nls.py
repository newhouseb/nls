from subprocess import Popen, PIPE
import sys

# USAGE for nls.py
# NOTE: I alias 'nls' to 'python nls.py'
#
# nls - prints the equivalent of ls, with notes for each file if it exists
# nls bootstrap - initializes 
# nls [some file] [some description] - saves [some description] (quotes optional) 
#     as the note for [somefile]
#
# If I had used dictionary comprehensions, this would probably be a much
# shorter script, but I wanted to keep it 2.6 compatible.  There are probably
# a lot of other things you could do as well, so fork github:newhouseb/nls and do them!

# Do the commap we're supposed to wrap
files = Popen(["ls"], stdout=PIPE).communicate()[0].splitlines()

# Open the file, don't freak out if it doesn't exist
notes = {}
try:
    nls_file = open('.nls').read().splitlines()
except IOError:
    nls_file = []

# Parse the file into a dict mapping file to note
for entry in nls_file:
    file, note = entry.split(':', 1)
    notes[file] = note

# If there was an argument then we're changing the .nls file
if len(sys.argv) > 1:
    # Put all unseen files as blank entries in the .nls file
    if len(sys.argv) == 2 and sys.argv[1] == 'bootstrap':
        for file in files:
            if file not in notes:
                notes[file] = ''
    # Add the single file
    elif sys.argv[1] in files:
        notes[sys.argv[1]] = ' '.join(sys.argv[2:])
    # Commit changes
    open('.nls','w').write(
        '\n'.join([file + ': ' + note for file,note in notes.iteritems()]))

# Print ls wth notation
for file in files:
    if file in notes:
        print '\033[1m' + file + ':\033[0m ' + notes[file].strip()
    else:
        print '\033[1m' + file + '\033[0m'
