import sys
import os
from c_transpiler import transpile_to_c
from parser import parse_from_file
import argparse

arg_parser = argparse.ArgumentParser(description='COD Compiler')

# List the possible program arguments
arg_parser.add_argument(
    '-v', '--version',
    help='Show the version of the COD compiler',
    action='store_true')

arg_parser.add_argument(
    '-d',
    '--debug',
    help='Outputs/keeps the .ast.json file and the .c file',
    action='store_true')

arg_parser.add_argument(
    '-r',
    '--run',
    help='Run the produced executable after compilation',
    action='store_true')

arg_parser.add_argument(
    'filename',
    nargs='?',
    help='File with the source code to compile/interpret',
    default='')

arg_parser.add_argument(
    "-o",
    "--output",
    metavar='<file>',
    help="Directs the output to a path/name of your choice")

arg_parser.add_argument(
    '-t', '--time',
    help='Time how long compilation took',
    action='store_true')

# Actually parse the arguments
args = arg_parser.parse_args(sys.argv[1:])

if args.version:
    print('COD Compiler v1.0')
    sys.exit(0)
else:
    if args.filename == '':
        print('No file specified. Use -h for help.')
        sys.exit(1)

    file_name = os.path.abspath(args.filename)
    program, subroutines = parse_from_file(file_name)
    transpile_to_c(program, subroutines, file_name, args)

# # Get the file name from the command line
# if len(sys.argv) > 1:

#     # Get the file name
#     file_name = sys.argv[1]

#     # Get the absolute path
#     file_name = os.path.abspath(file_name)

#     # Get the program parts
#     program, subroutines = parse_from_file(file_name)
#     transpile_to_c(program, subroutines, file_name)
# else:
#     print("CODLang transpiler V1")
