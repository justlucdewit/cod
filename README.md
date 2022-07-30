<div align="center">
    <img
        alt="Cod"
        src="assets/cod-logo.png"
        width="150">
</div>

<br />

# The Cod Compiler
Cod is an opensource concatenative stack-based general purpose programming language that compiles to C 

<br />

# Installation
You can download the latest version from your operating system on [The cod website](https://codlang.com)

Once downloaded you can put the executable in your system PATH and then it should work

<br />

# Usage
`cod someScript.cod -o someScript.c`

for More help, run `cod --help`

Make sure to download the [standard library](https://github.com/justlucdewit/cod/tree/master/stdlib) in your project root

<br />

# Language
Hello World:

``` lua
"Hello World!" prints
```

Fizzbuzz:

```lua
-- Fizzbuzz example written in Cod
include "std/math.cod"
include "std/io.cod"
include "std/stack.cod"

alias max_loop_count 40

-- Subroutine to check if number is divisible by another number
subroutine divisible_by {
    % 0 ==
}

-- Counter
1

-- Start the loop
true

while {
    pop
    
    -- Check if divisible by 3
    dup 3 divisible_by if {
        "fizz" prints
    } pop

    -- Check if divisible by 5
    dup 5 divisible_by if {
        "buzz" prints
    } pop
    
    -- Check if divisible by neither
    dup 3 divisible_by ! swap dup cycle3 swap 5 divisible_by ! & if {
        swap printn swap
    } pop

    -- Print newline
    10 printc pop

    -- Increment count
    1 +

    -- Determain if loop again
    dup max_loop_count <=
}
```
