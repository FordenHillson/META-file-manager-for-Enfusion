import tkinter as tk
from tkinter import ttk, filedialog
import re
import os

selected_files = []

def process_files():
    global selected_files
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()

        # Check if FBXResourceClass PC { exists
        if "FBXResourceClass PC {" not in content:
            continue

        # Check if ExportSceneHierarchy is already present
        if "ExportSceneHierarchy" not in content:
            # If not present, add ExportSceneHierarchy 1 after FBXResourceClass PC {
            content = re.sub(r'FBXResourceClass PC {', r'FBXResourceClass PC {\n    ExportSceneHierarchy 1', content)

        # Check if GenerateBSP 1 is already present
        if generate_bsp_var.get() and "GenerateBSP 1" not in content:
            # If Generate BSP checkbox is checked and GenerateBSP 1 is not present,
            # add GenerateBSP 1 after Common TXOCommonClass
            content = re.sub(r'Common TXOCommonClass "([^"]*)" : "([^"]*)" {', 
                             r'Common TXOCommonClass "\1" : "\2" {\n    GenerateBSP 1', content)           
        

        with open(file, 'w') as f:
            f.write(content)

def delete_export_scene_hierarchy():
    global selected_files
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()

        # Check if ExportSceneHierarchy 1 exists
        if "ExportSceneHierarchy 1" in content:
            # Delete ExportSceneHierarchy 1
            content = re.sub(r'ExportSceneHierarchy 1\n?', '', content)
            status_label.config(text="Delete successfully!", foreground="black", background="orange",font=12)

        with open(file, 'w') as f:
            f.write(content)

def delete_generate_bsp():
    global selected_files
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()

        # Check if GenerateBSP 1 exists
        if "GenerateBSP 1" in content:
            # Delete GenerateBSP 1
            content = re.sub(r'GenerateBSP 1\n?', '', content)
            status_label.config(text="Delete successfully!", foreground="black", background="orange",font=12)

        with open(file, 'w') as f:
            f.write(content)

def delete_all_options():
    global selected_files
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()

        # Delete ExportSceneHierarchy 1
        content = re.sub(r'ExportSceneHierarchy 1\n?', '', content)

        # Delete GenerateBSP 1
        content = re.sub(r'GenerateBSP 1\n?', '', content)
        status_label.config(text="Delete successfully!", foreground="black", background="orange",font=12)

        with open(file, 'w') as f:
            f.write(content)

def select_files():
    global selected_files
    files = filedialog.askopenfilenames(filetypes=[("META files", "*.meta")])
    if files:
        selected_files = files
        file_listbox.delete(0, tk.END)
        for file in selected_files:
            filename = os.path.basename(file)  # Extract filename from full path
            file_listbox.insert(tk.END, filename)
        status_label.config(text="Files selected successfully!", foreground="white", background="green",font=12)
    else:
        status_label.config(text="No files selected.", foreground="white", background="red",font=12)

def process_selected():
    if selected_files:
        process_files()
        status_label.config(text="Enable successfully!", foreground="white", background="green",font=12)
    else:
        status_label.config(text="No files selected.", foreground="white", background="red",font=12)

# Create GUI
root = tk.Tk()
root.title("META File Manager for enfuison")

# Import the tcl file
root.tk.call('source', 'forest-dark.tcl')
# Set the theme with the theme_use method
ttk.Style().theme_use('forest-dark')

photo = tk.PhotoImage(file = 'icon.png')
root.wm_iconphoto(False, photo)

# Frame for file selection
file_frame = ttk.LabelFrame(root, text="Process")
file_frame.grid(row=0, column=0, padx=10, sticky="nsew", rowspan=1)
file_frame.columnconfigure(index=0, weight=1,)

select_button = ttk.Button(file_frame, text="Select META Files", command=select_files)
select_button.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")

process_button = ttk.Button(file_frame, text="Process Selected", command=process_selected)
process_button.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")

generate_bsp_var = tk.BooleanVar(value=False)

generate_bsp_checkbox = ttk.Checkbutton(file_frame, text="Generate BSP", variable=generate_bsp_var)
generate_bsp_checkbox.grid(row=2, column=0, padx=5, pady=(0, 0), sticky="ew")

# Frame for delete select
delete_frame = ttk.LabelFrame(root, text="Delete", padding=(0, 0, 0, 10))
delete_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew", rowspan=1)
delete_frame.columnconfigure(index=0, weight=10)

delete_export_scene_hierarchy_button = ttk.Button(delete_frame, text="Delete Export Scene Hierarchy", command=delete_export_scene_hierarchy)
delete_export_scene_hierarchy_button.grid(row=5, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=2)

delete_generate_bsp_button = ttk.Button(delete_frame, text="Delete Generate BSP", command=delete_generate_bsp)
delete_generate_bsp_button.grid(row=6, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)

delete_all_options_button = ttk.Button(delete_frame, text="Delete All Options", command=delete_all_options)
delete_all_options_button.grid(row=7, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=4)

# Frame for file list
list_frame = ttk.Frame(root)
list_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

file_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, width=52, height=12)
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

file_listbox.config(yscrollcommand=scrollbar.set)

status_label = ttk.Label(root, text="status", foreground="green")
status_label.grid(row=1, column=1, padx=10, pady=10)

# Configure grid rows and columns to expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
