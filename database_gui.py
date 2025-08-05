import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import credentials

print("DISPLAY environment variable:", os.environ.get("DISPLAY"))

class DatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("COMP353 Project – Volleyball Club System")
        self.root.geometry("800x600")
        self.root.option_add('*tearOff', False)

        # --- MENU BAR ---
        menubar = tk.Menu(self.root)
        self.tables_menu   = tk.Menu(menubar)
        self.queries_menu  = tk.Menu(menubar)
        self.data_ops_menu = tk.Menu(menubar)
        self.exit_menu     = tk.Menu(menubar)

        menubar.add_cascade(label="Tables",        menu=self.tables_menu)
        menubar.add_cascade(label="Queries",       menu=self.queries_menu)
        menubar.add_cascade(label="Data Operations", menu=self.data_ops_menu)
        menubar.add_cascade(label="Exit",          menu=self.exit_menu)
        self.root.config(menu=menubar)

        # Connect & populate tables
        self.conn = None
        self.cursor = None
        self.current_table = None
        self.connect_to_database()
        if self.conn and self.conn.is_connected():
            self.populate_tables_menu(self.tables_menu)
        else:
            self.tables_menu.add_command(
                label="Database Not Connected",
                command=lambda: messagebox.showerror(
                    "Error", "Cannot access tables: Database connection failed"
                )
            )

        # Queries menu: fixed indexing & column fetch
        for i, _ in enumerate(credentials.queries, start=1):
            self.queries_menu.add_command(
                label=f"Query {i}",
                command=lambda x=i: self.execute_query(x)
            )

        # Data Operations: Insert / Update / Delete
        self.data_ops_menu.add_command(label="Insert Record", command=self.insert_record)
        self.data_ops_menu.add_command(label="Update Record", command=self.update_record)
        self.data_ops_menu.add_command(label="Delete Record", command=self.delete_record)

        # Exit
        self.exit_menu.add_command(label="Quit", command=self.show_exit)

        # --- MAIN CONTENT AREA ---
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True)

        # Welcome label (packed, not placed – no manager conflict)
        welcome_text = (
            "Welcome to Volleyball Club System (VCS)\n"
            "Please use the navigation bar for the different features"
        )
        self.welcome_label = ttk.Label(
            self.content_frame,
            text=welcome_text,
            font=("Arial", 20),
            justify="center"
        )
        self.welcome_label.pack(fill="both", expand=True)

        # Data TreeView (hidden initially)
        self.data_frame = ttk.Frame(self.content_frame)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.h_scrollbar = ttk.Scrollbar(
            self.data_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(xscrollcommand=self.h_scrollbar.set)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    def connect_to_database(self):
        try:
            print(f"Connecting to MySQL: host={credentials.host}, user={credentials.user}")
            self.conn = mysql.connector.connect(
                host=credentials.host,
                user=credentials.user,
                password=credentials.password,
                database=credentials.database
            )
            self.cursor = self.conn.cursor()
            print("MySQL connection successful")
        except mysql.connector.Error as e:
            print("Connection error:", e)
            messagebox.showerror("Database Error", f"Failed to connect: {e}")

    def populate_tables_menu(self, menu):
        menu.delete(0, 'end')
        try:
            self.cursor.execute("SHOW TABLES")
            for (table_name,) in self.cursor.fetchall():
                menu.add_command(
                    label=table_name,
                    command=lambda x=table_name: self.show_table_data(x)
                )
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch tables: {e}")

    def show_table_data(self, table_name):
        # Track which table we're working on
        self.current_table = table_name

        # Switch views
        if self.welcome_label.winfo_ismapped():
            self.welcome_label.pack_forget()
        if not self.data_frame.winfo_ismapped():
            self.data_frame.pack(fill="both", expand=True)

        # Clear old rows
        self.tree.delete(*self.tree.get_children())

        # Fetch & display
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [col[0] for col in self.cursor.fetchall()]

            self.tree["columns"] = columns
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="w", minwidth=50)

            if rows:
                for row in rows:
                    self.tree.insert("", "end", values=row)
            else:
                self.tree.insert("", "end", values=("No data available",))

        except mysql.connector.Error as e:
            messagebox.showerror("Query Error", f"Failed to query {table_name}: {e}")

    def execute_query(self, n):
        if self.welcome_label.winfo_ismapped():
            self.welcome_label.pack_forget()
        if not self.data_frame.winfo_ismapped():
            self.data_frame.pack(fill="both", expand=True)

        query = credentials.queries[n - 1]
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            cols = [desc[0] for desc in self.cursor.description]

            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = cols
            for c in cols:
                self.tree.heading(c, text=c)
                self.tree.column(c, width=100, anchor="w", minwidth=50)

            if rows:
                for row in rows:
                    self.tree.insert("", "end", values=row)
            else:
                self.tree.insert("", "end", values=("No data available",))

        except mysql.connector.Error as e:
            messagebox.showerror("Query Error", f"Failed to execute Query {n}: {e}")

    def insert_record(self):
        if not self.current_table:
            return messagebox.showerror("Error", "Please select a table first.")
        # Get column metadata
        self.cursor.execute(f"SHOW COLUMNS FROM {self.current_table}")
        cols = self.cursor.fetchall()
        # Exclude AUTO_INCREMENT
        fields = [col[0] for col in cols if "auto_increment" not in col[5]]

        form = tk.Toplevel(self.root)
        form.title(f"Insert into {self.current_table}")
        entries = {}
        for i, name in enumerate(fields):
            ttk.Label(form, text=name).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            ent = ttk.Entry(form)
            ent.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entries[name] = ent

        def do_insert():
            vals = [entries[f].get() or None for f in fields]
            sql = f"INSERT INTO {self.current_table} ({','.join(fields)}) VALUES ({','.join(['%s']*len(fields))})"
            try:
                self.cursor.execute(sql, vals)
                self.conn.commit()
                messagebox.showinfo("Success", "Record inserted.")
                form.destroy()
                self.show_table_data(self.current_table)
            except mysql.connector.Error as e:
                messagebox.showerror("Insert Error", str(e))

        ttk.Button(form, text="Insert", command=do_insert).grid(
            row=len(fields), column=0, columnspan=2, pady=10
        )

    def update_record(self):
        if not self.current_table:
            return messagebox.showerror("Error", "Please select a table first.")
        sel = self.tree.focus()
        if not sel:
            return messagebox.showerror("Error", "Select a row to update.")
        values = self.tree.item(sel)["values"]
        cols = self.tree["columns"]

        # Identify primary key
        self.cursor.execute(f"SHOW COLUMNS FROM {self.current_table}")
        meta = self.cursor.fetchall()
        pk = next((col[0] for col in meta if col[3] == "PRI"), cols[0])
        pk_idx = cols.index(pk)

        form = tk.Toplevel(self.root)
        form.title(f"Update {self.current_table}")
        entries = {}
        for i, col in enumerate(cols):
            ttk.Label(form, text=col).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            ent = ttk.Entry(form)
            ent.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            ent.insert(0, values[i])
            if col == pk:
                ent.config(state="disabled")
            entries[col] = ent

        def do_update():
            assignments = []
            params = []
            for col, ent in entries.items():
                if col == pk:
                    continue
                assignments.append(f"{col} = %s")
                params.append(ent.get())
            params.append(values[pk_idx])
            sql = f"UPDATE {self.current_table} SET {', '.join(assignments)} WHERE {pk} = %s"
            try:
                self.cursor.execute(sql, params)
                self.conn.commit()
                messagebox.showinfo("Success", "Record updated.")
                form.destroy()
                self.show_table_data(self.current_table)
            except mysql.connector.Error as e:
                messagebox.showerror("Update Error", str(e))

        ttk.Button(form, text="Update", command=do_update).grid(
            row=len(cols), column=0, columnspan=2, pady=10
        )

    def delete_record(self):
        if not self.current_table:
            return messagebox.showerror("Error", "Please select a table first.")
        sel = self.tree.focus()
        if not sel:
            return messagebox.showerror("Error", "Select a row to delete.")
        values = self.tree.item(sel)["values"]
        cols = self.tree["columns"]

        self.cursor.execute(f"SHOW COLUMNS FROM {self.current_table}")
        meta = self.cursor.fetchall()
        pk = next((col[0] for col in meta if col[3] == "PRI"), cols[0])
        pk_idx = cols.index(pk)
        pk_val = values[pk_idx]

        if not messagebox.askyesno("Confirm Delete", f"Delete {self.current_table} where {pk}={pk_val}?"):
            return

        try:
            self.cursor.execute(
                f"DELETE FROM {self.current_table} WHERE {pk} = %s", (pk_val,)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Record deleted.")
            self.show_table_data(self.current_table)
        except mysql.connector.Error as e:
            messagebox.showerror("Delete Error", str(e))

    def show_exit(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to quit?"):
            if self.conn and self.conn.is_connected():
                self.conn.close()
            self.root.quit()

# Global exception hook
import sys
def handle_exception(exc_type, exc_value, exc_traceback):
    print("Uncaught exception:", exc_type, exc_value)
sys.excepthook = handle_exception

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseGUI(root)
    root.mainloop()
