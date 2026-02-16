import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "database.db"


# =========================
# Připojení k databázi
# =========================
def connect_db():
    return sqlite3.connect(DB_NAME)


# =========================
# Inicializace databáze
# =========================
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS akce (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazev TEXT NOT NULL,
            datum TEXT NOT NULL,
            misto TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ucastnici (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jmeno TEXT NOT NULL,
            trida TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrace (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            akce_id INTEGER,
            ucastnik_id INTEGER,
            FOREIGN KEY (akce_id) REFERENCES akce(id),
            FOREIGN KEY (ucastnik_id) REFERENCES ucastnici(id)
        )
    """)

    conn.commit()
    conn.close()


# =========================
# Hlavní aplikace
# =========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Správa akcí a registrací")
        self.root.geometry("900x600")

        self.create_widgets()
        self.load_data()

    # =========================
    # GUI rozložení
    # =========================
    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        # Záložky
        self.tab_akce = ttk.Frame(notebook)
        self.tab_ucastnici = ttk.Frame(notebook)
        self.tab_registrace = ttk.Frame(notebook)

        notebook.add(self.tab_akce, text="Akce")
        notebook.add(self.tab_ucastnici, text="Účastníci")
        notebook.add(self.tab_registrace, text="Registrace")

        self.create_akce_tab()
        self.create_ucastnici_tab()
        self.create_registrace_tab()

    # =========================
    # ZÁLOŽKA AKCE (CREATE + READ)
    # =========================
    def create_akce_tab(self):
        frame = ttk.LabelFrame(self.tab_akce, text="Vytvoření akce")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Název:").grid(row=0, column=0, padx=5, pady=5)
        self.nazev_entry = ttk.Entry(frame)
        self.nazev_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Datum:").grid(row=0, column=2, padx=5, pady=5)
        self.datum_entry = ttk.Entry(frame)
        self.datum_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Místo:").grid(row=0, column=4, padx=5, pady=5)
        self.misto_entry = ttk.Entry(frame)
        self.misto_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(frame, text="Vytvořit akci", command=self.add_akce).grid(
            row=0, column=6, padx=10
        )

        # Treeview
        self.akce_tree = ttk.Treeview(
            self.tab_akce,
            columns=("ID", "Název", "Datum", "Místo"),
            show="headings"
        )
        for col in ("ID", "Název", "Datum", "Místo"):
            self.akce_tree.heading(col, text=col)

        self.akce_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_akce(self):
        nazev = self.nazev_entry.get().strip()
        datum = self.datum_entry.get().strip()
        misto = self.misto_entry.get().strip()

        if not nazev or not datum or not misto:
            messagebox.showerror("Chyba", "Vyplňte všechna pole!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO akce (nazev, datum, misto) VALUES (?, ?, ?)",
            (nazev, datum, misto)
        )
        conn.commit()
        conn.close()

        self.load_akce()
        self.nazev_entry.delete(0, tk.END)
        self.datum_entry.delete(0, tk.END)
        self.misto_entry.delete(0, tk.END)

    def load_akce(self):
        for row in self.akce_tree.get_children():
            self.akce_tree.delete(row)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM akce")
        for row in cursor.fetchall():
            self.akce_tree.insert("", tk.END, values=row)
        conn.close()

    # =========================
    # ZÁLOŽKA ÚČASTNÍCI (CRUD + FILTR)
    # =========================
    def create_ucastnici_tab(self):
        frame = ttk.LabelFrame(self.tab_ucastnici, text="Registrace účastníků")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Jméno:").grid(row=0, column=0, padx=5, pady=5)
        self.jmeno_entry = ttk.Entry(frame)
        self.jmeno_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Třída:").grid(row=0, column=2, padx=5, pady=5)
        self.trida_entry = ttk.Entry(frame)
        self.trida_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(frame, text="Přidat účastníka", command=self.add_ucastnik).grid(
            row=0, column=4, padx=10
        )

        # Filtr
        filter_frame = ttk.Frame(self.tab_ucastnici)
        filter_frame.pack(fill="x", padx=10)

        ttk.Label(filter_frame, text="Filtr podle třídy:").pack(side="left")
        self.filter_entry = ttk.Entry(filter_frame)
        self.filter_entry.pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Filtrovat", command=self.filter_ucastnici).pack(side="left")
        ttk.Button(filter_frame, text="Zobrazit vše", command=self.load_ucastnici).pack(side="left", padx=5)

        self.ucastnici_tree = ttk.Treeview(
            self.tab_ucastnici,
            columns=("ID", "Jméno", "Třída"),
            show="headings"
        )
        for col in ("ID", "Jméno", "Třída"):
            self.ucastnici_tree.heading(col, text=col)

        self.ucastnici_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_ucastnik(self):
        jmeno = self.jmeno_entry.get().strip()
        trida = self.trida_entry.get().strip()

        if not jmeno or not trida:
            messagebox.showerror("Chyba", "Vyplňte jméno a třídu!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ucastnici (jmeno, trida) VALUES (?, ?)",
            (jmeno, trida)
        )
        conn.commit()
        conn.close()

        self.load_ucastnici()
        self.jmeno_entry.delete(0, tk.END)
        self.trida_entry.delete(0, tk.END)

    def load_ucastnici(self):
        for row in self.ucastnici_tree.get_children():
            self.ucastnici_tree.delete(row)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ucastnici")
        for row in cursor.fetchall():
            self.ucastnici_tree.insert("", tk.END, values=row)
        conn.close()

    def filter_ucastnici(self):
        trida = self.filter_entry.get().strip()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ucastnici WHERE trida LIKE ?", (f"%{trida}%",))
        rows = cursor.fetchall()
        conn.close()

        for row in self.ucastnici_tree.get_children():
            self.ucastnici_tree.delete(row)

        for row in rows:
            self.ucastnici_tree.insert("", tk.END, values=row)

    # =========================
    # ZÁLOŽKA REGISTRACE (VAZBY + DELETE)
    # =========================
    def create_registrace_tab(self):
        frame = ttk.LabelFrame(self.tab_registrace, text="Registrace na akci")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="ID Akce:").grid(row=0, column=0, padx=5, pady=5)
        self.akce_id_entry = ttk.Entry(frame)
        self.akce_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="ID Účastníka:").grid(row=0, column=2, padx=5, pady=5)
        self.ucastnik_id_entry = ttk.Entry(frame)
        self.ucastnik_id_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(frame, text="Zaregistrovat", command=self.add_registrace).grid(
            row=0, column=4, padx=10
        )

        ttk.Button(frame, text="Smazat registraci", command=self.delete_registrace).grid(
            row=0, column=5, padx=10
        )

        self.reg_tree = ttk.Treeview(
            self.tab_registrace,
            columns=("ID", "Akce ID", "Účastník ID"),
            show="headings"
        )
        for col in ("ID", "Akce ID", "Účastník ID"):
            self.reg_tree.heading(col, text=col)

        self.reg_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_registrace(self):
        akce_id = self.akce_id_entry.get().strip()
        ucastnik_id = self.ucastnik_id_entry.get().strip()

        if not akce_id.isdigit() or not ucastnik_id.isdigit():
            messagebox.showerror("Chyba", "ID musí být číslo!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO registrace (akce_id, ucastnik_id) VALUES (?, ?)",
            (akce_id, ucastnik_id)
        )
        conn.commit()
        conn.close()

        self.load_registrace()

    def load_registrace(self):
        for row in self.reg_tree.get_children():
            self.reg_tree.delete(row)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registrace")
        for row in cursor.fetchall():
            self.reg_tree.insert("", tk.END, values=row)
        conn.close()

    def delete_registrace(self):
        selected = self.reg_tree.selection()
        if not selected:
            messagebox.showerror("Chyba", "Vyber registraci k odstranění!")
            return

        reg_id = self.reg_tree.item(selected[0])["values"][0]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM registrace WHERE id = ?", (reg_id,))
        conn.commit()
        conn.close()

        self.load_registrace()

    # =========================
    # Načtení všech dat
    # =========================
    def load_data(self):
        self.load_akce()
        self.load_ucastnici()
        self.load_registrace()


# =========================
# Spuštění aplikace
# =========================
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
