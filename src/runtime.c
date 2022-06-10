#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

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

void stack_print_numeric() {
    printf("%llu", stack[stack_ptr - 1]);
}

void stack_print_char() {
    printf("%c", (char)stack[stack_ptr - 1]);
}

char stack_is_true() {
    return stack[stack_ptr - 1] != 0;
}
