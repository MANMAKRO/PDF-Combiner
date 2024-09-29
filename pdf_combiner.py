import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os

# List to store full file paths
pdf_file_paths = []

def combine_pdfs(output_path):
    merger = PdfMerger()
    for pdf in pdf_file_paths:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def add_files():
    files = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*")),
    )
    for file in files:
        file_name = os.path.basename(file)
        if file not in pdf_file_paths:
            pdf_file_paths.append(file)
            listbox.insert(tk.END, file_name)
        else:
            messagebox.showinfo("Duplicate File", f"'{file_name}' is already added.")

def remove_selected():
    selected_indices = listbox.curselection()
    for index in selected_indices[::-1]:
        listbox.delete(index)
        del pdf_file_paths[index]

def move_up():
    selected_indices = listbox.curselection()
    for index in selected_indices:
        if index == 0:
            continue
        file_name = listbox.get(index)
        file_path = pdf_file_paths[index]
        
        # Swap in listbox
        listbox.delete(index)
        listbox.insert(index - 1, file_name)
        listbox.selection_set(index - 1)
        
        # Swap in file paths
        pdf_file_paths.pop(index)
        pdf_file_paths.insert(index - 1, file_path)

def move_down():
    selected_indices = listbox.curselection()
    for index in selected_indices[::-1]:
        if index == listbox.size() - 1:
            continue
        file_name = listbox.get(index)
        file_path = pdf_file_paths[index]
        
        # Swap in listbox
        listbox.delete(index)
        listbox.insert(index + 1, file_name)
        listbox.selection_set(index + 1)
        
        # Swap in file paths
        pdf_file_paths.pop(index)
        pdf_file_paths.insert(index + 1, file_path)

def combine_files():
    if len(pdf_file_paths) < 2:
        messagebox.showwarning("Warning", "Please add at least two PDF files.")
        return
    
    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*")),
    )
    
    if not output_path:
        return
    
    try:
        combine_pdfs(output_path)
        messagebox.showinfo("Success", f"PDF files combined and saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

app = tk.Tk()
app.title("PDF Combiner")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=50, height=15)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

button_frame = tk.Frame(app)
button_frame.pack(padx=10, pady=10)

add_button = tk.Button(button_frame, text="Add PDF Files", command=add_files)
add_button.grid(row=0, column=0, padx=5, pady=5)

remove_button = tk.Button(button_frame, text="Remove Selected", command=remove_selected)
remove_button.grid(row=0, column=1, padx=5, pady=5)

up_button = tk.Button(button_frame, text="Move Up", command=move_up)
up_button.grid(row=0, column=2, padx=5, pady=5)

down_button = tk.Button(button_frame, text="Move Down", command=move_down)
down_button.grid(row=0, column=3, padx=5, pady=5)

combine_button = tk.Button(button_frame, text="Combine PDFs", command=combine_files)
combine_button.grid(row=0, column=4, padx=5, pady=5)

app.mainloop()
