import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES, DND_TEXT
import pandas as pd
import subprocess
import json
import os

class DnDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Synthetic Text Data")

        # To store results
        self.text_columns = []
        self.requirement = []
        self.region = []

        # Create a label for dragging and dropping
        label = tk.Label(root, text="Drag and drop something here", width=40, height=10, bg="lightgray")
        label.pack(padx=20, pady=10)

        # Register the label as a drop target
        label.drop_target_register(DND_TEXT, DND_FILES)
        label.dnd_bind('<<Drop>>', self.drop)

        # Create an entry widget
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(padx=20, pady=10)

        # Create a Text widget for output
        self.listbox = tk.Listbox(root, selectmode = "multiple")
        self.listbox.pack(expand=True, fill ="both")

        select_button = tk.Button(root, text="Get Selected Items", command=self.get_select_items)
        select_button.pack(padx=20, pady=10)


    def drop(self, event):
        file_path = event.data
        self.entry.delete(0, tk.END)  # Clear the entry
        self.entry.insert(0, file_path)  # Insert dropped data

        # Process the file and capture results
        self.text_columns, self.requirement, self.region = self.process_file(file_path)
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END) 
        for index, item in enumerate(self.text_columns):
            self.listbox.insert(tk.END, item)
            self.listbox.itemconfig(index, bg="yellow" if index % 2 == 0 else "cyan")
    
    def get_select_items(self):
        select_indices = self.listbox.curselection()
        select_items = [self.listbox.get(i) for i in select_indices]
        select_items_requirement = [self.requirement[i] for i in select_indices]
        select_items_region = [self.region[i] for i in select_indices]
        lists_json = [json.dumps(lst) for lst in (select_items, select_items_requirement, select_items_region)]
        script_path = "text_gen.py"
        result = subprocess.check_output(["python", script_path, *lists_json], text=True, stderr=subprocess.STDOUT)

        
    def process_file(self, file_path):
            data = pd.read_csv(file_path)
            text_columns = data.select_dtypes(include=['object']).columns.tolist()
            script_path = "testing.py"
            
            # Save the DataFrame to a temporary CSV file
            temp_file_path = "temp_data.csv"
            data.to_csv(temp_file_path, index=False)
            
            # Call the external script
            result = subprocess.check_output(["python", script_path, temp_file_path], text=True, stderr=subprocess.STDOUT)
            output_dict = json.loads(result)
            requirement = output_dict['requirement']
            region = output_dict['region']
            
            # Clean up the temporary file
            os.remove(temp_file_path)
            
            return text_columns, requirement, region

    def clear_entry(self):
        self.entry.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)



# Create the main window
root = TkinterDnD.Tk()
root.title("Synthetic text data")
app = DnDApp(root)


# Start the main loop
root.mainloop()