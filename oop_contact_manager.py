import tkinter as tk
from tkinter import messagebox

# Step 1: Define the Contact class
class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, Email: {self.email}"

    def __eq__(self, other):
        if isinstance(other, Contact):
            return self.name == other.name and self.phone == other.phone and self.email == other.email
        return False

    def __hash__(self):
        return hash((self.name, self.phone, self.email))

# Step 2: Define the AddressBook class
class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def update_contact(self, old_contact, new_contact):
        index = self.contacts.index(old_contact)
        self.contacts[index] = new_contact

    def delete_contact(self, contact):
        self.contacts.remove(contact)

    def get_contacts(self):
        return self.contacts

# Step 3: Define the ContactForm class
class ContactForm:
    def __init__(self, parent, submit_callback):
        self.frame = tk.Frame(parent)
        self.frame.pack()

        self.name_label = tk.Label(self.frame, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1)

        self.phone_label = tk.Label(self.frame, text="Phone:")
        self.phone_label.grid(row=1, column=0)
        self.phone_entry = tk.Entry(self.frame)
        self.phone_entry.grid(row=1, column=1)

        self.email_label = tk.Label(self.frame, text="Email:")
        self.email_label.grid(row=2, column=0)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=2, column=1)

        self.submit_button = tk.Button(self.frame, text="Submit", command=submit_callback)
        self.submit_button.grid(row=3, column=0, columnspan=2)

    def get_contact_data(self):
        return Contact(self.name_entry.get(), self.phone_entry.get(), self.email_entry.get())

    def set_contact_data(self, contact):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, contact.name)
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, contact.phone)
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, contact.email)

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

# Step 4: Define the ContactList class
class ContactList:
    def __init__(self, parent, select_callback):
        self.frame = tk.Frame(parent)
        self.frame.pack()

        self.listbox = tk.Listbox(self.frame, width=50)
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', lambda event: select_callback(self.get_selected_contact()))

    def update_list(self, contacts):
        self.listbox.delete(0, tk.END)
        for contact in contacts:
            self.listbox.insert(tk.END, str(contact))

    def get_selected_contact(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_contact_str = self.listbox.get(selected_index)
            contact_data = selected_contact_str.split(", ")
            return Contact(
                name=contact_data[0].split(": ")[1],
                phone=contact_data[1].split(": ")[1],
                email=contact_data[2].split(": ")[1]
            )
        return None

# Step 5: Define the ContactApp class
class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        self.address_book = AddressBook()

        self.contact_form = ContactForm(root, self.submit_contact)
        self.contact_list = ContactList(root, self.load_contact_into_form)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack()

    def submit_contact(self):
        new_contact = self.contact_form.get_contact_data()
        selected_contact = self.contact_list.get_selected_contact()

        if selected_contact:
            self.address_book.update_contact(selected_contact, new_contact)
        else:
            self.address_book.add_contact(new_contact)

        self.contact_form.clear_form()
        self.refresh_contact_list()

    def load_contact_into_form(self, contact):
        if contact:
            self.contact_form.set_contact_data(contact)

    def delete_contact(self):
        selected_contact = self.contact_list.get_selected_contact()
        if selected_contact:
            try:
                self.address_book.delete_contact(selected_contact)
                self.refresh_contact_list()
                self.contact_form.clear_form()
            except ValueError:
                messagebox.showerror("Error", "Contact not found in list.")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def refresh_contact_list(self):
        contacts = self.address_book.get_contacts()
        self.contact_list.update_list(contacts)

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
