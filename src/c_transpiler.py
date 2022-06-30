from pathlib import Path
import json
import subprocess
import os
import time

def generate_rt_calls(program, indent_count=1):
    result = ""

    indent = "\t" * indent_count

    # Add the program as calls to the runtime
    for part in program:
        if part["type"] == "push":
            result += f"{indent}stack_push({part['value']});\n"

        elif part["type"] == "if":
            res = generate_rt_calls(part["contents"], indent_count + 1)
            result += f"{indent}if (stack_is_true()) {{\n"
            result += res
            result += f"{indent}}}\n"

        elif part["type"] == "while":
            res = generate_rt_calls(part["contents"], indent_count + 1)
            result += f"{indent}while (stack_is_true()) {{\n"
            result += res
            result += f"{indent}}}\n"

        elif part["type"] == "SRCall":
            result += f"{indent}CODSR_{part['uuid']}();\n"

        elif part["type"] == "push_str":
            result += f"{indent}stack_push_str(\"{part['value']}\");\n"

        elif part["type"] == "raw":
            result += f"{indent}{part['value']}\n"

        else:
            print('unknown program part type: ' + part["type"])
            exit(-1)

    return result

def generate_subroutines(subroutines):
    result = ""

    for subroutine_name in subroutines:
        subroutine = subroutines[subroutine_name]
        result += f"\n// Subroutine '{subroutine_name}'\nvoid CODSR_{subroutine['uuid']}() {{\n\tuint64_t a, b, c, d;\n"
        result += generate_rt_calls(subroutine['value'], 1)
        result += "}\n\n"

    return result

# Takes a list of program parts, and constructs
# the output program in C
def transpile_to_c(program, subroutines, input_path, args):
    # Create the output path for the c file
    output_path_base = input_path.replace(".cod", "")
    output_path = output_path_base + ".c"
    output_ast = output_path_base + ".ast.json"

    # Get start timestamp in ms
    start_time = int(round(time.time() * 1000))

    # Convert the program to beautified json and save it as the ast
    if args.debug:
        with open(output_ast, "w") as f:
            f.write(json.dumps(program, indent=4))

    # Get the runtime as a string
    runtime = open(f"{Path(__file__).resolve().parent}\\runtime.c", "r").read()
    result = runtime

    result += generate_subroutines(subroutines)
    result += "int main(char argc, char** argv) {\n\tsrand(time(0));\n\tstack = malloc(sizeof(uint64_t) * stack_capacity);\n\tuint64_t a, b, c, d;\n"
    result += generate_rt_calls(program)

    # End the main function
    result += "\treturn 0;\n}"

    # Write the result to the output file
    with open(output_path, "w") as f:
        f.write(result)

    # Compile the output_path using gcc
    # gcc -o output_path_base output_path
    output_path_base = output_path_base.replace("\\", "/")
    output_path_base = output_path_base.split("/")
    output_path_base.pop()
    output_path_base = "/".join(output_path_base)

    output_path_base = args.output if args.output else output_path_base + '/output'

    subprocess.call(["gcc", "-o", output_path_base, output_path])

    # Delete the output_path file
    if not args.debug:
        os.remove(output_path)

    # Print how long compilation took
    if args.time:
        end_time = int(round(time.time() * 1000))
        print(f"Compilation took {end_time - start_time} ms")

    # Run the compiled program
    if args.run:
        subprocess.call([output_path_base])


    

