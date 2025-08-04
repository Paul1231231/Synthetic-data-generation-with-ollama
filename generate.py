from transformers import pipeline
import torch
import re
import pandas as pd
import sys



data = pd.read_csv('output.csv')
def synthetic_data_text(sample_size, model_path="./gemma-3-4b",prompt="", temperature=1):
    model = pipeline('text-generation', model=model_path, tokenizer=model_path, torch_dtype=torch.float32, temperature=temperature)
    torch.set_float32_matmul_precision('high')
    column = []
    # force llm to output in correct format (var1; var2; ...)
    while len(column) < sample_size:
        #asking
        generated_text = model(prompt, num_return_sequences=5)
        #extract the data list from the response
        for i in range(5): #num_return_sequences allow llm to have 5 different output each time
            match = re.findall(r"\(.*?\)", generated_text[i]['generated_text'])
            if match:
                output = match[-1] # get the string of data 
                modified_output = output.replace("(", "").replace(")", "") #delete the () in the string
                output_list = modified_output.split(";") # turn into python list
                column += output_list
    # make sure the new column match the sample size
    new_column = column[:sample_size]
    return new_column
        
        
# getting system input from tkinter window
model_path = sys.argv[1]
prompt = sys.argv[2]
temperature = sys.argv[3]
temperature = float(temperature)#turn it back to float number
new = synthetic_data_text(50, model_path=model_path, prompt=prompt, temperature=temperature)
print(new)