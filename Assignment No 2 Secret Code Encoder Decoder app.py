import tkinter as tk
from tkinter import messagebox
import pyperclip  # For clipboard functionality (You will need to install this package: pip install pyperclip)

# Caesar Cipher encode function
def encode_message(message, shift):
    encoded_message = ""
    for char in message:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            encoded_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            encoded_message += encoded_char
        else:
            encoded_message += char
    return encoded_message

# Caesar Cipher decode function
def decode_message(message, shift):
    return encode_message(message, -shift)

# Function to encode message from GUI
def encode_gui_message():
    message = entry_message.get()
    try:
        shift = int(entry_shift.get())
        encoded_message = encode_message(message, shift)
        result_var.set(f"Encoded Message:\n{encoded_message}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid shift number.")

# Function to decode message from GUI
def decode_gui_message():
    message = entry_message.get()
    try:
        shift = int(entry_shift.get())
        decoded_message = decode_message(message, shift)
        result_var.set(f"Decoded Message:\n{decoded_message}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid shift number.")

# Function to copy result to clipboard
def copy_to_clipboard():
    result = result_var.get().split(":\n")[-1]  # Extract the encoded/decoded message
    pyperclip.copy(result)
    messagebox.showinfo("Copied", "The message has been copied to clipboard!")

# GUI setup
root = tk.Tk()
root.title("Secret Code Generator")
root.geometry("500x400")
root.config(bg='#2B2B2B')  # Dark background for futuristic appearance

# Title label
tk.Label(root, text="Secret Code Generator", font=("Helvetica", 18, "bold"), bg='#2B2B2B', fg='#FFEB3B').pack(pady=10)

# Message entry
tk.Label(root, text="Enter your message:", font=("Helvetica", 12), bg='#2B2B2B', fg='white').pack(pady=5)
entry_message = tk.Entry(root, width=50, font=("Helvetica", 12))
entry_message.pack(pady=10)

# Shift entry
tk.Label(root, text="Enter shift value:", font=("Helvetica", 12), bg='#2B2B2B', fg='white').pack(pady=5)
entry_shift = tk.Entry(root, width=10, font=("Helvetica", 12))
entry_shift.pack(pady=10)

# Result display area
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=("Helvetica", 12), bg='#2B2B2B', fg='lightgreen', wraplength=400, justify='left')
result_label.pack(pady=10)

# Button Frame
button_frame = tk.Frame(root, bg='#2B2B2B')
button_frame.pack(pady=10)

# Encode and Decode buttons
encode_button = tk.Button(button_frame, text="Encode", command=encode_gui_message, font=("Helvetica", 12), bg='#4CAF50', fg='white', width=10)
encode_button.grid(row=0, column=0, padx=5)

decode_button = tk.Button(button_frame, text="Decode", command=decode_gui_message, font=("Helvetica", 12), bg='#2196F3', fg='white', width=10)
decode_button.grid(row=0, column=1, padx=5)

# Copy to Clipboard button
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=("Helvetica", 12), bg='#FF5722', fg='white')
copy_button.pack(pady=10)

# Exit button
exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Helvetica", 12), bg='#f44336', fg='white', width=10)
exit_button.pack(pady=10)

# Run the application
root.mainloop()
