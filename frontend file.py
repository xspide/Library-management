import sqlite3
from datetime import datetime

class LibraryManagementSystem:
    def __init__(self, db_name='library.db'):
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
