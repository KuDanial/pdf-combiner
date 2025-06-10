import customtkinter as ctk
from tkinter import filedialog, messagebox, Listbox
from PyPDF2 import PdfMerger
import os
from tkinter import ttk

class PDFCombinerApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("PDF Combiner")
        self.window.geometry("800x500")
        self.window.resizable(False, False)  # Prevent window resizing
        
        # Set initial theme
        self.is_dark_mode = True
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title and theme toggle frame
        self.title_frame = ctk.CTkFrame(self.main_frame)
        self.title_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="PDF Combiner", 
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(side="left", padx=20)
        
        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            self.title_frame,
            text="🌙 Dark Mode",
            width=120,
            command=self.toggle_theme
        )
        self.theme_button.pack(side="right", padx=20)
        
        # Instructions label
        self.instructions_label = ctk.CTkLabel(
            self.main_frame,
            text="Drag and drop files to reorder them",
            font=("Helvetica", 12)
        )
        self.instructions_label.pack(pady=5)
        
        # Create a frame for the listbox
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Create listbox with scrollbar
        self.file_list = Listbox(
            self.list_frame,
            selectmode="single",
            bg="#2b2b2b",
            fg="white",
            selectbackground="#1f538d",
            font=("Helvetica", 12),
            height=15
        )
        self.file_list.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.file_list.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.file_list.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind drag and drop events
        self.file_list.bind('<Button-1>', self.on_click)
        self.file_list.bind('<B1-Motion>', self.on_drag)
        self.file_list.bind('<ButtonRelease-1>', self.on_release)
        
        # Buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10, fill="x")
        
        # Add PDF button
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="Add PDF",
            command=self.add_pdf
        )
        self.add_button.pack(side="left", padx=5)
        
        # Combine button
        self.combine_button = ctk.CTkButton(
            self.button_frame,
            text="Combine PDFs",
            command=self.combine_pdfs
        )
        self.combine_button.pack(side="left", padx=5)
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear List",
            command=self.clear_list
        )
        self.clear_button.pack(side="left", padx=5)
        
        # Move Up button
        self.move_up_button = ctk.CTkButton(
            self.button_frame,
            text="Move Up",
            command=self.move_up
        )
        self.move_up_button.pack(side="left", padx=5)
        
        # Move Down button
        self.move_down_button = ctk.CTkButton(
            self.button_frame,
            text="Move Down",
            command=self.move_down
        )
        self.move_down_button.pack(side="left", padx=5)
        
        # Store PDF files
        self.pdf_files = []
        self.drag_data = {"item": None, "index": None}
        
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="🌙 Dark Mode")
            self.file_list.configure(bg="#2b2b2b", fg="white", selectbackground="#1f538d")
        else:
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="☀️ Light Mode")
            self.file_list.configure(bg="white", fg="black", selectbackground="#0078d7")
        
    def on_click(self, event):
        # Get the index of the clicked item
        index = self.file_list.nearest(event.y)
        self.drag_data["item"] = self.file_list.get(index)
        self.drag_data["index"] = index
        
    def on_drag(self, event):
        # Get the index of the item being dragged over
        index = self.file_list.nearest(event.y)
        if index != self.drag_data["index"]:
            # Move the item in the listbox
            self.file_list.delete(self.drag_data["index"])
            self.file_list.insert(index, self.drag_data["item"])
            # Move the item in the pdf_files list
            item = self.pdf_files.pop(self.drag_data["index"])
            self.pdf_files.insert(index, item)
            self.drag_data["index"] = index
            
    def on_release(self, event):
        self.drag_data["item"] = None
        self.drag_data["index"] = None
        
    def move_up(self):
        selected = self.file_list.curselection()
        if selected and selected[0] > 0:
            index = selected[0]
            # Move in listbox
            item = self.file_list.get(index)
            self.file_list.delete(index)
            self.file_list.insert(index - 1, item)
            self.file_list.selection_set(index - 1)
            # Move in pdf_files
            item = self.pdf_files.pop(index)
            self.pdf_files.insert(index - 1, item)
            
    def move_down(self):
        selected = self.file_list.curselection()
        if selected and selected[0] < len(self.pdf_files) - 1:
            index = selected[0]
            # Move in listbox
            item = self.file_list.get(index)
            self.file_list.delete(index)
            self.file_list.insert(index + 1, item)
            self.file_list.selection_set(index + 1)
            # Move in pdf_files
            item = self.pdf_files.pop(index)
            self.pdf_files.insert(index + 1, item)
        
    def add_pdf(self):
        files = filedialog.askopenfilenames(
            filetypes=[("PDF files", "*.pdf")]
        )
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.file_list.insert("end", f"{os.path.basename(file)}")
    
    def combine_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("Warning", "Please add PDF files first!")
            return
            
        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if output_file:
            try:
                merger = PdfMerger()
                for pdf in self.pdf_files:
                    merger.append(pdf)
                merger.write(output_file)
                merger.close()
                messagebox.showinfo("Success", "PDFs combined successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_list(self):
        self.pdf_files.clear()
        self.file_list.delete(0, "end")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PDFCombinerApp()
    app.run()
