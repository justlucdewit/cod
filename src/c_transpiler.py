from sys import exit

runtime = """
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

uint64_t* stack;
size_t stack_ptr = 0;
size_t stack_capacity = 100;

void stack_push(uint64_t value) {
    if (stack_ptr == stack_capacity) {
        stack_capacity *= 2;
        stack = realloc(stack, stack_capacity * sizeof(uint64_t));
    }
  
    stack[stack_ptr++] = value;
}

void stack_push_str(char* str) {
    uint64_t len = (uint64_t) strlen(str);

    // Push pointer to the string
    size_t str_ptr_as_number = (size_t) str;
    stack_push(str_ptr_as_number);

    // Push length
    stack_push(len);
}

uint64_t stack_pop() {
    if (stack_ptr == 0) {
        return 0;
    }
    
    stack_ptr--;
    return stack[stack_ptr];
}

void stack_malloc() {
    if (stack_ptr == 0) {
        stack_push(0);
        return;
    }
    
    // Pop buffer size from stack
    uint64_t buffer_size = stack_pop();

    // Reserve that much memory
    size_t buffer = (size_t) malloc(buffer_size);

    // Push the buffer address to the stack
    stack_push(buffer);
}

void stack_free() {
    if (stack_ptr == 0) {
        return;
    }
    
    // Pop buffer address from stack
    size_t buffer_address = stack_pop();

    // Free the buffer
    free((void*) buffer_address);
}

void stack_realloc() {
    if (stack_ptr == 0) {
        stack_push(0);
        return;
    }

    // Pop buffer size from stack
    uint64_t buffer_size = stack_pop();

    // Pop buffer address from stack
    size_t buffer_address = stack_pop();

    // Reallocate the buffer
    size_t buffer = (size_t) realloc((void*) buffer_address, buffer_size);
    
    // Push the buffer address to the stack
    stack_push(buffer);
}

// stack write8
void stack_write8() {
    if (stack_ptr == 0) {
        return;
    }

    // Pop value from stack
    uint64_t value = stack_pop();

    // Pop buffer address from stack
    size_t address = (size_t) stack_pop();

    // Write the value to the buffer
    *((size_t*) address) = value;
}

// stack read8
void stack_read8() {
    if (stack_ptr == 0) {
        return;
    }

    // Pop buffer address from stack
    size_t address = (size_t) stack_pop();

    // Read the value from the buffer
    size_t value = *((size_t*) address);

    // Push the value to the stack
    stack_push(value & 0xFF);
}

void stack_read64() {
    if (stack_ptr == 0) {
        return;
    }

    // Pop buffer address from stack
    size_t address = (size_t) stack_pop();

    // Read the value from the buffer
    size_t value = *((size_t*) address);

    // Push the value to the stack
    stack_push(value);
}

void stack_swap() {
    if (stack_ptr == 0) {
        return;
    }

    uint64_t value = stack_pop();
    uint64_t value2 = stack_pop();

    stack_push(value);
    stack_push(value2);
}

void stack_cycle3() {
    if (stack_ptr == 0) {
        return;
    }

    uint64_t a = stack_pop();
    uint64_t b = stack_pop();
    uint64_t c = stack_pop();

    stack_push(b);
    stack_push(a);
    stack_push(c);
}

void stack_dup() {
    if (stack_ptr == 0) {
        stack_push(0);
    }
    
    stack_push(stack[stack_ptr - 1]);
}

// Generate u64 random numbers
#define IMAX_BITS(m) ((m)/((m)%255+1) / 255%255*8 + 7-86/((m)%255+12))
#define RAND_MAX_WIDTH IMAX_BITS(RAND_MAX)
_Static_assert((RAND_MAX & (RAND_MAX + 1u)) == 0, "RAND_MAX not a Mersenne number");

void stack_random() {

    uint64_t r = 0;
    int i;
    for (i = 0; i < 64; i += RAND_MAX_WIDTH) {
        r <<= RAND_MAX_WIDTH;
        r ^= (unsigned) rand();
    }
    // Push a random u64 to the stack
    stack_push(rand());
}

void stack_print_numeric() {
    printf("%llu", stack[stack_ptr - 1]);
}

void stack_print_char() {
    printf("%c", (char)stack[stack_ptr - 1]);
}

void stack_print_str() {
    size_t len = stack_pop();
    size_t address = stack_pop();
    char* str = (char*) address;

    // Print str of length
    size_t i;
    for (i = 0; i < len; i++) {
        printf("%c", str[i]);
    }
}

void stack_cycle_n() {
    if (stack_ptr == 0) {
        return;
    }

    uint64_t n = stack_pop();
    
    // instead of cycling the top 3 values
    // cycle the top n values
    size_t buffer_count = 0;
    uint64_t* buffer = malloc(n * sizeof(uint64_t));

    size_t i;
    for (i = 0; i < n; i++) {
        buffer[buffer_count++] = stack_pop();
    }

    for (i = n - 1; i > 0; i--) {
        stack_push(buffer[i - 1]);
    }

    stack_push(buffer[n - 1]);

    free(buffer);
}

void stack_parse_int64() {
    if (stack_ptr == 0) {
        return;
    }

    // Pop string length from stack
    size_t len = stack_pop();

    // Pop string address from stack
    size_t address = stack_pop();

    char* str = (char*) address;

    // Parse the string
    int64_t value = strtoll(str, NULL, 10);

    // Push the value to the stack
    stack_push(value);
}

char stack_is_true() {
    return stack[stack_ptr - 1] != 0;
}

uint64_t* variable_buffer;
"""

