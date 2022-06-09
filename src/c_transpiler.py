from pathlib import Path
import json

def generate_rt_calls(program, indent_count=1):
    result = ""

    indent = "\t" * indent_count

    # Add the program as calls to the runtime
    for part in program:
        if part["type"] == "push":
            result += f"{indent}stack_push({part['value']});\n"
        elif part["type"] == "printn":
            result += f"{indent}stack_print_numeric();\n"
        elif part["type"] == "printc":
            result += f"{indent}stack_print_char();\n"
        elif part["type"] == "pop":
            result += f"{indent}stack_pop();\n"
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
        elif part["type"] in "-+*/":
            result += f"{indent}a = stack_pop();\n"
            result += f"{indent}stack_push(stack_pop() {part['type']} a);\n"

        else:
            print('unknown program part type: ' + part["type"])

    return result

# Takes a list of program parts, and constructs
# the output program in C
def transpile_to_c(program, input_path):
    # Create the output path for the c file
    output_path_base = input_path.replace(".cod", "")
    output_path = output_path_base + ".c"
    output_ast = output_path_base + ".ast.json"

    # Convert the program to beautified json and save it as the ast
    with open(output_ast, "w") as f:
        f.write(json.dumps(program, indent=4))

    # Get the runtime as a string
    runtime = open(f"{Path(__file__).resolve().parent}\\runtime.c", "r").read()
    result = runtime

    result += generate_rt_calls(program);

    # End the main function
    result += "\treturn 0;\n}"

    # Write the result to the output file
    with open(output_path, "w") as f:
        f.write(result)
