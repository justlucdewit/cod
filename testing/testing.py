from pathlib import Path
import os

def execute_test(test_path):
    
    # run command
    os.system(f"python ./src/compiler.py ./testing/tests/{test_path}.cod")

execute_test("t001")