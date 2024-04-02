import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.font as tkFont
import re
import os

def process_files(selected_files):
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()

        if "FBXResourceClass PC {" not in content:
            continue

        if "ExportSceneHierarchy" not in content or not export_scene_hierarchy_enabled.get():
            content = re.sub(r'FBXResourceClass PC {', r'FBXResourceClass PC {\n    ExportSceneHierarchy 1', content)

        if generate_bsp_var.get() and "GenerateBSP 1" not in content:
            content = re.sub(r'Common TXOCommonClass "([^"]*)" : "([^"]*)" {', 
                             r'Common TXOCommonClass "\1" : "\2" {\n    GenerateBSP 1', content)           
        
        with open(file, 'w') as f:
            f.write(content)

def delete_option(option):
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()

        if option in content:
            content = re.sub(option + r'\s*1?', '', content)
            status_label.config(text="Delete successfully!", foreground="black", background="orange", font=label_font_size)

        with open(file, 'w') as f:
            f.write(content)

def delete_export_scene_hierarchy():
    delete_option("ExportSceneHierarchy")

def delete_generate_bsp():
    delete_option("GenerateBSP")

def delete_all_options():
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()

        content = re.sub(r'ExportSceneHierarchy 1\s*', '', content)
        content = re.sub(r'GenerateBSP 1\s*', '', content)
        status_label.config(text="Delete successfully!", foreground="black", background="orange", font=label_font_size)

        with open(file, 'w') as f:
            f.write(content)

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("META files", "*.meta")])
    if files:
        file_listbox.delete(0, tk.END)
        for file in files:
            selected_files.append(file)
            filename = os.path.basename(file)
            file_listbox.insert(tk.END, filename)
        status_label.config(text="Files selected successfully!", foreground="white", background="green", font=label_font_size)
    else:
        status_label.config(text="No files selected.", foreground="white", background="red", font=label_font_size)

def process_selected():
    if not export_scene_hierarchy_enabled.get() and not generate_bsp_var.get():
        status_label.config(text="Please pick one option.", foreground="white", background="red", font=label_font_size)
        return

    if selected_files:
        process_files(selected_files)
        status_label.config(text="Enable successfully!", foreground="white", background="green", font=label_font_size)
    else:
        status_label.config(text="No files selected.", foreground="white", background="red", font=label_font_size)

def reset_selection():
    global selected_files
    selected_files = []
    file_listbox.delete(0, tk.END)
    status_label.config(text="Clear!", foreground="black", background="orange", font=label_font_size)

root = tk.Tk()
root.title("META File Manager for enfuison ver 0.1")

# Import the tcl file
root.tk.call('source', 'forest-dark.tcl')
# Set the theme with the theme_use method
ttk.Style().theme_use('forest-dark')

root.iconbitmap("favicon.ico")

s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 18))
s.configure('my.TCheckbutton', font=('Helvetica', 18))
label_font_size = ('Helvetica', 18)

selected_files = []

file_frame = ttk.LabelFrame(root, text="Process", padding=(20, 10, 20, 10) )
file_frame.grid(row=0, column=0, padx=10, pady=(30, 10), sticky="nsew")
file_frame.columnconfigure(index=0, weight=1)

select_button = ttk.Button(file_frame, text="Select META Files", command=select_files, style='my.TButton')
select_button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

reset_button = ttk.Button(file_frame, text="Clear Selection", command=reset_selection, style='my.TButton')
reset_button.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

export_scene_hierarchy_enabled = tk.BooleanVar(value=False)
esh_checkbox = ttk.Checkbutton(file_frame, text="Enable Export Scene Hierarchy", variable=export_scene_hierarchy_enabled, style='my.TCheckbutton')
esh_checkbox.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

generate_bsp_var = tk.BooleanVar(value=False)
generate_bsp_checkbox = ttk.Checkbutton(file_frame, text="Generate BSP", variable=generate_bsp_var, style='my.TCheckbutton')
generate_bsp_checkbox.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

delete_frame = ttk.LabelFrame(root, text="Delete", padding=(20, 10, 20, 10) )
delete_frame.grid(row=1, column=0, padx=10, pady=(30, 10), sticky="nsew")
delete_frame.columnconfigure(index=0, weight=1)

delete_export_scene_hierarchy_button = ttk.Button(delete_frame, text="Delete Export Scene Hierarchy", command=delete_export_scene_hierarchy, style='my.TButton')
delete_export_scene_hierarchy_button.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

delete_generate_bsp_button = ttk.Button(delete_frame, text="Delete Generate BSP", command=delete_generate_bsp, style='my.TButton')
delete_generate_bsp_button.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

delete_all_options_button = ttk.Button(delete_frame, text="Delete All Options", command=delete_all_options, style='my.TButton')
delete_all_options_button.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

list_frame = ttk.LabelFrame(root,text="List", padding=(20, 10, 20, 10))
list_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=2)
list_frame.columnconfigure(index=0, weight=1)

file_listbox = tk.Listbox(list_frame, selectmode=tk.BROWSE, bd=2, width=64, height=24, font=tkFont.Font(family="Helvetica", size=14))
file_listbox.grid(row=0, column=0, sticky="nsew")

process_button = ttk.Button(list_frame, text="Process Selected", command=process_selected, style='my.TButton')
process_button.grid(row=1, column=0, pady=6, sticky="nsew")

status_label = ttk.Label(list_frame, text="", foreground="green", anchor='center', background="gray28", wraplength=400)
status_label.grid(row=4, column=0, pady=6, sticky="nsew", rowspan=2)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

file_listbox.config(yscrollcommand=scrollbar.set)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
