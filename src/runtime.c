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

void stack_pop() {
  if (stack_ptr == 0) {
    return;
  }
  
  stack_ptr--;
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
