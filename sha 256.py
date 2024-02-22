import tkinter as tk
import tkinter.filedialog
import hashlib
import os

class FileHashCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("File Hash Calculator")

        self.file_list = []

        # Create listbox to display files
        self.file_listbox = tk.Listbox(self.root, width=50, height=15)
        self.file_listbox.pack(pady=10)

        # Buttons
        self.add_button = tk.Button(self.root, text="Add Files", command=self.add_files)
        self.add_button.pack(side=tk.LEFT, padx=10)
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_files)
        self.clear_button.pack(side=tk.LEFT, padx=10)
        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate_hashes)
        self.calculate_button.pack(side=tk.LEFT, padx=10)
        self.save_button = tk.Button(self.root, text="Save Text", command=self.save_text)
        self.save_button.pack(side=tk.LEFT, padx=10)

        # Key bindings
        self.root.bind('<Delete>', self.delete_selected)

    def add_files(self):
        files = tkinter.filedialog.askopenfilenames()
        for file in files:
            self.file_list.append(file)
            self.file_listbox.insert(tk.END, file)

    def clear_files(self):
        self.file_list = []
        self.file_listbox.delete(0, tk.END)

    def delete_selected(self, event):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            for index in selected_indices[::-1]:
                del self.file_list[index]
                self.file_listbox.delete(index)

    def calculate_hashes(self):
        self.hash_dict = {}
        for file in self.file_list:
            try:
                with open(file, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                    self.hash_dict[file] = file_hash
            except Exception as e:
                print(f"Error calculating hash for {file}: {e}")

        # Clear listbox and display hash values
        self.file_listbox.delete(0, tk.END)
        for file, file_hash in self.hash_dict.items():
            self.file_listbox.insert(tk.END, f"{file} - {file_hash}")

    def save_text(self):
        if not self.hash_dict:
            return

        most_common_subfolder = os.path.commonpath(self.hash_dict.keys())
        save_filename = "file_hashes.txt"

        with open(save_filename, 'w') as f:
            for file, file_hash in self.hash_dict.items():
                folder, filename = os.path.split(file)
                relative_folder = os.path.relpath(folder, most_common_subfolder)
                f.write(f"{file_hash} * {relative_folder}/{filename}\n")

        print(f"File hashes saved to {save_filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileHashCalculator(root)
    root.mainloop()
