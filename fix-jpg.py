# This is a GUI in PySimpleGUI with a button to open a file,
# a text field to add this file in binary, and a button to save the file.

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image():
    global hex_values
    global prefix, suffix
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.JPEG *.JPG")])
    
    prefix_bound = float(configs[0].get())
    suffix_bound = float(configs[1].get())

    if file_path:
        with open(file_path, 'rb') as f:
            hex_values = f.read().hex().upper()
            prefix = hex_values[:int(len(hex_values) * prefix_bound)]
            suffix = hex_values[int(len(hex_values) * suffix_bound):]
            print("Total file length = ", len(hex_values))
            print("Prefix length = ", len(prefix))
            print("Suffix length = ", len(suffix))
            print("Display length = ", len(hex_values) - len(prefix) - len(suffix))
            hex_text.delete('1.0', tk.END)
            hex_text.insert('1.0', hex_values[int(len(hex_values) * prefix_bound): int(len(hex_values) * suffix_bound)])
    print("Image hex has been loaded")

def update_image_display():
    print("Rendering...")
    global hex_values, image_label, prefix, suffix
    hex_values = hex_text.get('1.0', tk.END).replace('\n', '').strip()
    
    try:
        image_data = bytes.fromhex(prefix + hex_values + suffix)
        image_data = bytearray(image_data)
        with open("edited_image.jpg", "wb") as f:
            f.write(image_data)
            f.close()
        updated_image = Image.open("edited_image.jpg")
        zoom_x = float(configs[2].get())
        zoom_w = float(configs[3].get())
        zoom_y = float(configs[4].get())
        zoom_h = float(configs[5].get())

        updated_image = updated_image.crop((int(zoom_x*updated_image.width), 
                                            int(zoom_y*updated_image.height), 
                                            int((zoom_x + zoom_w)*updated_image.width), 
                                            int((zoom_y + zoom_h)*updated_image.height))
                                        ).resize((800, 800))
        updated_photo = ImageTk.PhotoImage(updated_image, width=800)
        image_label.configure(image=updated_photo)
        image_label.image = updated_photo
    except ValueError:
        pass
    print("done.")

def main():
    global hex_text, image_label
    global prefix, suffix
    global configs

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

    # An option to not use the Render button, but every time the user edits something
    #hex_text.bind("<KeyRelease>", update_image_display)
    
    scroll_bar.config(command=hex_text.yview)
    
    # Image preview window
    img_root = tk.Toplevel()
    img_root.title("Image Preview")
    img_root.geometry("800x800")

    image_frame = tk.Frame(img_root)
    image_frame.pack()

    image_label = tk.Label(image_frame)
    image_label.pack()

    # The config panel
    config_root = tk.Toplevel()
    config_root.title("Config Panel")

    panel = tk.Frame(config_root)
    panel.pack(padx=20, pady=20)

    labels = ["Prefix Bound", "Suffix Bound", "Zoom X", "Zoom width", "Zoom Y", "Zoom height"]
    init_vals = [0.797824, 0.797829, 0.6, 0.05, 0.8, 0.05]
    configs = []

    for label_text in labels:
        label = tk.Label(panel, text=label_text)
        label.grid(row=labels.index(label_text), column=0, padx=5, pady=5, sticky="e")

        entry = tk.Entry(panel)
        entry.grid(row=labels.index(label_text), column=1, padx=5, pady=5, sticky="w")
        entry.insert(0, init_vals[labels.index(label_text)])
        configs.append(entry)

    # The GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()