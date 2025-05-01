from tkinter import *                                   #Tkinter based program
from tkinter import filedialog, messagebox              #Use Tkinters filedialgo aswell as message box 
from algo.huffman import compress_file, decompress_file #Import some functions from huffman py in the algo folder 
from cosmetic import WindowSet                          #Import WindowSet from the cosmetic folder
from cosmetic.dark_title_bar import *                   #Import dark_title_bar from the cosmetic folder, looking cool :)
from bfs_dfs import bfs, dfs                            #Import BFS and DFS functions
import os                                               #Used to track files and stuff 
from datetime import date                               #For current date 

#Today's Date
today = date.today()
formatted_date = today.strftime("%m/%d/%Y")

#Global colors used + main font used 
color1 = '#343434'  # dark gray used for background for frames
color2 = '#29aff1'  # primary blue used throughout the app
color3 = '#4d4d4d'  # lighter gray used for entry background
color4 = '#ebebeb'  # cream color used for foreground
color5 = "#d50ce2"  # rose color 
theFont = "arial"   #Primary font used

#GUI Class
class DocumentScannerGUI: 
    #Initilize 
    def __init__(self, root):
        self.root = root 
        self.root.title("Tuffy's Document Scanner" )
        root.configure(bg='#101010')
        dark_title_bar(root)
        root.geometry("+0+0")
        WindowSet.setScreen(root, wRatio= .72, hRatio= .84) 

        self.stored_huffman_codes = None
        self.stored_compressed_path = None
        self.graph = {}  # Graph for citations

        self.create_widgets()
    
    #Create all the widgets 
    def create_widgets(self):
        #Label widget for header
        self.name_label = Label(root,
                        text="Tuffy's Document Scanner",
                        bg=color1, fg=color2,
                        font=("Fixedsys", 20))
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #Widget properties for the Select button 
        self.select_button = Button(root, 
                                    text="Select Files", 
                                    command=self.select_file,
                                    activebackground="#6a6a6a",
                                    activeforeground="white",
                                    fg=color1,
                                    bg=color2,
                                    font=("Fixedsys", 17),
                                    cursor="hand2",
                                    bd=3,
                                    disabledforeground="gray",
                                    highlightbackground="black",
                                    highlightcolor="green",
                                    highlightthickness=2
                                    )
        self.select_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        # Button to model citations
        self.citation_button = Button(root,
                                       text="Model Citations",
                                       command=self.model_citations,
                                       activebackground="#6a6a6a",
                                       activeforeground="white",
                                       fg=color1,
                                       bg=color2,
                                       font=("Fixedsys", 17),
                                       cursor="hand2",
                                       bd=3,
                                       highlightbackground="black",
                                       highlightcolor="green",
                                       highlightthickness=2)
        self.citation_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #Widget properties for the results label 
        self.result_label1 = Label(root,
                                    text="Compression details will appear here",
                                    fg= color5,
                                    bg= color1,
                                    font=("Fixedsys", 2))
        self.result_label1.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.result_label2 = Label(root,
                                    text="Compression details will appear here",
                                    fg= color5,
                                    bg= color1,
                                    font=("Fixedsys", 2))
        self.result_label2.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        #Widget properties for the Huffman code textbox 
        self.huffman_codes_text1 = Text(root, 
                                        height=20, width=67,
                                        fg = "#c1bec8", bg="#585858")
        self.huffman_codes_text1.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        self.huffman_codes_text2 = Text(root, 
                                        height=20, width=67,
                                        fg = "#c1bec8", bg="#585858")
        self.huffman_codes_text2.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        # Textbox to display BFS/DFS results
        self.traversal_result = Text(root,
                                     height=10,
                                     width=74,
                                     fg='#c1bec8',
                                     bg="#585858")
        self.traversal_result.grid(row=5, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #Widget properties for the decompress button
        self.decompress_button = Button(root, 
                                        text="Compare Files", 
                                        activebackground="#6a6a6a",
                                        activeforeground="white",
                                        fg= color1,
                                        bg= color2,
                                        font=("Fixedsys", 17),
                                        cursor="hand2",
                                        bd=3,
                                        disabledforeground="gray",
                                        highlightbackground="black",
                                        highlightcolor="green",
                                        highlightthickness=2)
        self.decompress_button.grid(row=6, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #Widget properties for the decoded textbox 
        self.decoded_text_display = Text(root, 
                                        height=10, 
                                        width=74, 
                                        fg = '#c1bec8',
                                        bg="#585858")
        self.decoded_text_display.grid(row=7, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

         # Widget properties of the current date Label
        self.current_date = Label(root,
                                text=formatted_date,
                                fg=color1, bg=color2,
                                font=("Fixedsys", 17)
                                )
        self.current_date.grid(row=8, column=0, padx=15, pady=5, sticky="W")

    def select_file(self): 
        # Ask for the first file
        file_path1 = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path1:
            messagebox.showerror("Error", "You must select the first file.")
            return

        # Ask for the second file
        file_path2 = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path2:
            messagebox.showerror("Error", "You must select the second file.")
            return

        # Now we have both file paths
        file_paths = (file_path1, file_path2)
        self.compress_and_display(file_paths)

        self.decompress_and_display()

    def compress_and_display(self, file_paths):
        file_path1, file_path2 = file_paths

        compressed_path1, huffman_codes1 = compress_file(file_path1)
        compressed_path2, huffman_codes2 = compress_file(file_path2)

        # Store correct pairs
        self.stored_files = [
            (compressed_path1, huffman_codes1),
            (compressed_path2, huffman_codes2)
        ]

        # Now show compression ratios correctly
        original_size1 = os.path.getsize(file_path1)
        compressed_size1 = os.path.getsize(compressed_path1)
        compression_ratio1 = (compressed_size1 / original_size1) * 100

        self.result_label1.config(text=f"Original: {original_size1} bytes | Compressed: {compressed_size1} bytes | Ratio: {compression_ratio1:.2f}%")
        self.huffman_codes_text1.delete("1.0", END)

        original_size2 = os.path.getsize(file_path2)
        compressed_size2 = os.path.getsize(compressed_path2)
        compression_ratio2 = (compressed_size2 / original_size2) * 100

        self.result_label2.config(text=f"Original: {original_size2} bytes | Compressed: {compressed_size2} bytes | Ratio: {compression_ratio2:.2f}%")
        self.huffman_codes_text2.delete("1.0", END)

    def decompress_and_display(self):
        if not hasattr(self, 'stored_files') or not self.stored_files:
            messagebox.showerror("Error", "No files have been compressed yet!")
            return

        (compressed_path1, huffman_codes1) = self.stored_files[0]
        (compressed_path2, huffman_codes2) = self.stored_files[1]

        output_path1 = compressed_path1.replace(".bin", "_decompressed.txt")
        output_path2 = compressed_path2.replace(".bin", "_decompressed.txt")

        decompress_file(compressed_path1, huffman_codes1, output_path1)
        decompress_file(compressed_path2, huffman_codes2, output_path2)

        with open(output_path1, 'r', encoding='utf-8') as file1:
            decoded_text1 = file1.read()
        with open(output_path2, 'r', encoding='utf-8') as file2:
            decoded_text2 = file2.read()

        self.huffman_codes_text1.delete("1.0", END)
        self.huffman_codes_text1.insert(END, decoded_text1)

        self.huffman_codes_text2.delete("1.0", END)
        self.huffman_codes_text2.insert(END, decoded_text2)

    def model_citations(self):
        # Prompt user to input citation relationships
        num_edges = int(self.simple_input_dialog("Enter number of citation relationships:"))
        for _ in range(num_edges):
            relationship = self.simple_input_dialog("Enter citation (Document1 Document2):")
            doc1, doc2 = relationship.split()

            if doc1 not in self.graph:
                self.graph[doc1] = []
            self.graph[doc1].append(doc2)

        # Prompt user for traversal type using buttons
        traversal_type = self.select_traversal_type()
        if not traversal_type:
            return  # User canceled the selection

        start_node = self.simple_input_dialog("Enter the starting document:")

        # Perform the selected traversal
        if traversal_type == "bfs":
            result = bfs(self.graph, start_node)
        elif traversal_type == "dfs":
            result = dfs(self.graph, start_node)

        # Display the traversal result
        self.traversal_result.delete("1.0", END)
        self.traversal_result.insert(END, f"{traversal_type.upper()} Traversal Order:\n")
        self.traversal_result.insert(END, " -> ".join(result))

    def select_traversal_type(self):
        # Popup window for selecting traversal type
        selection_window = Toplevel(self.root)
        selection_window.title("Select Traversal Type")
        selection_window.geometry("300x200")
        selection_window.configure(bg=color1)

        label = Label(selection_window, text="Choose Traversal Type:", bg=color1, fg=color4, font=(theFont, 12))
        label.pack(pady=10)

        traversal_type = StringVar(value="")  # Variable to store the selected option

        # BFS button
        bfs_button = Radiobutton(selection_window, text="BFS", variable=traversal_type, value="bfs",
                                 bg=color1, fg=color4, font=(theFont, 12), selectcolor=color3)
        bfs_button.pack(pady=5)

        # DFS button
        dfs_button = Radiobutton(selection_window, text="DFS", variable=traversal_type, value="dfs",
                                 bg=color1, fg=color4, font=(theFont, 12), selectcolor=color3)
        dfs_button.pack(pady=5)

        def submit():
            selection_window.destroy()

        submit_button = Button(selection_window, text="Submit", command=submit, bg=color2, fg=color1, font=(theFont, 12))
        submit_button.pack(pady=10)

        selection_window.wait_window()
        return traversal_type.get()

    def simple_input_dialog(self, prompt):
        # Simple input dialog using a popup window
        input_window = Toplevel(self.root)
        input_window.title("Input")
        input_window.geometry("300x150")
        input_window.configure(bg=color1)

        label = Label(input_window, text=prompt, bg=color1, fg=color4, font=(theFont, 12))
        label.pack(pady=10)

        input_var = StringVar()
        entry = Entry(input_window, textvariable=input_var, font=(theFont, 12))
        entry.pack(pady=5)

        def submit():
            input_window.destroy()

        submit_button = Button(input_window, text="Submit", command=submit, bg=color2, fg=color1, font=(theFont, 12))
        submit_button.pack(pady=10)

        input_window.wait_window()
        return input_var.get()

#Main function used to run the GUI
if __name__ == "__main__":    
    root = Tk()
    app = DocumentScannerGUI(root)
    root.mainloop()
