# 🔒 MyPass - Modern & Secure Password Manager

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-UI-blue?style=for-the-badge)
![Cryptography](https://img.shields.io/badge/Cryptography-Fernet-red?style=for-the-badge)

A highly secure, locally stored password manager built with **Python** and **CustomTkinter**. Unlike basic implementations, this project features **military-grade encryption (Fernet)** to protect user credentials stored in a local JSON database.

<img width="621" height="505" alt="image" src="https://github.com/user-attachments/assets/1f35abc2-0e45-4512-8671-04ce222f3fb2" />

## 🛡️ Key Features
* **Modern UI:** Built with `CustomTkinter` for a sleek, dark-mode compatible interface.
* **Strong Encryption:** Uses the `cryptography` library (Fernet) to encrypt passwords before saving them. Even if someone steals the database, they cannot read the passwords without the key.
* **Password Generator:** Integrated tool to generate strong, randomized passwords.
* **Clipboard Support:** Automatically copies generated passwords to the clipboard using `pyperclip`.
* **Search & Delete:** Easily find or remove credentials from the database.

## ⚠️ Security Notice
This project generates a `key.key` file upon first run. **Do not lose this file!** Without it, the encrypted data in `data.json` cannot be decrypted and will be lost forever.
*Note: The `key.key` and `data.json` files are excluded from this repository for security reasons (.gitignore).*

## 🛠️ Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/kutyfuty/MyPass-Password-Manager.git](https://github.com/kutyfuty/MyPass-Password-Manager.git)
