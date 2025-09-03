import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")

        # Variables
        self.length_var = tk.IntVar(value=12)
        self.include_letters = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        # Layout
        tk.Label(root, text="Password Length:").grid(row=0, column=0, sticky="w")
        tk.Spinbox(root, from_=4, to=64, textvariable=self.length_var, width=5).grid(row=0, column=1)

        tk.Checkbutton(root, text="Include Letters", variable=self.include_letters).grid(row=1, column=0, sticky="w")
        tk.Checkbutton(root, text="Include Numbers", variable=self.include_numbers).grid(row=2, column=0, sticky="w")
        tk.Checkbutton(root, text="Include Symbols", variable=self.include_symbols).grid(row=3, column=0, sticky="w")
        tk.Checkbutton(root, text="Exclude Ambiguous (e.g., O, 0, l, 1)", variable=self.exclude_ambiguous).grid(row=4, column=0, columnspan=2, sticky="w")

        tk.Button(root, text="Generate Password", command=self.generate_password).grid(row=5, column=0, columnspan=2, pady=10)

        self.password_entry = tk.Entry(root, width=40)
        self.password_entry.grid(row=6, column=0, columnspan=2, padx=5)

        tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=7, column=0, columnspan=2, pady=5)

    def generate_password(self):
        length = self.length_var.get()
        letters = self.include_letters.get()
        numbers = self.include_numbers.get()
        symbols = self.include_symbols.get()
        exclude_ambiguous = self.exclude_ambiguous.get()

        if not (letters or numbers or symbols):
            messagebox.showerror("Error", "Select at least one character type.")
            return

        # Define character sets
        char_sets = []
        if letters:
            char_sets.append(string.ascii_letters)
        if numbers:
            char_sets.append(string.digits)
        if symbols:
            char_sets.append(string.punctuation)

        # Exclude ambiguous characters if selected
        ambiguous_chars = 'O0l1I'
        if exclude_ambiguous:
            char_sets = [''.join(c for c in s if c not in ambiguous_chars) for s in char_sets]

        # Ensure at least one character from each selected set
        password_chars = [random.choice(s) for s in char_sets]

        # Fill the rest of the password length
        all_chars = ''.join(char_sets)
        if len(all_chars) == 0:
            messagebox.showerror("Error", "No characters available to generate password.")
            return

        password_chars += [random.choice(all_chars) for _ in range(length - len(password_chars))]

        # Shuffle to avoid predictable sequences
        random.shuffle(password_chars)

        password = ''.join(password_chars)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
