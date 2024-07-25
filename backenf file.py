import tkinter as tk
from tkinter import messagebox, simpledialog
from library_management import LibraryManagementSystem

class LibraryApp:
    def __init__(self, root):
        self.lms = LibraryManagementSystem()
        self.root = root
        self.root.title("Library Management System")
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.add_book_button = tk.Button(self.frame, text="Add Book", command=self.add_book)
        self.add_book_button.pack(side=tk.LEFT)

        self.add_member_button = tk.Button(self.frame, text="Add Member", command=self.add_member)
        self.add_member_button.pack(side=tk.LEFT)

        self.borrow_book_button = tk.Button(self.frame, text="Borrow Book", command=self.borrow_book)
        self.borrow_book_button.pack(side=tk.LEFT)

        self.return_book_button = tk.Button(self.frame, text="Return Book", command=self.return_book)
        self.return_book_button.pack(side=tk.LEFT)

        self.view_books_button = tk.Button(self.frame, text="View Books", command=self.view_books)
        self.view_books_button.pack(side=tk.LEFT)

    def add_book(self):
        title = simpledialog.askstring("Title", "Enter book title:")
        author = simpledialog.askstring("Author", "Enter book author:")
        genre = simpledialog.askstring("Genre", "Enter book genre:")
        if title and author and genre:
            self.lms.add_book(title, author, genre)
            messagebox.showinfo("Success", "Book added successfully")

    def add_member(self):
        name = simpledialog.askstring("Name", "Enter member name:")
        email = simpledialog.askstring("Email", "Enter member email:")
        password = simpledialog.askstring("Password", "Enter member password:")
        if name and email and password:
            self.lms.add_member(name, email, password)
            messagebox.showinfo("Success", "Member added successfully")

    def borrow_book(self):
        member_id = simpledialog.askinteger("Member ID", "Enter member ID:")
        book_id = simpledialog.askinteger("Book ID", "Enter book ID:")
        if member_id and book_id:
            try:
                self.lms.borrow_book(member_id, book_id)
                messagebox.showinfo("Success", "Book borrowed successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def return_book(self):
        member_id = simpledialog.askinteger("Member ID", "Enter member ID:")
        book_id = simpledialog.askinteger("Book ID", "Enter book ID:")
        if member_id and book_id:
            self.lms.return_book(member_id, book_id)
            messagebox.showinfo("Success", "Book returned successfully")

    def view_books(self):
        books = self.lms.get_books()
        book_list = "\n".join([f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Available: {book[4]}" for book in books])
        messagebox.showinfo("Books", book_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
