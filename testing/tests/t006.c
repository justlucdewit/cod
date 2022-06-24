#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

uint64_t* stack;
size_t stack_ptr = 0;
size_t stack_capacity = 100;
char* execPath;

void stack_push(uint64_t value) {
    if (stack_ptr == stack_capacity) {
        stack_capacity *= 2;
        stack = realloc(stack, stack_capacity * sizeof(uint64_t));
    }
  
    stack[stack_ptr++] = value;
}

void stack_push_str(char* str) {
    size_t len = strlen(str);

    // Push pointer to the string
    stack_push((uint64_t)str);

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

char* c_read_file(const char* f_name, size_t* f_size) {
    char* full_file_name = malloc(sizeof(char) * strlen(execPath) + strlen(f_name));
    strcpy(full_file_name, execPath);
    strcat(full_file_name, f_name);
    
    char * buffer;
    size_t length;
    FILE * f = fopen(full_file_name, "rb");
    size_t read_length;

    if (f == NULL) {
        printf("Runtime error: Could not read file '%s'", full_file_name);
        exit(-1);
    }
    
    fseek(f, 0, SEEK_END);
    length = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    buffer = (char *)malloc(length + 1);
    
    if (length) {
        read_length = fread(buffer, 1, length, f);
    }
    
    fclose(f);
    
    buffer[length] = '\0';
    *f_size = length;
    
    return buffer;
}

void stack_file_read() {
    // Pop string length from stack
    size_t len = stack_pop();

    // Pop string address from stack
    char* address = (char*) stack_pop();

    size_t f_size;
    char* buffer = c_read_file(address, &f_size);

    printf(buffer);
}

void test(char* path) {
    int len = strlen(path);
    char* res = malloc(sizeof(char) * (len + 1));

    int i = 0;
    int lastSlashPos = 0;
    for (i = 0; i < len; i++) {
        char currChar = path[i];

        if (currChar == '/')
            lastSlashPos = i;
    }

    strncpy(res, path, lastSlashPos);
    res[lastSlashPos] = '/';
    execPath = res;
    printf(execPath);
}int main(char argc, char** argv) {
	test(argv[0]);
	srand(time(0));
	stack = malloc(sizeof(uint64_t) * stack_capacity);
	uint64_t a, b, c, d;
	stack_push(7);
	stack_push(2);
	a = stack_pop();
	stack_push(stack_pop() / a);
	stack_print_numeric();
	return 0;
}