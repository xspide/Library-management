-- books table
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    available INTEGER NOT NULL
);

-- members table
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- transactions table
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date TEXT NOT NULL,
    return_date TEXT,
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);
import sqlite3
from datetime import datetime

class LibraryManagementSystem:
    def _init_(self, db_name='library.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    available INTEGER NOT NULL
                )"""
            )
            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )"""
            )
            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER NOT NULL,
                    book_id INTEGER NOT NULL,
                    borrow_date TEXT NOT NULL,
                    return_date TEXT,
                    FOREIGN KEY (member_id) REFERENCES members(id),
                    FOREIGN KEY (book_id) REFERENCES books(id)
                )"""
            )

    def add_book(self, title, author, genre):
        with self.connection:
            self.connection.execute(
                "INSERT INTO books (title, author, genre, available) VALUES (?, ?, ?, ?)",
                (title, author, genre, 1)
            )

    def add_member(self, name, email, password):
        with self.connection:
            self.connection.execute(
                "INSERT INTO members (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )

    def borrow_book(self, member_id, book_id):
        with self.connection:
            book = self.connection.execute(
                "SELECT available FROM books WHERE id = ?", (book_id,)
            ).fetchone()
            if book and book[0] == 1:
                self.connection.execute(
                    "UPDATE books SET available = 0 WHERE id = ?", (book_id,)
                )
                self.connection.execute(
                    "INSERT INTO transactions (member_id, book_id, borrow_date) VALUES (?, ?, ?)",
                    (member_id, book_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
            else:
                raise Exception("Book is not available")

    def return_book(self, member_id, book_id):
        with self.connection:
            self.connection.execute(
                "UPDATE books SET available = 1 WHERE id = ?", (book_id,)
            )
            self.connection.execute(
                "UPDATE transactions SET return_date = ? WHERE member_id = ? AND book_id = ? AND return_date IS NULL",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), member_id, book_id)
            )

    def get_books(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM books").fetchall()

    def get_members(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM members").fetchall()

    def get_transactions(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM transactions").fetchall()

if _name_ == "_main_":
    lms = LibraryManagementSystem()
    lms.add_book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction")
    lms.add_member("John Doe", "john@example.com", "password123")
    lms.borrow_book(1, 1)
    print(lms.get_books())
    print(lms.get_members())
    print(lms.get_transactions())
    lms.return_book(1, 1)
    print(lms.get_transactions())
import tkinter as tk
from tkinter import messagebox
from library_management import LibraryManagementSystem

class LibraryApp:
    def _init_(self, root):
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
        title = tk.simpledialog.askstring("Title", "Enter book title:")
        author = tk.simpledialog.askstring("Author", "Enter book author:")
        genre = tk.simpledialog.askstring("Genre", "Enter book genre:")
        if title and author and genre:
            self.lms.add_book(title, author, genre)
            messagebox.showinfo("Success", "Book added successfully")

    def add_member(self):
        name = tk.simpledialog.askstring("Name", "Enter member name:")
        email = tk.simpledialog.askstring("Email", "Enter member email:")
        password = tk.simpledialog.askstring("Password", "Enter member password:")
        if name and email and password:
            self.lms.add_member(name, email, password)
            messagebox.showinfo("Success", "Member added successfully")

    def borrow_book(self):
        member_id = tk.simpledialog.askinteger("Member ID", "Enter member ID:")
        book_id = tk.simpledialog.askinteger("Book ID", "Enter book ID:")
        if member_id and book_id:
            try:
                self.lms.borrow_book(member_id, book_id)
                messagebox.showinfo("Success", "Book borrowed successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def return_book(self):
        member_id = tk.simpledialog.askinteger("Member ID", "Enter member ID:")
        book_id = tk.simpledialog.askinteger("Book ID", "Enter book ID:")
        if member_id and book_id:
            self.lms.return_book(member_id, book_id)
            messagebox.showinfo("Success", "Book returned successfully")

    def view_books(self):
        books = self.lms.get_books()
        book_list = "\n".join([f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Available: {book[4]}" for book in books])
        messagebox.showinfo("Books", book_list)

if _name_ == "_main_":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
