import customtkinter
from tkinter import messagebox
import random
import pyperclip
import json
from cryptography.fernet import Fernet
from PIL import Image
import os

# --- THEME SETTINGS ---
customtkinter.set_appearance_mode("Dark")  # Options: "System", "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

# --- ENCRYPTION SETUP ---
def load_key():
    """Loads the encryption key from file or generates a new one."""
    key_path = "key.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            key = key_file.read()
            return key
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        return key

key = load_key()
cipher = Fernet(key)

# ---------------------------- FUNCTIONS ------------------------------- #
def save():
    """Encrypts and saves the password to the JSON database."""
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
        return

    # Encrypt the password
    encrypted_password = cipher.encrypt(password.encode()).decode()

    new_data = {
        website: {
            "email": email,
            "password": encrypted_password,
        }
    }

    is_ok = messagebox.askokcancel(title=website, message=f"Details entered:\nEmail: {email}\nPassword: {password}\nIs it ok to save?")

    if is_ok:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            if website in data:
                is_update = messagebox.askyesno(title="Update Entry", message=f"Entry for {website} already exists.\nUpdate password?")
                if is_update:
                    data.update(new_data)
                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
                    messagebox.showinfo(title="Success", message="Password updated successfully!")
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
        finally:
            entry_website.delete(0, 'end')
            entry_password.delete(0, 'end')
            entry_website.focus()

def generate_password():
    """Generates a random strong password."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)
    password = "".join(password_list)

    entry_password.delete(0, 'end')
    entry_password.insert(0, password)
    pyperclip.copy(password)

def find_password():
    """Searches for a website and shows the decrypted password."""
    website = entry_website.get()
    if len(website) == 0:
         messagebox.showwarning(title="Oops", message="Please enter a website name.")
         return

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            encrypted_password = data[website]["password"]
            try:
                decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
                messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {decrypted_password}")
            except:
                messagebox.showerror(title="Error", message="Could not decrypt password (Key mismatch).")
        else:
            messagebox.showinfo(title="Not Found", message=f"No details for {website} exists.")

def toggle_password():
    """Toggles password visibility."""
    if entry_password.cget('show') == '*':
        entry_password.configure(show='')
    else:
        entry_password.configure(show='*')

def delete_password():
    """Deletes an entry from database."""
    website = entry_website.get()
    if len(website) == 0:
         messagebox.showwarning(title="Oops", message="Please enter a website to delete.")
         return

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    else:
        if website in data:
            confirm = messagebox.askyesno(title="Confirm Delete", message=f"Are you sure you want to delete {website}?")
            if confirm:
                del data[website]
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
                messagebox.showinfo(title="Deleted", message=f"{website} deleted successfully.")
                entry_website.delete(0, 'end')
        else:
            messagebox.showwarning(title="Error", message="Website not found.")

# ---------------------------- UI LAYOUT ------------------------------- #
window = customtkinter.CTk()
window.title("MyPass - Password Manager")
window.geometry("620x480")
window.config(padx=40, pady=40)

# Grid Configuration (4 Columns for perfect alignment)
# Col 0: Labels | Col 1: Entries | Col 2: Button 1 | Col 3: Button 2
window.grid_columnconfigure(1, weight=1)

# --- LOGO ---
try:
    logo_img_data = Image.open("assets/logo.png")
    my_image = customtkinter.CTkImage(light_image=logo_img_data,
                                      dark_image=logo_img_data,
                                      size=(160, 160))
    image_label = customtkinter.CTkLabel(window, image=my_image, text="")
    image_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
except FileNotFoundError:
    image_label = customtkinter.CTkLabel(window, text="🔒 MyPass", font=("Arial", 30, "bold"), text_color="#3B8ED0")
    image_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))


# --- ROW 1: Website ---
label_website = customtkinter.CTkLabel(window, text="Website:", font=("Arial", 14))
label_website.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="e")

entry_website = customtkinter.CTkEntry(window, width=200, placeholder_text="e.g. Amazon")
entry_website.grid(row=1, column=1, padx=(0, 5), pady=10, sticky="ew")

btn_search = customtkinter.CTkButton(window, text="Search", width=90, command=find_password)
btn_search.grid(row=1, column=2, padx=5, pady=10)

btn_delete = customtkinter.CTkButton(window, text="Delete", width=60, fg_color="#D32F2F", hover_color="#B71C1C", command=delete_password)
btn_delete.grid(row=1, column=3, padx=(5, 0), pady=10)


# --- ROW 2: Email (Full Width) ---
label_email = customtkinter.CTkLabel(window, text="Email/User:", font=("Arial", 14))
label_email.grid(row=2, column=0, padx=(0, 10), pady=10, sticky="e")

entry_email = customtkinter.CTkEntry(window)
entry_email.insert(0, "my.email@example.com")
# Spans 3 columns to align with Entry + Search + Del buttons
entry_email.grid(row=2, column=1, columnspan=3, padx=(0, 0), pady=10, sticky="ew")


# --- ROW 3: Password ---
label_pass = customtkinter.CTkLabel(window, text="Password:", font=("Arial", 14))
label_pass.grid(row=3, column=0, padx=(0, 10), pady=10, sticky="e")

entry_password = customtkinter.CTkEntry(window, width=200, show="*")
entry_password.grid(row=3, column=1, padx=(0, 5), pady=10, sticky="ew")

btn_show = customtkinter.CTkButton(window, text="Show", width=90, fg_color=("gray75", "gray30"), command=toggle_password)
btn_show.grid(row=3, column=2, padx=5, pady=10)

btn_generate = customtkinter.CTkButton(window, text="Generate", width=60, command=generate_password)
btn_generate.grid(row=3, column=3, padx=(5, 0), pady=10)


# --- ROW 4: Add Button (Full Width) ---
btn_add = customtkinter.CTkButton(window, text="Save Password", height=40, font=("Arial", 15, "bold"), command=save)
btn_add.grid(row=4, column=1, columnspan=3, padx=(0, 0), pady=(20, 0), sticky="ew")

window.mainloop()