from ollama import generate, chat
import sys
import pandas as pd
from pydantic import BaseModel
import json

class Column(BaseModel):
    name: str
    description: str
    country: str

class ColumnList(BaseModel):
    columns: list[Column]

#user input should be a pandas dataframe

#user_input = sys.argv[1]
#user_input = pd.read_csv(user_input)
user_input = pd.read_csv('temp_data.csv')
text_columns = user_input.select_dtypes(include=['object']).columns.tolist()
head = user_input.head(10).to_string()
content = "Here is the head of a dataset: " + head + "Please provide a detail description of the requirement of the all column base of the whole data for generating synthetic data and follow the format strictly Also, identify which country is the data from "
response = chat(
messages=[
    {
    'role': 'user',
    'content': content,
    }
],
model='llama3',
format=ColumnList.model_json_schema(),
)
response = ColumnList.model_validate_json(response.message.content)
requirementlist = []
for i in range(len(text_columns)):
    requirementlist.append(response.columns[i].description)
regionlist = []
for i in range(len(text_columns)):
    regionlist.append(response.columns[i].country)
output_dict = {
    "requirement": requirementlist,
    "region": regionlist
}
print(json.dumps(output_dict))
