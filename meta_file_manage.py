import tkinter as tk
from tkinter import ttk, filedialog
import re

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

        with open(file, 'w') as f:
            f.write(content)

def select_files():
    global selected_files
    files = filedialog.askopenfilenames(filetypes=[("META files", "*.meta")])
    if files:
        selected_files = files
        file_listbox.delete(0, tk.END)
        for file in selected_files:
            file_listbox.insert(tk.END, file)
        status_label.config(text="Files selected successfully!", foreground="green")
    else:
        status_label.config(text="No files selected.", foreground="red")

def process_selected():
    if selected_files:
        process_files()
        status_label.config(text="Files processed successfully!", foreground="green")
    else:
        status_label.config(text="No files selected.", foreground="red")

def toggle_dark_mode():
    # You can customize dark mode colors here
    dark_mode = dark_mode_var.get()
    if dark_mode:
        root.config(bg="#333333")
        for widget in root.winfo_children():
            if isinstance(widget, (ttk.Frame, ttk.Label, ttk.Button)):
                widget.config(style="Dark.TButton")
    else:
        root.config(bg="white")
        for widget in root.winfo_children():
            if isinstance(widget, (ttk.Frame, ttk.Label, ttk.Button)):
                widget.config(style="TButton")

# Create GUI
root = tk.Tk()
root.title("META File Manager for enfuison")

photo = tk.PhotoImage(file = 'icon.png')
root.wm_iconphoto(False, photo)

# Style
style = ttk.Style()
style.configure('TButton', foreground='blue', font=('Arial', 12))
style.configure('TLabel', font=('Arial', 12))
style.configure('Dark.TButton', foreground='white', background='#444444')

# Dark mode variable
dark_mode_var = tk.BooleanVar(value=False)

# Frame for file selection
file_frame = ttk.Frame(root)
file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

select_button = ttk.Button(file_frame, text="Select META Files", command=select_files)
select_button.grid(row=0, column=0, padx=10, pady=10)

process_button = ttk.Button(file_frame, text="Process Selected", command=process_selected)
process_button.grid(row=0, column=1, padx=10, pady=10)

dark_mode_button = ttk.Checkbutton(file_frame, text="Dark Mode", variable=dark_mode_var, command=toggle_dark_mode)
dark_mode_button.grid(row=0, column=2, padx=10, pady=10)

status_label = ttk.Label(file_frame, text="", foreground="green")
status_label.grid(row=0, column=3, padx=10, pady=10)

# Frame for file list
list_frame = ttk.Frame(root)
list_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

file_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, width=50, height=5)
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

file_listbox.config(yscrollcommand=scrollbar.set)

# Configure grid rows and columns to expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
