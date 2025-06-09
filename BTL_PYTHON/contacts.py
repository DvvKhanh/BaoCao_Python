# contacts.py

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------------
# LỚP QUẢN LÝ DỮ LIỆU LIÊN HỆ
# -----------------------------
class ContactManager:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    self.contacts = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.contacts = []
        else:
            self.contacts = []

    def save_contacts(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.contacts, file, indent=4, ensure_ascii=False)

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def update_contact(self, index, new_contact):
        if 0 <= index < len(self.contacts):
            self.contacts[index] = new_contact
            self.save_contacts()

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            del self.contacts[index]
            self.save_contacts()

    def search_contacts(self, keyword):
        return [c for c in self.contacts if keyword.lower() in c["name"].lower()]

# -----------------------------
# GIAO DIỆN NGƯỜI DÙNG
# -----------------------------
class ContactApp:
    def __init__(self, root):
        self.manager = ContactManager()
        self.root = root
        self.root.title("Contact Manager")
        self.root.configure(bg="#f5f5f5")
        self.create_widgets()
        self.load_contacts()

    def create_widgets(self):
        frame = tk.LabelFrame(self.root, text="File Manager", padx=20, pady=10, bg="#f5f5f5", font=("Arial", 10, "bold"))
        frame.pack(pady=10)

        tk.Label(frame, text="Name", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        tk.Label(frame, text="Phone", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        tk.Label(frame, text="Email", font=("Arial", 10), bg="#f5f5f5").grid(row=2, column=0, sticky="e", pady=5, padx=5)

        self.name_entry = tk.Entry(frame, font=("Arial", 10), width=30)
        self.phone_entry = tk.Entry(frame, font=("Arial", 10), width=30)
        self.email_entry = tk.Entry(frame, font=("Arial", 10), width=30)

        self.name_entry.grid(row=0, column=1, pady=5)
        self.phone_entry.grid(row=1, column=1, pady=5)
        self.email_entry.grid(row=2, column=1, pady=5)

        btn_frame = tk.Frame(frame, bg="#f5f5f5")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Add", width=12, bg="#4CAF50", fg="white", command=self.add_contact).grid(row=0, column=0, padx=8, pady=5)
        tk.Button(btn_frame, text="Edit", width=12, bg="#2196F3", fg="white", command=self.edit_contact).grid(row=0, column=1, padx=8, pady=5)
        tk.Button(btn_frame, text="First", width=12, bg="#FFC107", fg="black", command=self.select_first).grid(row=0, column=2, padx=8, pady=5)
        tk.Button(btn_frame, text="Delete", width=12, bg="#F43636", fg="white", command=self.delete_contact).grid(row=0, column=3, padx=8, pady=5)

        search_frame = tk.Frame(self.root, bg="#f5f5f5")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search by Name:", font=("Arial", 10), bg="#f5f5f5").pack(side=tk.LEFT, padx=(10, 5))
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", bg="#03A9F4", fg="white", command=self.search_contact).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Reset", bg="#B803F4", fg="white", command=self.load_contacts).pack(side=tk.LEFT, padx=5)


        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone", "Email"), show='headings', height=10)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_contacts(self):
        self.tree.delete(*self.tree.get_children())

        for contact in self.manager.contacts:
            self.tree.insert('', tk.END, values=(contact["name"], contact["phone"], contact["email"]))

    def add_contact(self):
        contact = self.get_form_data()
        if not contact["name"]:
            messagebox.showwarning("Warning", "Vui lòng nhập thông tin")
            return
        self.manager.add_contact(contact)
        self.load_contacts()
        self.clear_fields()

    def edit_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Vui nhập chọn một liên hệ để chỉnh sửa.")
            return
        index = self.tree.index(selected[0])
        contact = self.get_form_data()
        self.manager.update_contact(index, contact)
        self.load_contacts()

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Vui lòng chọn một liên hệ để xóa.")
            return
        index = self.tree.index(selected[0])
        self.manager.delete_contact(index)
        self.load_contacts()
        self.clear_fields()

    def select_first(self):
        children = self.tree.get_children()
        if not children:
            messagebox.showinfo("Info", "No contacts to select.")
            return
        self.tree.selection_set(children[0])
        self.tree.focus(children[0])
        self.tree.see(children[0])
        self.on_select(None)

    def search_contact(self):
        name = self.search_entry.get().strip().lower()
        if not name:
            messagebox.showinfo("Info", "Vui lòng nhập tên để tìm kiếm.")
            return
        self.tree.delete(*self.tree.get_children())
        for contact in self.manager.contacts:

            if name in contact["name"].lower():
                self.tree.insert('', tk.END, values=(contact["name"], contact["phone"], contact["email"]))

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], 'values')
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[0])
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, values[1])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[2])

    def get_form_data(self):
        return {
            "name": self.name_entry.get().strip(),
            "phone": self.phone_entry.get().strip(),
            "email": self.email_entry.get().strip()
        }

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

# -----------------------------
# CHẠY CHƯƠNG TRÌNH
# -----------------------------
if __name__ == '__main__':
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
