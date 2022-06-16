libs = {
    "math.cod": """
        macro increment {
            1 +
        }

        macro decrement {
            1 -
        }
    """,

    "cstr.cod": """
        -- Pops a pointer to a string from the stack
        -- and itterates over the string until it finds
        -- null terminator, printing out each character
        subroutine cstr_print {
            0
            swap dup cycle3 dup cycle3 + read8

            while {
                printc pop
                1 +
                swap dup cycle3 dup cycle3 + read8
            }
        }
    """
}