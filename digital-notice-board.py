import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ---------------- DATABASE ----------------
conn = sqlite3.connect("advanced_notice.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS notices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    category TEXT,
    priority TEXT,
    audience TEXT,
    content TEXT,
    date TEXT,
    views INTEGER DEFAULT 0
)
""")
conn.commit()

# ---------------- USERS ----------------
users = {
    "admin": "admin123",
    "hod": "hod123",
    "faculty": "fac123",
    "student": "stud123"
}

# ---------------- LOGIN ----------------
def login():
    if users.get(user_entry.get()) == pass_entry.get():
        open_dashboard(user_entry.get())
    else:
        messagebox.showerror("Error", "Invalid Login")

# ---------------- DASHBOARD ----------------
def open_dashboard(role):

    for w in root.winfo_children():
        w.destroy()

    root.title("Central Digital Notice Board")
    root.geometry("900x600")
    root.config(bg="#0F172A")

    def add_notice():
        if not content.get().strip():
            messagebox.showwarning("Warning", "Enter notice content")
            return

        cursor.execute("""
        INSERT INTO notices (role, category, priority, audience, content, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (role, cat.get(), pri.get(), aud.get(),
              content.get(), datetime.now().strftime("%d-%m-%Y %H:%M")))
        conn.commit()
        load_notices()
        content.delete(0, tk.END)

    def load_notices():
        notice_list.delete(0, tk.END)
        for row in cursor.execute("SELECT * FROM notices ORDER BY id DESC"):
            color = "#EF4444" if row[3] == "Urgent" else "#F1F5F9"
            notice_list.insert(tk.END,
                f"{row[0]}. [{row[3]}] {row[5]} - {row[6]}")
            notice_list.itemconfig(tk.END, fg=color)

    def delete_notice():
        sel = notice_list.curselection()
        if sel:
            notice_id = notice_list.get(sel[0]).split(".")[0]
            cursor.execute("DELETE FROM notices WHERE id=?", (notice_id,))
            conn.commit()
            load_notices()
        else:
            messagebox.showwarning("Warning", "Select a notice")

    tk.Label(root,
             text=f"CENTRAL DIGITAL NOTICE BOARD ({role.upper()})",
             font=("Times", 20, "bold"),
             bg="#0F172A",
             fg="#F1F5F9").pack(pady=15)

    card = tk.Frame(root, bg="#1E293B")
    card.pack(pady=10, padx=20, fill="both", expand=True)

    # Show controls only if not student
    if role != "student":
        content = tk.Entry(card, width=50)
        content.pack(pady=5)

        cat = tk.StringVar(value="Academic")
        pri = tk.StringVar(value="General")
        aud = tk.StringVar(value="Whole Campus")

        for var, options in [
            (cat, ["Academic", "Exams", "Placements", "Cultural", "Sports", "Circular"]),
            (pri, ["Urgent", "Important", "General"]),
            (aud, ["Department", "Year", "Whole Campus"])
        ]:
            tk.OptionMenu(card, var, *options).pack(pady=3)

        tk.Button(card, text="Add Notice", bg="#3B82F6",
                  fg="white", command=add_notice).pack(pady=5)

        tk.Button(card, text="Delete Notice", bg="#EF4444",
                  fg="white", command=delete_notice).pack(pady=5)

    notice_list = tk.Listbox(card, width=100, height=20,
                             bg="#1E293B", fg="#F1F5F9",
                             selectbackground="#3B82F6")
    notice_list.pack(pady=10)

    load_notices()

# ---------------- LOGIN WINDOW ----------------
root = tk.Tk()
root.title("Login - Digital Notice Board")
root.geometry("400x300")
root.config(bg="#F4E1C1")

tk.Label(root, text="LOGIN",
         font=("Palatino Linotype", 20, "bold"),
         bg="#F4E1C1").pack(pady=20)

tk.Label(root, text="Username", bg="#F4E1C1").pack()
user_entry = tk.Entry(root)
user_entry.pack()

tk.Label(root, text="Password", bg="#F4E1C1").pack()
pass_entry = tk.Entry(root, show="*")
pass_entry.pack()

tk.Button(root, text="Login",
          bg="#3B82F6", fg="white",
          command=login).pack(pady=20)

root.mainloop()