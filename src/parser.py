import os
import uuid

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
        print(f"Error: Expected a scope but got {words[i]}")
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
            scope_words.append(word)
        elif word == "}":
            indentation -= 1
            scope_words.append(word)
        else:
            scope_words.append(word)

    scope_words.pop()

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

include_files = []

# Gets list of words and returns a new list of words with the words
# of includes included
def resolve_includes(words, file_directory):
    # Get the words of the includes
    new_words = []
    max_words = len(words)
    i = 0

    while i < max_words:
        if words[i] == "include":
            include_str_rel =  words[i+1][1:-1]
            include_str = file_directory + include_str_rel

            # Make include_str into absolute path
            include_str = os.path.abspath(include_str)

            if include_str in include_files:
                print(f"Error: Circular include detected at {include_str_rel}")
                exit(-1)

            include_files.append(include_str)

            # If file doesnt exist
            if not os.path.isfile(include_str):
                print(f"Can not include file: '{include_str}'")
                exit(-1)

            include_content = open(include_str).read()
            include_words = lex_from_text(include_content, include_str)
            new_words += include_words

            i += 1
        else:
            new_words.append(words[i])

        i += 1

    return new_words

def lex_from_text(contents, file):
    # Remove the comments
    contents = remove_comments(contents)

    # Break the text into words
    words = []
    buffer = ""
    stringMode = False
    escapeMode = False
    for char in contents:
        # Handle strings
        if stringMode:
            if escapeMode:
                buffer += char
                escapeMode = False
            elif char == "\"":
                stringMode = False
                words.append(buffer + "\"")
                buffer = ""
            else:
                if char == "\\":
                    escapeMode = True
                else:
                    buffer += char

        elif char == "\"" and not stringMode:
            stringMode = True
            if buffer != "":
                words.append(buffer)
                buffer = ""
            buffer = "\""
        
        # Break words by space and newline
        elif char == " " or char == "\n":
            if buffer != "":
                words.append(buffer)
                buffer = ""

        else:
            buffer += char

    if buffer != "":
        words.append(buffer)

    # Remove empty strings
    words = [word for word in words if word != ""]

    if stringMode:
        print("Error: Unclosed string")
        exit(-1)

    # Get the directory of the file
    file = file.replace("\\", "/")
    file_directory = file.split("/")
    file_directory.pop()
    file_directory = "/".join(file_directory) + "/"

    words = resolve_includes(words, file_directory)

    return words

# Receives name of some file, reads code of that
# file and returns it as a list of program parts
def parse_from_file(file="test/test.cod"):
    # Get the contents of the file as string
    contents = open(file, "r").read()

    words = lex_from_text(contents, file)
    program = parse_from_words(words, root=True)
    
    return program

macros = {}

subroutines = {}

aliases = {
    "true": { "type": "push", "value": "1" },
    "false": { "type": "push", "value": "0" },
}

def parse_from_words(words, root=False):
    program = []

    custom_words = []

    builtin_words = [
        "argc",
        "argv",
        
        "parseInt"
    ]

    i = 0
    
    while i < len(words):
        word = words[i]

        if word.isdigit():
            program.append({ "type": "push", "value": int(word) })

        elif word in builtin_words:
            program.append({ "type": word })

        elif word.startswith("\""):
            program.append({ "type": "push_str", "value": word[1:-1] })

        elif word == "alias":
            alias_name = words[i + 1]
            alias_value = words[i + 2]

            if alias_name in custom_words:
                print(f"Error: custom word '{alias_name}' already exists")
                exit(-1)

            i += 2
            aliases[alias_name] = { "type": "alias", "value": alias_value }
            custom_words.append(alias_name)
        
        elif word == "macro":
            i += 1
            macro_name = words[i]
            scope_words, new_i = gather_scope(words, i)
            i = new_i - 1

            if macro_name in custom_words:
                print(f"Error: custom word '{macro_name}' already exists")
                exit(-1)

            macros[macro_name] = { "type": "macro", "value": scope_words }
            custom_words.append(macro_name)

        elif word == "subroutine":
            i += 1
            subroutine_name = words[i]
            scope_words, new_i = gather_scope(words, i)
            i = new_i - 1
            subroutine_uuid = uuid.uuid4()

            if subroutine_name in custom_words:
                print(f"Error: custom word '{subroutine_name}' already exists")
                exit(-1)

            subroutines[subroutine_name] = { "type": "subroutine", "uuid": str(subroutine_uuid).replace("-", "_"), "value": parse_from_words(scope_words, False) }
            custom_words.append(subroutine_name)
        
        elif word == "if":
            scope_words, new_i = gather_scope(words, i)
            i = new_i - 1
            program.append({ "type": "if", "contents": parse_from_words(scope_words) })
        
        elif word == "while":
            scope_words, new_i = gather_scope(words, i)
            i = new_i - 1
            program.append({ "type": "while", "contents": parse_from_words(scope_words) })
        
        elif word == "raw":
            i += 1
            raw_value = words[i]
            program.append({ "type": "raw", "value": raw_value[1:-1] })

        elif word in aliases:
            program.append(parse_from_words([ aliases[word]["value"] ])[0])
        
        elif word in macros:
            program += parse_from_words(macros[word]["value"])

        elif word in subroutines:
            subroutine = subroutines[word]
            program.append({ "type": "SRCall", "uuid": subroutine["uuid"], "value": word })
        
        else:
            print(f"Unknown word: {word}")
            exit(-1)

        i += 1

    if root:
        return program, subroutines
    else:
        return program