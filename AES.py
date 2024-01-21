from tkinter.messagebox import showerror
from tkinter import filedialog
from tkinter import *
from Crypto.Cipher import AES
from pygubu.builder import *
from Crypto import Random
from tkinter import *
import tkinter as tk
import threading
import pygubu
import base64
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        #loading and setting the GUI
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('Text_Cipher.ui')
        self.main_frame = builder.get_object('main_frame')
        builder.connect_callbacks(self)

        self.text_load_btn = builder.get_object('text_load_btn')

        self.input_text = builder.get_object('input_text')

        self.key_field = builder.get_object('key_field')

        self.vector_group = builder.get_variable("vector_group")
        self.mode_group = builder.get_variable("mode_group")
        self.key_group = builder.get_variable("key_group")

        self.radiobutton1 = builder.get_object('radiobutton1')
        self.radiobutton2 = builder.get_object('radiobutton2')
        self.vector_callback()

        self.radiobutton3 = builder.get_object('radiobutton3')
        self.radiobutton4 = builder.get_object('radiobutton4')
        self.mode_callback()

        self.radiobutton5 = builder.get_object('radiobutton5')
        self.radiobutton6 = builder.get_object('radiobutton6')
        self.radiobutton7 = builder.get_object('radiobutton7')
        self.key_callback()
        self.big_input = False

        self.file_path = ""

    def encrypt(self, message, key, mode):
        try:
            #Selection of how to generate the vector 'random' or 'null' according to the user's choice
            if self.vector == 1:
                # Generating a random vector
                iv = Random.new().read(AES.block_size)
            else:
                #Generating a vector by substituting only null values ​​into the block
                iv = b'\0' * AES.block_size
            # Use also in case of CBC
            if mode == AES.MODE_CBC:
                cipher = AES.new(key, mode, iv)
            else:
                #In the case of ECB, the library does not require an IV
                cipher = AES.new(key, mode)

            # Arrange data by blocks
            padding = AES.block_size - len(message) % AES.block_size
            message += bytes([padding]) * padding

            # Text encryption
            data = iv + cipher.encrypt(message) # IV + message
            # BASE64 encoding
            result = base64.b64encode(data)

            #Text settings in the GUI
            result = result.decode()
            # For performance reasons, allow a maximum of 55 characters per line
            if self.big_input:
                result = '\n'.join(result[i:i + 55] for i in range(0, len(result), 55))
                
            self.input_text.delete(1.0, "end")
            self.input_text.insert(1.0, result)
        except Exception as e:
            raise Exception("Something went wrong.\nTry to check your configuration.")

    def decrypt(self, message, key, mode):
        try:
            # Decoding a BASE64 message
            message = base64.b64decode(message)
            # Get vector (first block -> first 16 B)
            iv = message[:AES.block_size]

            # Use in case of CBC also
            if mode == AES.MODE_CBC:
                cipher = AES.new(key, mode, iv)
            else:
                cipher = AES.new(key, mode)
            # Data decryption
            data = cipher.decrypt(message[AES.block_size:])
            padding = data[-1]

            if data[-padding:] != bytes([padding]) * padding:
                raise ValueError("Invalid block allocation")

            self.input_text.delete(1.0, "end")
            self.input_text.insert(1.0, data[:-padding].decode("utf-8"))
        except Exception as e:
            raise Exception("Something went wrong.\nTry to check your configuration.")

    def encrypt_btn_click(self):
        self.input_text.config(state=NORMAL)
        #Getting the message to encode from widgets and then encoding the text to UTF-8
        message = self.input_text.get("1.0", END).encode('utf-8')

        key = self.key_field.get()
        if len(key) < self.key_len or len(key) > self.key_len:
            raise Exception("The length of the key must be: {} characters.\nYou have: {} Characters".format(self.key_len, len(key)))

        #Transforming the message into flat form
        key = bytes(key, "utf-8")
        self.encrypt(message, key, self.mode)

    def decrypt_btn_click(self):
        self.input_text.config(state=NORMAL)
        # Get the message to encode and encode the text to UTF-8
        message = self.input_text.get("1.0", END).encode('utf-8')
        key = self.key_field.get()
        if len(key) < self.key_len or len(key) > self.key_len:
            raise Exception(
                "The length of the key must be: {} characters.\nYou have {} Characters".format(self.key_len, len(key)))

        # Transforming the message into flat form
        key = bytes(key, "utf-8")
        self.decrypt(message, key, self.mode)

    def load_file(self):
        #Opens a dialog box to load a text file
        try:
            file_path = filedialog.askopenfilename(title="Select a text file", filetypes=
            [
                ('text files', ('.txt'))
            ])
            if not file_path or file_path is None or file_path == "":
                return

            #Open a separate file and load the data
            with open(file_path, 'r') as file:
                data = file.read()
                file_size = os.path.getsize(file_path)

                self.big_input = True if file_size >= 1000001 else False

                self.input_text.delete(1.0, "end")
                self.input_text.insert(1.0, data)
                file.close()
        except Exception as e:
            raise Exception("Failed to load file: " + str(e))

    def text_load_btn_click(self):
        # Start a new thread to load a file
        startit = threading.Thread(target=self.load_file)
        startit.start()

    def save_file(self):
        #Save a file
        try:
            save_location = filedialog.asksaveasfile(mode='w', initialfile="cipher", defaultextension=".txt",
                                                     filetypes=
                                                     [
                                                         ('text files', ('.txt'))
                                                     ])
            if save_location is None or not save_location or save_location == "":
                return

            message = self.input_text.get("1.0", END)
            save_location.write(message)
            save_location.close()
        except Exception as e:
            raise Exception("Failed to save file:  " + str(e))

    def save_btn_click(self):
        #Start a new thread to save the file
        startit = threading.Thread(target=self.save_file)
        startit.start()

    def vector_callback(self):
        #callback function for setting the vector after clicking the button
        self.vector = self.vector_group.get()

    def mode_callback(self):
        #Callback function for setting the mode
        value = self.mode_group.get()
        if value == 1:
            self.mode = AES.MODE_CBC
        else:
            self.mode = AES.MODE_ECB

    def key_callback(self):
        #Callback function for setting the key size when the radiobutton is clicked
        value = self.key_group.get()

        if value == 1:
            self.key_len = 16
        elif value == 2:
            self.key_len = 24
        else:
            self.key_len = 32

    def clear_btn_callback(self):
        #Callback function for reset button
        self.input_text.delete(1.0, "end")
        self.key_field.delete(0, END)

    def run(self):
        self.main_frame.mainloop()

if __name__ == '__main__':
    root = Tk()
    root.title("AES Text Cipher")
    app = MainWindow(root)
    
    #Setting the Error Notification Dialog Box
    def report_callback_exception(self, exc, val, tb):
        showerror("Error", message=str(val))

    tk.Tk.report_callback_exception = report_callback_exception
    app.run()