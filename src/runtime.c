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
    uint64_t* buffer = malloc(buffer_size);

    // Push the buffer address to the stack
    stack_push((uint64_t) buffer);
}

void stack_free() {
    if (stack_ptr == 0) {
        return;
    }
    
    // Pop buffer address from stack
    uint64_t buffer_address = stack_pop();

    // Free the buffer
    free((void*) buffer_address);
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

int main() {
    stack = malloc(sizeof(uint64_t) * stack_capacity);
    uint64_t a, b, c, d;
