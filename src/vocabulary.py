def valid_tokens_functionsAndPrompts(json_file, sentence_definition):
    """
        Give every single token to create every function from scratch in a matrix
    """
    matrix = []
    for function in sentence_definition:
        matrix.append(set([(key, value) for key, value in json_file.items() if key in function]))

    return list(enumerate(matrix))


def filter_valid_tokens(vocabulary, current: str, sentence_definition): # list of functions enumerated 
    """
        Given the current state of the string filter only valid set of tokens

        The enumerated sentence_definition is equal to the enumerated vocabulary 
        0 name_1    0 set_of_tokens of function name_1
        1 ...       1 ...
        2 ...       2 ...
        3 ...       3 ...

        if the current string can be found within the function name then:
            get only the set_of_tokens of the function_name enumerated
    """
    if current in sentence_definition:
        return None

    matrix = []
    for num, string in sentence_definition:
        # 'en string encontramos el siguiente texto'
        if string.find(current) == 0:
            for nb, set_of_tokens in vocabulary:
                if num == nb:
                    matrix.append((num, set_of_tokens))
                    break

    return matrix


def token_to_string(json_file, valid_tokens):
    """
        Return token to string ---> list of sets of tokens
    """
    matrix_str = []
    for valid_token in valid_tokens:
        matrix_str.append(set([key for key, value in json_file.items() if value in valid_token]))
    return matrix_str

def main():
    names = [
        "fn_add_numbers",
        "fn_greet",
        "fn_reverse_string",
        "fn_get_square_root",
        "fn_substitute_string_with_regex"
    ]

    prompts = [
        "What is the sum of 2 and 3?",
        "What is the sum of 265 and 345?",
        "Greet shrek",
        "Greet john",
        "Reverse the string 'hello'",
        "Reverse the string 'world'",
        "What is the square root of 16?",
        "Calculate the square root of 144",
        "Replace all numbers in \"Hello 34 I'm 233 years old\" with NUMBERS",
        "Replace all vowels in 'Programming is fun' with asterisks",
        "Substitute the word 'cat' with 'dog' in 'The cat sat on the mat with another cat'"
    ]


    enumerated_list = enumerate(names)
    current_str = "fn_greet"

    function_vocabulary = valid_tokens_functions(json_file, names)
    filtered = filter_valid_tokens(function_vocabulary, current_str, enumerated_list)

    print(filtered)

# Nunca pasar docstring 
def searcher(expr, delimiter):
    res = expr.find(delimiter, len(expr) - len(delimiter), len(expr))
    
    if res == -1: # Not found
        return False
    return True

def valid_tokens_prompts(json_file, prompt_definition):
    return [token_id for token, token_id in json_file.items() for prompt in prompt_definition if token in prompt]