**AES Text Cipher**

License: MIT: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)


**Description**

This Python application provides a user-friendly interface for encrypting and decrypting text using the AES (Advanced Encryption Standard) cipher. It features:

- **Encryption and decryption:** Securely encrypt or decrypt text using AES.
- **Key size selection:** Choose between 128-bit, 192-bit, or 256-bit keys for varying security levels.
- **Cipher mode selection:** Select between ECB (Electronic Codebook) or CBC (Cipher Block Chaining) modes for different levels of security and data integrity.
- **IV generation:** Choose random or null initialization vectors (IVs) for CBC mode.
- **File loading and saving:** Encrypt and decrypt text from and to files.
- **Error handling:** Displays informative error messages to guide users.
- **Seamless UI:** Simply yet seamless User Interface foe easier approach
**Dependencies**

- Python 3
- `pygubu`
- `pycryptodome`
- `tkinter`

**Installation**

1. Install dependencies:

   ```bash
   pip install pygubu pycryptodome
   ```

2. Download the code files: `AES.py` and `Text_Cipher.ui`.


3. Clone the repository:

   ```bash
   git clone https://github.com/[your-username]/AES-Text-Cipher.git
   ```

4. Install dependencies:

   ```bash
   cd AES-Text-Cipher
   pip install -r requirements.txt
   ```

**Usage**

1. Run the application:

   ```bash
   python AES.py
   ```

2. **GUI Interface:**
   - Enter text to encrypt or paste text from a file.
   - Provide the encryption/decryption key (16, 24, or 32 characters).
   - Select the desired key size and cipher mode.
   - Click "Encrypt" or "Decrypt".
   - View the encrypted or decrypted text in the output field.
   - Save the output to a file if needed.

**Important Notes**

- **Secure key management:** Keep encryption keys confidential and store them securely.
- **Cipher mode selection:** CBC mode is generally preferred over ECB mode for better security.
- **IVs in CBC mode:** Use a different, unpredictable IV for each encryption to ensure security.
- **Error handling:** Pay attention to error messages for troubleshooting.


**Additional Information**

- **Code structure:** The code is organized into classes for readability and maintainability.
- **GUI layout:** The GUI is designed using `pygubu` for a user-friendly experience.
- **Encryption/decryption details:** The code uses the `Crypto.Cipher` library for AES encryption and decryption.
- **Error handling:** The code includes error handling to catch potential exceptions and provide informative messages.


**Contributing**

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

**License**

MIT: [https://choosealicense.com/licenses/mit/](https://choosealicense.com/licenses/mit/)
