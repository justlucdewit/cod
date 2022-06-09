import sys
import os
from c_transpiler import transpile_to_c
from parser import parse_from_file

# Get the file name from the command line
if len(sys.argv) > 1:

    # Get the file name
    file_name = sys.argv[1]

    # Get the absolute path
    file_name = os.path.abspath(file_name)

    # Get the program parts
    program = parse_from_file(file_name)
    transpile_to_c(program, file_name)
else:
    print("CODLang transpiler V1")