from pathlib import Path
import json
import subprocess
import os
import time

def generate_rt_calls(program, variables, indent_count=1):
    result = ""

    indent = "\t" * indent_count

    # Add the program as calls to the runtime
    for part in program:
        if part["type"] == "push":
            result += f"{indent}stack_push({part['value']});\n"

        elif part["type"] == "if":
            res = generate_rt_calls(part["contents"], variables, indent_count + 1)
            result += f"{indent}if (stack_is_true()) {{\n"
            result += res
            result += f"{indent}}}\n"

        elif part["type"] == "while":
            res = generate_rt_calls(part["contents"], variables, indent_count + 1)
            result += f"{indent}while (stack_is_true()) {{\n"
            result += res
            result += f"{indent}}}\n"

        elif part["type"] == "SRCall":
            result += f"{indent}CODSR_{part['uuid']}();\n"

        elif part["type"] == "push_str":
            result += f"{indent}stack_push_str(\"{part['value']}\");\n"

        elif part["type"] == "raw":
            result += f"{indent}{part['value']}\n"

        elif part["type"] == "set_var":
            var_name = part["value"]
            var_index = 0
            for var in variables:
                if var["name"] == var_name:
                    var_index = var["index"]
                    break

            result += f"{indent}variable_buffer[{var_index}] = stack[stack_ptr - 1];\n"

        elif part["type"] == "get_var":
            var_name = part["value"]
            var_index = 0
            for var in variables:
                if var["name"] == var_name:
                    var_index = var["index"]
                    break
            result += f"{indent}stack_push(variable_buffer[{var_index}]);\n"

        else:
            print('unknown program part type: ' + part["type"])
            exit(-1)

    return result

def generate_subroutines(subroutines, variables):
    result = ""

    for subroutine_name in subroutines:
        subroutine = subroutines[subroutine_name]
        result += f"\n// Subroutine '{subroutine_name}'\nvoid CODSR_{subroutine['uuid']}() {{\n\tuint64_t a, b, c, d;\n"
        result += generate_rt_calls(subroutine['value'], variables, 1)
        result += "}\n\n"

    return result

# Takes a list of program parts, and constructs
# the output program in C
def transpile_to_c(program, subroutines, variables, input_path, args):
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
    result = runtime

    result += generate_subroutines(subroutines, variables)
    result += f"int main(char argc, char** argv) {{\n\tsrand(time(0));\n\tstack = malloc(sizeof(uint64_t) * stack_capacity);\n\tuint64_t a, b, c, d;\nvariable_buffer = calloc({len(variables)}, sizeof(uint64_t));\n"
    result += generate_rt_calls(program, variables)

    # End the main function
    result += "\treturn 0;\n}"

    # Write the result to the output file
    with open(output_path, "w") as f:
        f.write(result)

    # Print how long compilation took
    if args.time:
        end_time = int(round(time.time() * 1000))
        print(f"Compilation took {end_time - start_time} ms")

