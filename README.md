# 🛡️ Folder Shield Pro

> *A secure desktop utility designed to encrypt and protect sensitive folders using AES-256 encryption via the Fernet protocol.*

## 🔒 Security Features
- **AES-256 Encryption:** Utilizes `cryptography.fernet` to ensure folder contents are inaccessible without the correct Master Password.
- **Config Persistence:** Securely stores your master password hash in a local `config.json` file.
- **Fail-Safe Mechanism:** Includes a system reset feature for lost credentials (with a permanent lockout warning).
- **Dark UI:** Sleek, modern interface built with `tkinter` for a professional experience.

## ⚙️ How it Works
1. **Encryption:** The application compresses your folder into a ZIP, encrypts the binary data, and replaces the folder with a `.locked` file.
2. **Decryption:** It decrypts the `.locked` file using your Master Password and extracts the original folder structure.
3. **Integrity:** The `config.json` manages the authentication layer, ensuring only authorized users can lock/unlock files.

## 🚀 How to Run

1. **Download:** Click the green **[Code]** button -> **[Download ZIP]**.
2. **Extract:** Unzip the files.
3. **Open Terminal:** Open **PowerShell** or **Command Prompt** in the project folder.
4. **Execute:** Run the following command:
   python folder_shield_pro.py
