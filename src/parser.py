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

# Receives codefile as string and removes
# all comments from it, comments are notated
# with --, and can be put after code on the same line
def remove_comments(code):
    # Split the code into lines
    lines = code.split("\n")

    # Remove all comments
    for i in range(len(lines)):
        lines[i] = lines[i].split("--")[0]

    # Remove all empty strings
    lines = [line for line in lines if line != ""]

    # Join the lines back together
    code = " ".join(lines)

    return code

# Receives name of some file, reads code of that
# file and returns it as a list of program parts
def parse_from_file(file="test/test.lang"):
    # Get the contents of the file as string
    contents = open(file, "r").read()

    # Remove the comments
    contents = remove_comments(contents)

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

macros = {}

def parse_from_words(words):
    program = []

    custom_words = []

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

        elif word == "alias":
            macro_name = words[i + 1]
            macro_value = words[i + 2]

            if macro_name in custom_words:
                print(f"Error: custom word '{macro_name}' already exists")
                exit(-1)

            i += 2
            macros[macro_name] = { "type": "maco", "value": macro_value }
            custom_words.append(macro_name)
        
        elif word == "if":
            scope_words, new_i = gather_scope(words, i)
            i = new_i
            program.append({ "type": "if", "contents": parse_from_words(scope_words) })
        
        elif word == "while":
            scope_words, new_i = gather_scope(words, i)
            i = new_i
            program.append({ "type": "while", "contents": parse_from_words(scope_words) })
        
        elif word in macros:
            program.append(parse_from_words([ macros[word]["value"] ])[0])
        
        else:
            print(f"Unknown word: {word}")
            exit(-1)

        i += 1

    return program