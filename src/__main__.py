from llm_sdk import Small_LLM_Model
import json
import torch
from pydantic import BaseModel, Field, model_validator
from typing import Dict, List
from enum import Enum
import numpy as np
import torch.nn.functional as F

from src.vocabulary import searcher, valid_tokens_prompts

class TypeData(BaseModel):
    type: str

class Parameters(BaseModel):
    param_type: Dict[str, Dict[str, str]]

# TODO anadir el minimo de parametros para la funcion
class Function(BaseModel):
    name: str
    description: str
    parameters: dict[str, TypeData]
    returns: TypeData

    def __str__(self):    
        return (
            f"Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"Parameters: {self.parameters}\n"
            f"Returns: {self.returns}"
        )

class PromptDef(BaseModel):
    prompt: str

    def __str__(self):
        return (
            f"Prompt: {self.prompt}"
        )

def convert_pydantic_to_string(data_list: List[BaseModel]) -> List[str]:
    return_list: List[str] = []
    for data in data_list:
        return_list.append(data.prompt)

    return return_list

def softmax(logits):  
    exp_values = np.exp(logits - np.max(logits)) 

    probabilities = exp_values / np.sum(exp_values)
    return probabilities

def valid_tokens_numbers(json_file):
    """
        Give every single token to create every function from scratch in a matrix
    """
    valid_tokens = list()
    numbers = "0123456789"
    for token, token_id in json_file.items():
        if token in numbers:
            valid_tokens.append(token_id)

    return valid_tokens

def get_token_value(json_file, token_id):
    for token, token_id_json in json_file.items():
        if token_id == token_id_json:
            print(token)

def main():
    
    # encode
    # convert to list of integers
    # get the logits from this list of integers
    # take the max logit
    # decode

    # mi problema aqui era que no sabia como transportar la informacion tensor -> list of integers -> list of float sin perder el valor
    # no sabia como pasarle los ID de los tokens, pero eso no es mi problema porque ya lo hace la funcion torch.argmax

    model: Small_LLM_Model = Small_LLM_Model()
    prompt = "Continua la secuencia: 0 - "

    path = model.get_path_to_vocab_file() # token - token id

    with open(path) as f:
        json_file = json.load(f)

    prompt_string = (
        "Actúa como un selector de funciones. Analiza la pregunta del usuario, "
        "elige la función correcta de la lista inferior y extrae sus parámetros. "
        "Responde ÚNICAMENTE con un objeto JSON plano que tenga esta estructura exacta, "
        "sin texto extra ni formato markdown: "
        '[{"prompt": "<prompt_name>", "name": "<function_name>", "parameters": {...}}] '
        "FUNCIONES DISPONIBLES: "
        "- fn_add_numbers: Suma dos números. Parámetros: a (number), b (number). "
        "- fn_greet: Saluda a una persona. Parámetros: name (string). "
        "- fn_reverse_string: Invierte un texto. Parámetros: s (string). "
        "- fn_get_square_root: Calcula la raíz cuadrada. Parámetros: a (number). "
        "- fn_substitute_string_with_regex: Reemplaza texto usando regex. Parámetros: "
        "source_string (string), regex (string), replacement (string). "
        'PREGUNTA: "What is the sum of 2 and 3?"'
    )

    
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

    prompt_vocabulary = valid_tokens_prompts(json_file, prompts)
    delimiter = '"prompt": "'
    res = '[{"prompt": "'

    respuesta_llm = []

    generated_text = "pepe"
    counter = 0
    while "]" not in generated_text and counter < 110:
        isPrompt = searcher(prompt_string, delimiter)
        
        tensor: torch.Tensor = model.encode(prompt_string)
        logits = model.get_logits_from_input_ids(tensor[0].tolist())


        # masking
        # token ids are indices in a vocabulary
        # the index 16 represents the value 1
        # logits_tensor[token_id] = float('-inf')
  
        if isPrompt:
            for i in range(len(logits)):
                if i not in prompt_vocabulary:
                    logits[i] = float('-inf')

        logits_tensor = torch.Tensor(logits)

        probabilities = F.softmax(logits_tensor, dim=-1)

        predicted_indices = torch.argmax(probabilities, dim=-1)
  
        generated_text = model.decode(predicted_indices)

        prompt_string = prompt_string + generated_text
        respuesta_llm.append(generated_text)
        counter += 1

    print("".join(respuesta_llm))

# https://www.youtube.com/watch?v=YCIkDF-0B-Q
# https://zeroentropy.dev/concepts/logits/
# https://juditacs.github.io/2018/12/27/masked-attention.html
# https://praveentn.live/learn/concepts/logit-bias-and-masking
# https://www.kapilsharma.dev/posts/logits-to-text/
# https://docs.pytorch.org/
# logit masking and why is importan https://pub.towardsai.net/your-llm-obeys-99-of-the-time-that-1-is-taking-down-production-a6ea1b6f00c1
# aplico logit masking pero la respuesta es siempre sum no what sum 


if __name__ == "__main__":
    main()
