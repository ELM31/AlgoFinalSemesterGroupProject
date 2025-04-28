from tkinter import *                                   #Tkinter based program
from tkinter import filedialog, messagebox              #Use Tkinters filedialgo aswell as message box 
from algo.huffman import compress_file, decompress_file #Import some functions from huffman py in the algo folder 
from cosmetic import WindowSet                          #Import WindowSet from the cosmetic folder
from cosmetic.dark_title_bar import *                   #Import dark_title_bar from the cosmetic folder, looking cool :)
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
        WindowSet.setScreen(root, wRatio= .39, hRatio= .84)

        self.stored_huffman_codes = None
        self.stored_compressed_path = None

        self.create_widgets()
    
    #Create all the widgets 
    def create_widgets(self):
        pdf_frame = Frame
        #Label widget for header
        name_label = Label(root,
                        text="Tuffy's Document Scanner",
                        bg=color1, fg=color2,
                        font=("Fixedsys", 20))
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #Widget properties for the Select button 
        select_button = Button(root, 
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
        select_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #Widget properties for the results label 
        result_label = Label(root,
                                    text="Compression details will appear here.",
                                    fg= color5,
                                    bg= color1,
                                    font=("Fixedsys", 2))
        result_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #Widget properties for the Huffman code textbox 
        huffman_codes_text1 = Text(root, 
                                        height=20, width=35,
                                        fg = "#c1bec8", bg="#585858")
        huffman_codes_text1.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        huffman_codes_text2 = Text(root, 
                                        height=20, width=35,
                                        fg = "#c1bec8", bg="#585858")
        huffman_codes_text2.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        #Widget properties for the decompress button
        decompress_button = Button(root, 
                                        text="Decompress File", 
                                        command=self.decompress_and_display,
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
        decompress_button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        #Widget properties for the decoded textbox 
        decoded_text_display = Text(root, 
                                        height=10, 
                                        width=70, 
                                        fg = '#c1bec8',
                                        bg="#585858")
        decoded_text_display.grid(row=5, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

         # Widget properties of the current date Label
        current_date = Label(root,
                                text=formatted_date,
                                fg=color1, bg=color2,
                                font=("Fixedsys", 17)
                                )
        current_date.grid(row=6, column=0, padx=15, pady=5, sticky="W")

    def select_file(self): 
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]) #User chooses file
        if file_path: #if statement checks if file is non-void, allows the file to continue to the next function
            self.compress_and_display(file_path)

    def compress_and_display(self, file_path):
        compressed_path, huffman_codes = compress_file(file_path) #compress file using function from huffman code 
        
        #getting the ratio 
        original_size = os.path.getsize(file_path) #return orignal file size in bytes
        compressed_size = os.path.getsize(compressed_path) #return compressed file size in bytes
        compression_ratio = (compressed_size / original_size) * 100 #percentage of compressed file size compared to the original file size 
        
        #Showing results 
        self.result_label.config(text=f"Original: {original_size} bytes | Compressed: {compressed_size} bytes | Ratio: {compression_ratio:.2f}%") #results of the compression
        self.huffman_codes_text.delete("1.0", END) #gets rid of the previous label to show results
        
        #Go through the huffman_code dictonrary inserting each character into the huffman_code_text textbox
        for char, code in huffman_codes.items():
            self.huffman_codes_text.insert(END, f"{char}: {code}\n")
        
        #storing into the global variables 
        stored_huffman_codes = huffman_codes
        stored_compressed_path = compressed_path

    def decompress_and_display(self):
        #If program does has not yet used a file yet 
        if not self.stored_compressed_path or not self.stored_huffman_codes:
            messagebox.showerror("Error", "No file has been compressed yet!")
            return
        
        #Decompression processusing the decompress_file from the huffman python file 
        output_path = self.stored_compressed_path.replace(".bin", "_decompressed.txt")
        decompress_file(self.stored_compressed_path, self.stored_huffman_codes, output_path)
        
        #reading the decompressed file 
        with open(output_path, 'r', encoding='utf-8') as file:
            decoded_text = file.read()
        
        #Display text, while also deleting texts if any exists in the textbox
        self.decoded_text_display.delete("1.0", END)
        self.decoded_text_display.insert(END, decoded_text)
#Main function used to run the GUI
if __name__ == "__main__":    
    root = Tk()
    app = DocumentScannerGUI(root)
    root.mainloop()
