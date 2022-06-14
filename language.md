# Cod language
The following cod language explains how the cod programming language and its syntax works:

## Stack
Numbers in Cod mean that that number will be pushed to the stack, while you can pop the top value off the stack using the `pop` keyword.

```lua
1 2 3 pop 4 5
```

Would result into the stack `[5, 4, 2, 1]` Where 5 is the top value of the stack.

You can also use `dup` to duplicate the top value of the stack, use `swap` to swap the top 2 values on the stack, and use `cycle3` to cycle the top 3 values of the stack (`a, b, c => b, c, a`).

## Comments
Comments in Cod are notated using `--` and are ignored by the compiler.

```lua
-- This will be ignored

54 printn pop -- Can also be put after line of code
```

## User output
In Cod there are 2 ways to output to the user, one way is to print the numeric value of the top value of the stack using `printn`, and the other way is by printing the ASCII character of the value on top of the stack using `printc`

```lua
65 printc
66 printc
123 printn
```

Would print the text "AB123" to the terminal.

## Strings
Cod can also push strings to the stack, this is done by using double quote characters and will push 2 numbers to the stack representing the address of where the string lives, and the length of that string. This string could then be printed using the word `prints` (print string). `Hello` Would be equal to `push <some adress> push 5`

```lua
"Hello World!" prints
```

## Math
Cod also has some special words to do math operations on the stack. For example - which pops the top 2 values off the stack and subtracts them, and pushes the result back onto the stack.

The following code would print 3 to the terminal
```
5 2 - printn
```

This uses [Reverse Polish Notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation) (RPN for short) since the language is stack based and thus executes the instructions word for word on the stack.

Cod also has other math operations like `+`, `*`, `/`, `<`, `>`, `<=`, `>=`, `==`, `!=` The last 6 are used to compare 2 values which leaves a boolean value on the stack represented like 0 (false) or 1 (true)

# Aliases, Macros, Subroutines
Cod also has special features to create custom words in the form of macros, aliases, and subroutines.

An alias is a word that simply aliases another single word. For example if you wanted to use 'plus' instead of '+' you could use
an alias, but you can also use it as constants as you can set a macro equal to a numeric value

```lua
-- Create alias 'plus' for the plus operator
alias plus +

-- Create alias 'age' for the age of the user
alias age 6
```

Macros are similair to aliases, except they allow to create a custom word representing **multiple** other words. For example:

```lua
macro increment {
    1 +
}

65 increment
```

This would print 66 to the terminal since 65 is pushed, then 1 is pushed and then they are added together.

Subroutines work in practice exactly the same as macros, except they compile to a C function so the code does not all get copy pasted when used multiple times creating a lot of unnecessary repeated code in the final C file.

This is good to be used when you have a decently sized macro that is used multiple times.

```lua
subroutine count_down_from {
    while {
        -- Print the value
        printn

        -- Print new line char
        10 printc

        -- decrement
        1 -
    }
}

5 count_down_from
9 count_down_from
```

## Control flow
Cod currently has 2 forms of control flow: if statements, and while loops. Both of which use {} to notate their scope. Its also recommended to use indentations just like in non concatenative languages.

If statements look at the top value of the stack, and if its truthy, it will execute the code in the scope, and else it will skip it.

```lua
5
if {
    printn
}

0
if {
    printn
}
```

Will print 5 because 5 is truthy, but will not print 0 because 0 is falsey.

While loops work the same way as if statements, however instead of checking the top value of the stack once, it will do it repeadetly until its falsey, and thus running the scope multiple times.

```lua
5

while {
    -- Print the number
    printn

    -- Decrement
    1 -
}
```

Will print `54321`

## Heap memory
Instead of storing everything on the stack (which would be really messy). Cod gives you the ability to store data on the heap. This is done by using write8 and read8 to read/write to certain memory addresses, and malloc/realloc/free to manage buffers.

To create a buffer, you can use the `malloc` keyword wich pops a value from the stack used as the size of the buffer, and then pushes back the address of the buffer.

To resize the buffer, one could use the `realloc` word, which pops a value from the stack used as the new size of the buffer, another one for the buffer itself, and then pushes back the address of the buffer

One could free a buffer by using the `free` keyword, which pops a value from the stack used as the address of the buffer to be freed.

```lua
-- Create a buffer of 64 bytes
64 malloc

-- Grow buffer to 128 bytes
128 realloc

-- Free buffer
free
```

The above example reserves a buffer of 64 bytes, then grows it to 128 bytes, and then frees the buffer again.

One could write to a buffer by pushing the address of the buffer to the stack, and then the value to write to the buffer, and then using `write8` to write the value to the buffer as one byte.

`read8` is then used to get that value back again, it pops a value of the stack which will be used as the address of where to read. Then pushes back the value read from the buffer.

```lua
3 malloc

-- Write 'ABC' to the buffer
dup 0 +   -- get buffer address with offset of 0
65 write8 -- write 'A' to buffer at offset 0
pop       -- pop the buffer + offset address

dup 1 +
66 write8
pop

dup 1 +
67 write8
pop

-- Write 2nd character
dup 1 + read8
printn pop

-- Free the memory again
free
```

The code above reserves memory of 3 bytes, writes 'ABC' into that memory, and then prints the 2nd character of the string.