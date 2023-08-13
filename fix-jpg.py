# This is a GUI in PySimpleGUI with a button to open a file,
# a text field to add this file in binary, and a button to save the file.

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image():
    global hex_values
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg")])
    
    if file_path:
        with open(file_path, 'rb') as f:
            hex_values = f.read().hex().upper()
            hex_text.delete('1.0', tk.END)
            hex_text.insert('1.0', hex_values)
    print("Image hex has been loaded")

def update_image_display():
    print("Rendering...")
    global hex_values, image_label
    hex_values = hex_text.get('1.0', tk.END).replace('\n', '').strip()
    
    try:
        image_data = bytes.fromhex(hex_values)
        image_data = bytearray(image_data)
        with open("edited_image.jpg", "wb") as f:
            f.write(image_data)
            f.close()
        updated_image = Image.open("edited_image.jpg")
        
        updated_photo = ImageTk.PhotoImage(updated_image)
        image_label.configure(image=updated_photo)
        image_label.image = updated_photo
    except ValueError:
        pass
    print("done.")

def main():
    global hex_text, image_label
    root = tk.Tk()
    root.title("Hex Image Editor")

    open_button = tk.Button(root, text="Open Image", command=open_image)
    open_button.pack()

    update_button = tk.Button(root, text="Render Image", command=update_image_display)
    update_button.pack(side=tk.RIGHT)

    scroll_bar = tk.Scrollbar(root)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

    hex_text = tk.Text(root, height=45, width=180, yscrollcommand=scroll_bar.set)
    hex_text.pack()

    #hex_text.bind("<KeyRelease>", update_image_display)
    
    image_frame = tk.Frame(root)
    image_frame.pack()

    image_label = tk.Label(image_frame)
    image_label.pack()

    scroll_bar.config(command=hex_text.yview)
    root.mainloop()

if __name__ == "__main__":
    main()