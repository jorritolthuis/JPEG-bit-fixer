# This is a GUI in PySimpleGUI with a button to open a file,
# a text field to add this file in binary, and a button to save the file.

import PySimpleGUI as sg
import os
import sys
import binascii

def convert_base(num_str, source_base, target_base, target_length):
    # Convert the input string to an integer in the source base
    num_int = int(num_str, source_base)
    
    # Convert the integer to a string in the target base
    target_num_str = ''
    while num_int > 0:
        remainder = num_int % target_base
        if remainder < 10:
            target_num_str = str(remainder) + target_num_str
        else:
            target_num_str = chr(ord('a') + remainder - 10) + target_num_str
        num_int //= target_base
    
    # Add leading zeros to reach the target length
    while len(target_num_str) < target_length:
        target_num_str = '0' + target_num_str
    
    return target_num_str

# Converts binary to a string of 0 and 1 separated by spaces at every nibble
def to_binary(text):
    text = text.decode("utf-8")
    binary_txt = ""
    for i in range(0, len(text)):
        binary_txt += convert_base(text[i], 16, 2, 4)
    binary_txt = " ".join(binary_txt[i:i+4] for i in range(0, len(binary_txt), 4))
    return binary_txt

# Converts a string of 0 and 1 separated by a space at every nibble to bytes data
def from_binary(binary):
    binary = binary.replace(" ", "")
    hex_txt = ""
    for i in range(0, len(binary), 4):
        if i + 4 > len(binary):
            print("WARNING: binary string is not a multiple of 4")
            break
        hex_txt += convert_base(binary[i:i+4], 2, 16, 1)
    return hex_txt


# Define the window's contents
layout = [[sg.Text("File to open:")],
            [sg.Input(key="-FILE-"), sg.FileBrowse(file_types=(("Images", "*.jpg"), ))],
            [sg.Button("Open")],
            [sg.Text("File in binary:")],
            [sg.Multiline(key="-BIN-", size=(100, 40), font=("Courier New", 12))],
            [sg.Button("Render")],
            [sg.Button("Save")]]

# Create the window
window = sg.Window("Binary File Editor", layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if event == "Open":
        try:
            with open(values["-FILE-"], "rb") as f:
                content = f.read()
            bin_obj = binascii.hexlify(content)
            window["-BIN-"].update(bin_obj)
            #binary = to_binary(bin_obj)
            #window["-BIN-"].update(binary)
        except:
            window["-BIN-"].update("Error opening file.")
    if event == "Render":
        # Write the binary to a temporary file
        with open("temp.jpg", "wb") as f:
            #f.write(binascii.unhexlify(from_binary(values["-BIN-"])))
            f.write(binascii.unhexlify(values["-BIN-"]))
        # Open the temporary file with the default program
        os.startfile("temp.jpg")
    if event == "Save":
        # Show pop-up to save the file
        filename = sg.popup_get_file("Save file", save_as=True, file_types=(("Images", "*.jpg"), ))
        if filename:
            # Write the binary to the file
            with open(filename, "wb") as f:
                f.write(binascii.unhexlify(from_binary(values["-BIN-"])))
            sg.popup("File saved successfully!")
            break

window.close()