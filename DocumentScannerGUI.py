import os                                               #Directory/folder manipulation 
import shutil                                           #Copy file management 
from tkinter import *                                   #Primary GUI used 
from tkinter import filedialog, messagebox              #Tkinters messagebox uses
from algo.huffman import compress_file                  #Import some functions from huffman py in the algo folder 
from algo.sort import merge_sort                        #For sorting 
from cosmetic import WindowSet                          #Import WindowSet from the cosmetic folder for easier window config
from algo.naive_search import naive_search              # Use of naive search to find patterns
from cosmetic.dark_title_bar import *                   #Purely cosmetic function to make title bar dark to fit with the theme
import pdfplumber                                       #Convert pdf to text
from datetime import date                               #For current date 

#Today's Date for the label we use later 
today = date.today()
formatted_date = today.strftime("%m/%d/%Y")

#Global colors used + main font used 
color1 = '#343434'  # dark gray used for background for frames
color2 = '#29aff1'  # primary blue used throughout the app
color3 = '#4d4d4d'  # lighter gray used for entry background
color4 = '#ebebeb'  # cream color used for foreground
color5 = "#d50ce2"  # rose color 
color6 = "#101010"  # black
theFont1 = 'arial 10 bold'   #Primary font used
theFont2 = 'arial 15 bold'   #Primary font but BOLD

#Create Documents folder if it doesn't exist
DOCUMENTS_FOLDER = "Documents"
os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)

