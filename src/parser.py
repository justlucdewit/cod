# Function to see if a string is a number
# returns boolean value if it is or not
def string_is_number(string):
    if string.isdigit():
        return True

# Function to gather all of the program parts
# that are within some scope
def gather_scope(words, i):
    i += 1

    if words[i] != "{":
        print("Expected a scope after if keyword")
        exit(-1)

    i += 1

    # Get the words inside of the scope
    scope_words = []
    indentation = 0
    while indentation != -1:
        word = words[i]
        i += 1
        if word == "{":
            indentation += 1
        elif word == "}":
            indentation -= 1
        else:
            scope_words.append(word)

    return scope_words, i

# Receives name of some file, reads code of that
# file and returns it as a list of program parts
def parse_from_file(file="test/test.lang"):
    # Get the contents of the file as string
    contents = open(file, "r").read()

    # Split the contents into lines
    lines = contents.split("\n")

    # Break the lines into words
    words = []
    for line in lines:
        words.append(line.split(" "))

    # Flatten the words list
    words = [item for sublist in words for item in sublist]

    # Remove empty strings
    words = [word for word in words if word != ""]
    
    program = parse_from_words(words)

    # print("Parsed program: ")
    # for part in program:
    #     print('\t', part)
    
    return program

def parse_from_words(words):
    program = []

    builtin_words = [
        "printn",
        "printc",
        "pop",
        "+",
        "-",
        "/",
        "*"
    ]

    i = 0
    while i < len(words):
        word = words[i]

        if word.isdigit():
            program.append({ "type": "push", "value": int(word) })

        elif word in builtin_words:
            program.append({ "type": word })
        
        elif word == "if":
            scope_words, new_i = gather_scope(words, i)
            i = new_i
            program.append({ "type": "if", "contents": parse_from_words(scope_words) })
        
        elif word == "while":
            scope_words, new_i = gather_scope(words, i)
            i = new_i
            program.append({ "type": "while", "contents": parse_from_words(scope_words) })
        
        else:
            print(f"Unknown word: {word}")
            exit(-1)

        i += 1

    return program