import tkinter as tk
from tkinter import ttk, filedialog
import re
import os
import git

def process_files(selected_files):
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()

        # Check if FBXResourceClass PC { exists
        if "FBXResourceClass PC {" not in content:
            continue

        # Check if ExportSceneHierarchy is already present and if it is enabled
        if "ExportSceneHierarchy" not in content or not export_scene_hierarchy_enabled.get():
            # If not present or disabled, add ExportSceneHierarchy 1 after FBXResourceClass PC {
            content = re.sub(r'FBXResourceClass PC {', r'FBXResourceClass PC {\n    ExportSceneHierarchy 1', content)

        # Check if GenerateBSP 1 is already present
        if generate_bsp_var.get() and "GenerateBSP 1" not in content:
            # If Generate BSP checkbox is checked and GenerateBSP 1 is not present,
            # add GenerateBSP 1 after Common TXOCommonClass
            content = re.sub(r'Common TXOCommonClass "([^"]*)" : "([^"]*)" {', 
                             r'Common TXOCommonClass "\1" : "\2" {\n    GenerateBSP 1', content)           
        
        with open(file, 'w') as f:
            f.write(content)

def delete_option(option):
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()

        if option in content:
            # Delete the option
            content = re.sub(option + r'\s*1?', '', content)
            status_label.config(text="Delete successfully!", foreground="black", background="orange", font=12)

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

        # Delete ExportSceneHierarchy 1
        content = re.sub(r'ExportSceneHierarchy 1\s*', '', content)

        # Delete GenerateBSP 1
        content = re.sub(r'GenerateBSP 1\s*', '', content)
        status_label.config(text="Delete successfully!", foreground="black", background="orange", font=12)

        with open(file, 'w') as f:
            f.write(content)

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("META files", "*.meta")])
    if files:
        file_listbox.delete(0, tk.END)
        for file in files:
            selected_files.append(file)
            filename = os.path.basename(file)  # Extract filename from full path
            file_listbox.insert(tk.END, filename)
        status_label.config(text="Files selected successfully!", foreground="white", background="green", font=12)
    else:
        status_label.config(text="No files selected.", foreground="white", background="red", font=12)

def process_selected():
    if not export_scene_hierarchy_enabled.get() and not generate_bsp_var.get():
        status_label.config(text="Please pick one option.", foreground="white", background="red", font=12)
        return

    if selected_files:
        process_files(selected_files)
        status_label.config(text="Enable successfully!", foreground="white", background="green", font=12)
    else:
        status_label.config(text="No files selected.", foreground="white", background="red", font=12)

def reset_selection():
    global selected_files
    selected_files = []
    file_listbox.delete(0, tk.END)
    status_label.config(text="Selection reset successfully!", foreground="black", background="orange", font=12)

def update_software():
    try:
        # Assuming the repository is in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_path = os.path.join(script_dir)
        
        # Alternatively, if your repository is located in a parent directory, you can use:
        # repo_path = os.path.abspath(os.path.join(script_dir)
        
        repo = git.Repo(repo_path)
        origin = repo.remote(name='origin')
        origin.pull()
        status_label.config(text="Software updated successfully!", foreground="black", background="orange", font=12)
    except Exception as e:
        error_message = f"Error updating software: {str(e)}"
        status_label.config(text=error_message, foreground="red", background="orange", font=12)
        print(error_message)  # Print the error for debugging purposes

# Create GUI
root = tk.Tk()
root.title("META File Manager for enfuison")

# Set window size
root.geometry("750x460")  # Width x Height

# Lock window size
root.resizable(False, False)  # Lock both x and y directions

# Import the tcl file
root.tk.call('source', 'forest-dark.tcl')
# Set the theme with the theme_use method
ttk.Style().theme_use('forest-dark')

photo = tk.PhotoImage(file='icon.png')
root.wm_iconphoto(False, photo)

selected_files = []

# Frame for file selection
file_frame = ttk.LabelFrame(root, text="Process")
file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")

select_button = ttk.Button(file_frame, text="Select META Files", command=select_files)
select_button.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="ew")

process_button = ttk.Button(file_frame, text="Process Selected", command=process_selected)
process_button.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

export_scene_hierarchy_enabled = tk.BooleanVar(value=False)
esh_checkbox = ttk.Checkbutton(file_frame, text="Enable Export Scene Hierarchy", variable=export_scene_hierarchy_enabled)
esh_checkbox.grid(row=2, column=0, padx=5, pady=(2, 0), sticky="ew")

generate_bsp_var = tk.BooleanVar(value=False)
generate_bsp_checkbox = ttk.Checkbutton(file_frame, text="Generate BSP", variable=generate_bsp_var)
generate_bsp_checkbox.grid(row=3, column=0, padx=5, pady=(2, 0), sticky="ew")

# Button for software update
update_button = ttk.Button(file_frame, text="Update tool", command=update_software)
update_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

# Frame for delete select
delete_frame = ttk.LabelFrame(root, text="Delete", padding=(0, 0, 0, 10))
delete_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="new")

delete_export_scene_hierarchy_button = ttk.Button(delete_frame, text="Delete Export Scene Hierarchy", command=delete_export_scene_hierarchy)
delete_export_scene_hierarchy_button.grid(row=5, column=0, padx=10, pady=(30, 20), sticky="nsew", rowspan=2)

delete_generate_bsp_button = ttk.Button(delete_frame, text="Delete Generate BSP", command=delete_generate_bsp)
delete_generate_bsp_button.grid(row=6, column=0, padx=10, pady=(30, 20), sticky="nsew", rowspan=3)

delete_all_options_button = ttk.Button(delete_frame, text="Delete All Options", command=delete_all_options)
delete_all_options_button.grid(row=7, column=0, padx=10, pady=(30, 20), sticky="nsew", rowspan=4)

# Frame for file list and status label
list_frame = ttk.Frame(root)
list_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew", rowspan=2)

file_listbox = tk.Listbox(list_frame, selectmode=tk.BROWSE, width=64, height=18)
file_listbox.grid(row=0, column=0, sticky="nsew")

reset_button = ttk.Button(list_frame, text="Reset Selection", command=reset_selection)
reset_button.grid(row=1, column=0, pady=6, sticky="nsew")

status_label = ttk.Label(list_frame, text="", foreground="green", anchor='center', background="gray28", wraplength=400)
status_label.grid(row=4, column=0, pady=6, sticky="nsew", rowspan=2)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

file_listbox.config(yscrollcommand=scrollbar.set)

# Configure grid rows and columns to expand
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()

