import mysql.connector
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os


load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

temp_conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password
)
temp_cursor = temp_conn.cursor()
temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
temp_conn.close()

conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    isbn VARCHAR(50),
    total_copies INT,
    available_copies INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
)
""")


def add_book():
    title = entry_title.get()
    author = entry_author.get()
    isbn = entry_isbn.get()
    copies = entry_copies.get()

    if not (title and author and isbn and copies):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        sql = """INSERT INTO books 
                 (title, author, isbn, total_copies, available_copies) 
                 VALUES (%s, %s, %s, %s, %s)"""
        values = (title, author, isbn, int(copies), int(copies))
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")

        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        entry_isbn.delete(0, tk.END)
        entry_copies.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


def register_member():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()

    if not (name and email and phone):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        sql = "INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)"
        values = (name, email, phone)
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Success", "Member registered successfully!")

        frame_register.pack_forget()
        frame_book.pack(fill="both", expand="yes", padx=10, pady=10)
        frame_view.pack(fill="both", expand="yes", padx=10, pady=10)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


def login_member():
    email = login_email.get()
    phone = login_phone.get()

    if not (email and phone):
        messagebox.showerror("Error", "Both fields are required!")
        return

    cursor.execute("SELECT * FROM members WHERE email=%s AND phone=%s", (email, phone))
    member = cursor.fetchone()
    if member:
        messagebox.showinfo("Success", f"Welcome back, {member[1]}!")
        frame_login.pack_forget()
        frame_book.pack(fill="both", expand="yes", padx=10, pady=10)
        frame_view.pack(fill="both", expand="yes", padx=10, pady=10)
    else:
        messagebox.showerror("Error", "No account found. Please register.")
        frame_login.pack_forget()
        frame_register.pack(fill="both", expand="yes", padx=10, pady=10)


def view_books():
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    text_output.delete("1.0", tk.END)
    for row in rows:
        text_output.insert(tk.END, f"{row}\n")


def view_inventory():
    cursor.execute("SELECT title, total_copies, available_copies FROM books")
    rows = cursor.fetchall()
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, f"{'Title':<25} {'Total':<10} {'Available':<10}\n")
    text_output.insert(tk.END, "-"*55 + "\n")
    for row in rows:
        title, total, available = row
        text_output.insert(tk.END, f"{title:<25} {total:<10} {available:<10}\n")

root = tk.Tk()
root.title("📚 Library Management System")
root.geometry("650x650")
root.configure(bg="#ADD8E6")

TITLE_FONT = ("Helvetica", 18, "bold")
LABEL_FONT = ("Helvetica", 14)
BUTTON_FONT = ("Helvetica", 14, "bold")


frame_login = tk.Frame(root, bg="white", bd=4, relief="groove")
frame_login.pack(fill="both", expand="yes", padx=20, pady=20)

tk.Label(frame_login, text="🔑 Login Member", font=TITLE_FONT, bg="white").grid(row=0, column=0, columnspan=2, pady=15)

tk.Label(frame_login, text="Email:", font=LABEL_FONT, bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=10)
tk.Label(frame_login, text="Phone:", font=LABEL_FONT, bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=10)

login_email = tk.Entry(frame_login, font=LABEL_FONT, width=25)
login_phone = tk.Entry(frame_login, font=LABEL_FONT, width=25)

login_email.grid(row=1, column=1, padx=10, pady=10)
login_phone.grid(row=2, column=1, padx=10, pady=10)

tk.Button(frame_login, text="Login", command=login_member, bg="#87CEFA", font=BUTTON_FONT, width=18, height=2).grid(row=3, column=0, columnspan=2, pady=20)


frame_register = tk.Frame(root, bg="white", bd=4, relief="groove")

tk.Label(frame_register, text="📝 Register Member", font=TITLE_FONT, bg="white").grid(row=0, column=0, columnspan=2, pady=15)

tk.Label(frame_register, text="Name:", font=LABEL_FONT, bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=10)
tk.Label(frame_register, text="Email:", font=LABEL_FONT, bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=10)
tk.Label(frame_register, text="Phone:", font=LABEL_FONT, bg="white").grid(row=3, column=0, sticky="w", padx=10, pady=10)

entry_name = tk.Entry(frame_register, font=LABEL_FONT, width=25)
entry_email = tk.Entry(frame_register, font=LABEL_FONT, width=25)
entry_phone = tk.Entry(frame_register, font=LABEL_FONT, width=25)

entry_name.grid(row=1, column=1, padx=10, pady=10)
entry_email.grid(row=2, column=1, padx=10, pady=10)
entry_phone.grid(row=3, column=1, padx=10, pady=10)

tk.Button(frame_register, text="Register", command=register_member, bg="#90EE90", font=BUTTON_FONT, width=18, height=2).grid(row=4, column=0, columnspan=2, pady=20)


frame_book = tk.LabelFrame(root, text="Add Book", bg="white", font=TITLE_FONT, labelanchor="n")

tk.Label(frame_book, text="Title:", font=LABEL_FONT, bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=10)
tk.Label(frame_book, text="Author:", font=LABEL_FONT, bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=10)
tk.Label(frame_book, text="ISBN:", font=LABEL_FONT, bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=10)
tk.Label(frame_book, text="Copies:", font=LABEL_FONT, bg="white").grid(row=3, column=0, sticky="w", padx=10, pady=10)

entry_title = tk.Entry(frame_book, font=LABEL_FONT, width=25)
entry_author = tk.Entry(frame_book, font=LABEL_FONT, width=25)
entry_isbn = tk.Entry(frame_book, font=LABEL_FONT, width=25)
entry_copies = tk.Entry(frame_book, font=LABEL_FONT, width=25)

entry_title.grid(row=0, column=1, padx=10, pady=10)
entry_author.grid(row=1, column=1, padx=10, pady=10)
entry_isbn.grid(row=2, column=1, padx=10, pady=10)
entry_copies.grid(row=3, column=1, padx=10, pady=10)

tk.Button(frame_book, text="Add Book", command=add_book, bg="#90EE90", font=BUTTON_FONT, width=18, height=2).grid(row=4, column=0, columnspan=2, pady=20)


frame_view = tk.LabelFrame(root, text="View Books", bg="white", font=TITLE_FONT, labelanchor="n")

tk.Button(frame_view, text="Show All Books", command=view_books, bg="#87CEFA", font=BUTTON_FONT, width=25, height=2).pack(pady=10)
tk.Button(frame_view, text="Show Inventory (Manager)", command=view_inventory, bg="#FFB6C1", font=BUTTON_FONT, width=25, height=2).pack(pady=10)

text_output = tk.Text(frame_view, height=12, font=("Courier", 12), bg="#FFFACD")
text_output.pack(padx=10, pady=10, fill="both", expand=True)

def on_close():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()




