from llm_sdk.llm_sdk import Small_LLM_Model

def main():
    model: Small_LLM_Model = Small_LLM_Model()

    res: str = model.get_path_to_vocab_file()

    print(res)

if __name__ == "__main__":
    main()