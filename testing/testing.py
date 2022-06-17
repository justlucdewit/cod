from pathlib import Path
import os

def execute_test(test_path, expect):
    
    # run command
    os.system(f"python ./src/compiler.py ./testing/tests/{test_path}.cod")

    # Run t001.exe and get output result and exit code
    output = os.popen(f"\"./testing/tests/output\"").read()
    result = '🔴' if output != expect else '🟢'
    error_msg = f"expected '{expect}' but got '{output}'" if output != expect else ''
    print(f'{result} test {test_path} {error_msg}')

    # Delete the executable
    os.system(f"del \"testing\\tests\\output.exe\"")

# List of all tests
execute_test("t001", expect="123")
execute_test("t002", expect="123")
execute_test("t003", expect="12")
execute_test("t004", expect="2")
execute_test("t005", expect="35")
execute_test("t006", expect="3")
execute_test("t007", expect="010")
execute_test("t008", expect="100")
execute_test("t009", expect="101")
execute_test("t010", expect="011")
execute_test("t011", expect="001")
execute_test("t012", expect="110")
execute_test("t013", expect="10")
execute_test("t014", expect="7")
execute_test("t015", expect="ABCDE")
execute_test("t016", expect="54")
execute_test("t017", expect="14")
execute_test("t018", expect="3")
execute_test("t019", expect="7 5")
execute_test("t020", expect="8")
execute_test("t021", expect="8")
execute_test("t022", expect="69")
execute_test("t023", expect="66")
execute_test("t024", expect="987654321")
execute_test("t025", expect="5\n4\n3\n2\n1\n")
execute_test("t026", expect="1\n2\n3\n4\n5\n")
execute_test("t027", expect="Hello World!")
execute_test("t028", expect="3")
execute_test("t029", expect="14")
execute_test("t030", expect="Hello World!")
execute_test("t031", expect="11")
execute_test("t032", expect="2s")
execute_test("t033", expect="./testing/tests/output")
execute_test("t034", expect="24")
execute_test("t035", expect="This is a test")
execute_test("t036", expect="39")
execute_test("t037", expect="7")