#Function to convert a pdf into text 
def convert_pdf_to_text(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf, open(output_path, 'w', encoding='utf-8') as f:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                f.write(text + '\n')

#Main class 
class DocumentScannerApp:
    #initilzie everything 
    def __init__(self, root):
        self.root = root
        self.root.title("Tuffy's Document Manager")
        self.current_action = None
        root.configure(bg='#101010')
        dark_title_bar(root)
        root.geometry("+0+0")
        WindowSet.setScreen(root, wRatio= .27, hRatio= .57) 
        
        self.create_main_menu()

    #GUI for main menu
    def create_main_menu(self):
        #Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

     
        #Label widget for header
        name_label = Label(self.root,
                        text="Tuffy's Document Scanner",
                        bg=color1, fg=color2,
                        font=theFont2)
        name_label.pack(pady=10)

        #Import button
        import_btn = Button(self.root, text="Import Files", command=self.import_files, width=30, height=2, 
                            bg=color2, fg=color6,
                            activebackground= "#6a6a6a", activeforeground=color4,
                            cursor="hand2",
                            font=theFont1)
        import_btn.pack(pady=10)

        #Action buttons
        actions = [
            ("View Files", self.view_files),
            ("Compare Files", self.compare_files),
            ("Plagiarism Checker", self.plagiarism_check),
            ("Naive Search", self.naive_search),
            ("Compression", self.compress_files)
        ]

        for label, command in actions:
            btn = Button(self.root, text=label, command=command, width=30, height=2, 
                         bg=color1, fg=color4,
                         activebackground= "#6a6a6a", activeforeground=color4,
                         cursor="hand2",
                         font=theFont1)
            btn.pack(pady=5)
        # Widget properties of the current date Label
        current_date = Label(root,
                                text=formatted_date,
                                fg=color6, bg=color2,
                                font=theFont2)
        current_date.pack(pady=5)
    
    # Function in import text files and pdfs, pdfs converted into text files
    def import_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf")
        ])

        if not file_paths:
            return

        for path in file_paths:
            filename = os.path.basename(path)
            name, ext = os.path.splitext(filename)

            if ext.lower() == ".pdf":
                # Convert PDF to .txt and save in Documents
                output_path = os.path.join(DOCUMENTS_FOLDER, f"{name}.txt")
                convert_pdf_to_text(path, output_path)
                print(f"Converted and imported: {output_path}")

            elif ext.lower() == ".txt":
                # Copy TXT directly
                dest_path = os.path.join(DOCUMENTS_FOLDER, filename)
                shutil.copy2(path, dest_path)
                print(f"Imported: {dest_path}")

        messagebox.showinfo("Import Complete", "Selected files have been imported!")

    # Function to activiate actions in show_file_list 
    def view_files(self):
        self.show_file_list(action="view")
    def compare_files(self):
        self.show_file_list(action="compare")
    def plagiarism_check(self):
        self.show_file_list(action="plagiarism")
    def naive_search(self):
        self.show_file_list(action="search")
    def compress_files(self):
        self.show_file_list(action="compress")
        

    def update_file_list(self, *args):
        # Clear old checkboxes
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        # Get sorted file list
        files = [f for f in os.listdir(DOCUMENTS_FOLDER) if f.endswith('.txt')]
        sort_choice = self.sort_var.get()

        if sort_choice == "Alphabetical":
            files = merge_sort(files)
        elif sort_choice == "Newest First":
            files = sorted(files, key=lambda f: os.path.getmtime(os.path.join(DOCUMENTS_FOLDER, f)), reverse=True)
        
        # Recreate checkboxes
        self.file_vars = {}
        for fname in files:
            var = BooleanVar()
            chk = Checkbutton(self.file_list_frame, text=fname, variable=var,
                              font=theFont1,bg=color6, fg=color2)
            chk.pack(anchor="w")
            self.file_vars[fname] = var

    def show_file_list(self, action):
        self.current_action = action

        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Instructions dictonary 
        instructions = {
            "view": "View all imported files:",
            "compare": "Select 2 files to compare:",
            "plagiarism": "Select 1 file to check for plagiarism:",
            "search": "Select 1 file to search:",
            "compress": "Select 1 or more files to compress:"
        }

        # Label for instruction
        instr_label = Label(self.root, text=instructions.get(action, ""), 
                            font=theFont2,
                            bg="#101010", fg=color4)
        instr_label.pack(pady=10)

         # Sort options
        self.sort_var = StringVar(value = "Sort")
        sort_options = ["Alphabetical", "Newest First"]
        
        # Sort menu
        sort_menu = OptionMenu(self.root, self.sort_var, *sort_options)
        sort_menu.config(bg=color6, fg=color4, 
                         font=theFont1,
                         activebackground= color1, activeforeground=color4,
                         cursor="hand2",
                         highlightbackground=color6)
        sort_menu['menu'].config(bg=color1, fg=color4,
                                activebackground=color6)
        sort_menu.pack(pady=5, anchor="e")

        self.sort_var.trace_add("write", self.update_file_list)
        # Frame to hold file checkboxes
        self.file_list_frame = Frame(self.root, bg= color6, 
                                    borderwidth=2, relief="sunken")
        self.file_list_frame.pack()
        self.update_file_list()
        

        # Confirm button
        confirm_btn = Button(self.root, text="Continue", 
                             command=self.handle_action, 
                             bg=color2, fg=color6,
                             activebackground= "#6a6a6a", activeforeground=color4,
                             cursor="hand2",
                             font=theFont1)
        confirm_btn.pack(pady=10)

        # Back button
        back_btn = Button(self.root, text="Main Menu", 
                          command=self.create_main_menu,
                          bg=color2, fg=color6,
                          activebackground= "#6a6a6a", activeforeground=color4,
                          cursor="hand2",
                          font=theFont1)   
        back_btn.pack()

    # Funcions for action functions for handle_action
    def view_file_content(self, filename):
        # If text_display does not exist yet, create it
        if not hasattr(self, "text_display") or not str(self.text_display):
            self.text_display = Text(self.root, width=80, height=20, wrap="word")
            self.text_display.pack(pady=10)

        # Now clear and update the text
        self.text_display.delete(1.0, END)  # Clear previous text
        full_path = os.path.join(DOCUMENTS_FOLDER, filename)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_display.insert(END, content)
        except Exception as e:
            self.text_display.insert(END, f"Error loading file: {e}")

    def run_naive_search(self, selected_files):
        pattern = self.pattern_entry.get()
        if not pattern:
            messagebox.showwarning("Input Required", "Please enter a pattern to search.")
            return

        results = []
        for fname in selected_files:
            full_path = os.path.join(DOCUMENTS_FOLDER, fname)
            with open(full_path, 'r', encoding='utf-8') as file:
                text = file.read()

            positions = naive_search(text, pattern)
            if positions:
                pos_str = ', '.join(map(str, positions))
                results.append(f"{fname}: Found at positions {pos_str}")
            else:
                results.append(f"{fname}: Pattern not found")

        # Display results in a textbox
        if hasattr(self, "search_results_textbox"):
            self.search_results_textbox.destroy()  # Clear old results

        self.search_results_textbox = Text(self.root, width=80, height=20, wrap="word",
                                           bg=color1, fg=color4)
        self.search_results_textbox.pack(pady=10)
        self.search_results_textbox.insert(END, "\n\n".join(results))
    
    def show_search_ui(self, selected_files):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Instruction Label
        instr_label = Label(self.root, text="Enter the pattern to search:", 
                            font=theFont2, bg=color6, fg=color4)
        instr_label.pack(pady=10)

        # Entry box for pattern
        self.pattern_entry = Entry(self.root, width=40, font=theFont1, bg=color3, fg=color4)
        self.pattern_entry.pack(pady=5)

        # Search Button
        search_btn = Button(self.root, text="Search", 
                            command=lambda: self.run_naive_search(selected_files),
                            bg=color2, fg=color6,
                            activebackground= "#6a6a6a", activeforeground=color4,
                            cursor="hand2",
                            font=theFont1)
        search_btn.pack(pady=10)

        # Back Button
        back_btn = Button(self.root, text="Back", 
                        command=lambda: self.show_file_list(action="search"),
                        bg=color2, fg=color6,
                        activebackground= "#6a6a6a", activeforeground=color4,
                        cursor="hand2",
                        font=theFont1)
        back_btn.pack()




    def handle_action(self):
        selected_files = [fname for fname, var in self.file_vars.items() if var.get()]

        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file.")
            return
        
        if self.current_action == "view":
            if len(selected_files) > 1:
                messagebox.showwarning("Multiple Selection", "Please select only one file to view.")
                return
            # Text box for file content display
            self.text_display = Text(self.root, width=80, height=20, wrap="word",
                                     bg=color3, fg=color4)
            self.text_display.pack(pady=10)
            self.view_file_content(selected_files[0])

        elif self.current_action == "search":
            if len(selected_files) > 1:
                messagebox.showwarning("Multiple Selection", "Please select only one file to view.")
                return
            self.show_search_ui(selected_files)

        elif self.current_action == "compress":
            result_msgs = []
            for fname in selected_files:
                full_path = os.path.join(DOCUMENTS_FOLDER, fname)
                compressed_path, huffman_codes = compress_file(full_path)

                original_size = os.path.getsize(full_path)
                compressed_size = os.path.getsize(compressed_path)
                compression_ratio = (compressed_size / original_size) * 100

                msg = f"{fname} \nOriginal: {original_size} bytes\nCompressed: {compressed_size} bytes\nCompression Ratio ({compression_ratio:.2f}%)"
                result_msgs.append(msg)

           # Check if textbox exists and is still valid
            if not hasattr(self, "compression_details_textbox") or not str(self.compression_details_textbox):
                self.compression_details_textbox = Text(self.root, bg=color1, fg=color5, font=theFont1)
                self.compression_details_textbox.pack(pady=10)
            else:
                try:
                    self.compression_details_textbox.delete(1.0, END)
                except TclError:
                    # Widget was destroyed, recreate it
                    self.compression_details_textbox = Text(self.root, bg=color1, fg=color5, font=theFont1)
                    self.compression_details_textbox.pack(pady=10)

            self.compression_details_textbox.insert(END, "\n\n".join(result_msgs))


        else: 
            print(f"Action: {self.current_action}, Selected: {selected_files}")


if __name__ == "__main__":
    root = Tk()
    app = DocumentScannerApp(root)
    root.mainloop()
