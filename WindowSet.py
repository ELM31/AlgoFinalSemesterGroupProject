# Since main py file already has the tkinter import, no need to import here

def setScreen(root, wRatio , hRatio):
    screenW = root.winfo_screenwidth() # Gets the native screen width
    screenH = root.winfo_screenheight() # Gets the native screen height
    
    width = int(screenW * wRatio) # Multiplies by desired width ratio
    height = int(screenH * hRatio) # Multiplies by desired heigh ratio

    root.geometry(f"{width}x{height}")
