from tkinter import *
import subprocess
from tkinter import ttk
import pandas as pd

class App:
    def __init__(self, root):
        # init window
        self.root = root
        self.root.title("Synthetic Data")
        self.root.geometry("600x400")


    # model configuration

        # model type
        Label(self.root, text="model_type").grid(row=0, column=0)
        self.model_type = ttk.Combobox(self.root, values=['fast', 'gan', 'cgan', 'wgan', 'llm'])
        self.model_type.grid(row=1, column=0)

        #synthetic similarity (temperature of the llm model affect the similarity of output, lower temp mean more similar)(0,1-0.5:low temp, 0.5-0.8:medium, 0.9 or above:high)
        Label(self.root, text="Synthetic similarity").grid(row=0, column=1)
        self.temperature = Scale(self.root, from_= 1.5, to= 0, orient=HORIZONTAL, resolution=0.01)
        self.temperature.set(1.5)# default to have low similarity for output
        self.temperature.grid(row=1, column=1)

         # start button
        self.start = Button(self.root, text='Start', command=self.check_condition).grid(sticky='s')        

    # check whether choose llm or not
    def check_condition(self):
        if self.model_type.get() == 'llm':
            self.new_window()

        #open a new window for llm
    def new_window(self):
        #llm window init
        self.top = Toplevel()
        self.top.title("llm-text-generation")
        self.top.geometry("600x400")
        Label(self.top, text="This is the llm text generation plugin").grid()

        # init text variable
        self.requirement = StringVar()
        self.example = StringVar()
        self.region = StringVar()

        # ask for requirement, example and region of the column
        Label(self.top, text="Requirement of the data: ").grid()
        Entry(self.top, textvariable=self.requirement).grid()
        Label(self.top, text="Example of the data: ").grid()
        Entry(self.top, textvariable=self.example).grid()
        Label(self.top, text="Region of the data: (Only needed if the data is related to a region like name)").grid()
        Entry(self.top, textvariable=self.region).grid()

        # ask for llm model type
        Label(self.top, text="Please choose you llm: ").grid()
        self.llm_type = ttk.Combobox(self.top, values=['gemma-3-4b'])
        self.llm_type.grid()
        self.prompt = Text(self.top, width=60, height=20)
        self.column_name = "name"

        #run the python file
        def generate():
            script_path = 'generate.py'
            llm = "./" + self.llm_type.get()
            result = subprocess.check_output(["python", script_path, llm, self.prompt.get("1.0", END), str(self.temperature.get())], text=True, stderr=subprocess.STDOUT) #all input must be a string
            print(result)

        def show_prompt():
            self.prompt.delete('1.0', END)
            self.prompt.insert(END, f"Could you generate me 10 random full {self.region.get()} {self.column_name} in English? Here is the requirement: {self.requirement.get()}. And here is the example: {self.example.get()}. Please present only the output as a string, enclosed in parentheses ( and ), with the name separated by semi colon." )
            self.prompt.grid()
            Button(self.top, text="Start", command=generate).grid(row=9, column=1)


        #start button (generation)
        Button(self.top, text="Show prompt", command=show_prompt).grid()
        
   
        


root = Tk()
App(root)

root.mainloop()