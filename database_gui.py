import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

import credentials


class DatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("COMP353 Project")
        self.root.geometry("800x600")

        # Disable tear-off menus as per TkDocs recommendation
        self.root.option_add('*tearOff', False)

        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create individual cascade menus
        self.tables_menu = tk.Menu(menubar, tearoff=0)
        self.queries_menu = tk.Menu(menubar, tearoff=0)
        self.modify_data_menu = tk.Menu(menubar, tearoff=0)
        self.make_payment_menu = tk.Menu(menubar, tearoff=0)
        self.assign_player_menu = tk.Menu(menubar, tearoff=0)
        self.exit_menu = tk.Menu(menubar, tearoff=0)

        self.recent_player = {}

        self.location_submenu = tk.Menu(self.modify_data_menu, tearoff=0)
        # Add cascade menus to menubar
        menubar.add_cascade(label="Tables", menu=self.tables_menu)
        menubar.add_cascade(label="Queries", menu=self.queries_menu)
        menubar.add_cascade(label="Modify Data", menu=self.modify_data_menu)

        menubar.add_cascade(label="Make Payment", menu=self.make_payment_menu)
        menubar.add_cascade(label="Assign Player", menu=self.assign_player_menu)

        menubar.add_cascade(label="Exit", menu=self.exit_menu)


        self.modify_data_menu.add_cascade(label="Location", menu=self.location_submenu)
        self.location_submenu.add_command(label="Create Location", command=self.add_location)
        self.location_submenu.add_command(label="Edit Location", command=self.edit_location)
        self.location_submenu.add_command(label="Delete Location", command=self.delete_location)


        self.personnel_submenu = tk.Menu(self.modify_data_menu, tearoff=0)
        self.modify_data_menu.add_cascade(label="Personnel", menu=self.personnel_submenu)
        self.personnel_submenu.add_command(label="Create Personnel", command=self.add_personnel)
        self.personnel_submenu.add_command(label="Edit Personnel", command=self.edit_personnel)
        self.personnel_submenu.add_command(label="Delete Personnel", command=self.delete_personnel)



        self.family_member_submenu = tk.Menu(self.modify_data_menu, tearoff=0)
        self.modify_data_menu.add_cascade(label="FamilyMember", menu=self.family_member_submenu)
        self.family_member_submenu.add_command(label="Create FamilyMember", command=self.add_family_member)
        self.family_member_submenu.add_command(label="Edit FamilyMember", command=self.edit_family_member)
        self.family_member_submenu.add_command(label="Delete FamilyMember", command=self.delete_family_member)


        self.club_member_submenu = tk.Menu(self.modify_data_menu, tearoff=0)
        self.modify_data_menu.add_cascade(label="ClubMember", menu=self.club_member_submenu)
        self.club_member_submenu.add_command(label="Create ClubMember", command=self.add_club_member)
        self.club_member_submenu.add_command(label="Edit ClubMember", command=self.edit_club_member)
        self.club_member_submenu.add_command(label="Delete ClubMember", command=self.delete_club_member)


        self.team_submenu = tk.Menu(self.modify_data_menu, tearoff=0)
        self.modify_data_menu.add_cascade(label="TeamFormation", menu=self.team_submenu)
        self.team_submenu.add_command(label="Create TeamFormation", command=self.add_team_formation)
        self.team_submenu.add_command(label="Edit TeamFormation", command=self.edit_team_formation)
        self.team_submenu.add_command(label="Delete TeamFormation", command=self.delete_team_formation)





        # Add commands to respective menus with lambda for proper binding
        # Populate Tables menu dynamically with table names (only if connected)
        self.conn = None
        self.cursor = None
        self.connect_to_database()
        if self.conn and self.conn.is_connected():
            try:
                self.cursor.execute("CALL send_weekly_session_emails()")
                self.conn.commit()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to send weekly session emails: {err}")
            self.populate_tables_menu(self.tables_menu)
        else:
            self.tables_menu.add_command(label="Database Not Connected", command=lambda: messagebox.showerror("Error",
                                                                                                              "Cannot access tables: Database connection failed"))


        for i in range(0,len(credentials.queries)):  # Example with 3 query buttons
            self.queries_menu.add_command(label=f"Query {i+1}", command=lambda x=i: self.execute_query(x))


        self.make_payment_menu.add_command(label="Make Payment", command=lambda: self.make_payment())
        self.assign_player_menu.add_command(label="Assign Player", command=lambda: self.assign_player())

        self.exit_menu.add_command(label="Quit", command=lambda: self.show_exit())


        # Single dynamic content frame
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True)

        # Welcome label (initially visible)
        welcome_text = "Welcome to Volleyball Club System(VCS)\nPlease use the navigation bar for the different features"
        self.welcome_label = ttk.Label(self.content_frame, text=welcome_text, font=("Arial", 20), justify="center")
        self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the label


        # Table data frame (hidden initially)
        self.data_frame = ttk.Frame(self.content_frame)
        self.tree = ttk.Treeview(self.data_frame, show="headings")
        self.h_scrollbar = ttk.Scrollbar(self.data_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.h_scrollbar.set)

        # Pack widgets for data frame
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    def connect_to_database(self):
        # Initialize MySQL database connection
        try:
            print("Trying to connect to database...")
            print(f"Credentials: host={credentials.host}, user={credentials.user}, database={credentials.database}")
            self.conn = mysql.connector.connect(
                host=credentials.host,
                user=credentials.user,
                password=credentials.password,
                database=credentials.database
            )
            self.cursor = self.conn.cursor()
            print("Connected to MySQL database successfully")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            messagebox.showerror("Database Error", f"Failed to connect to MySQL: {e}")

    def populate_tables_menu(self, menu):
        # Clear existing menu items
        menu.delete(0, 'end')
        # Fetch all table names from the database
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            for table in tables:
                table_name = table[0]
                menu.add_command(label=table_name, command=lambda x=table_name: self.show_table_data(x))
        except mysql.connector.Error as e:
            print(f"Error fetching tables: {e}")
            messagebox.showerror("Database Error", f"Failed to fetch tables: {e}")

    def show_table_data(self, table_name):
        if self.welcome_label.winfo_exists():
            self.welcome_label.pack_forget()
        if not self.data_frame.winfo_ismapped():
            self.data_frame.pack(fill="both", expand=True)

        # FULL reset
        self.clear_tree()

        print(f"Executing SELECT * FROM {table_name}")
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            results = self.cursor.fetchall()

            self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [col[0] for col in self.cursor.fetchall()]

            self.tree["columns"] = columns
            self.tree["displaycolumns"] = columns

            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor="w", minwidth=50)

            if results:
                for row in results:
                    self.tree.insert("", "end", values=row)
            else:
                self.tree.insert("", "end", values=("No data available",) * len(columns))

        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            messagebox.showerror("Query Error", f"Failed to query {table_name}: {e}")

    def clear_tree(self):
        # Clear all rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # First clear displaycolumns (must match or be empty before clearing columns)
        self.tree["displaycolumns"] = ()

        # Then clear columns
        self.tree["columns"] = ()

    def execute_query(self, query_number):
            # Hide welcome label and show data frame
            if self.welcome_label.winfo_exists():
                self.welcome_label.pack_forget()
            if not self.data_frame.winfo_ismapped():
                self.data_frame.pack(fill="both", expand=True)

            # Clear previous table content
            self.clear_tree()

            query = credentials.queries[query_number]
            if not query:
                messagebox.showerror("Error", f"No query defined for Query {query_number + 1}")
                return

            try:
                print(f"Executing Query {query_number}: {query}")
                self.cursor.execute(query)
                results = self.cursor.fetchall()

                # Get column names from query result
                columns = [desc[0] for desc in self.cursor.description]

                # Setup Treeview columns
                self.tree["columns"] = columns
                self.tree["displaycolumns"] = columns

                for col in columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=120, anchor="w", minwidth=50)

                # Insert data rows
                if results:
                    for row in results:
                        self.tree.insert("", "end", values=row)
                else:
                    self.tree.insert("", "end", values=("No data available",) * len(columns))

            except mysql.connector.Error as e:
                print(f"Error executing query: {e}")
                messagebox.showerror("Query Error", f"Failed to execute Query {query_number}: {e}")

        # Placeholder for query execution (to be expanded later)
        # You can add a specific query here and display results in the Treeview

    def show_add_data(self):
        print("Add Data function called")
        # Placeholder for adding data
        pass

    def show_exit(self):
        print("Exit function called")
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            print("User confirmed exit")
            if self.conn and self.conn.is_connected():
                self.conn.close()  # Close database connection
            self.root.quit()
            self.root.destroy()

    # ---Location ---
    def add_location(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add Location")

        fields = [
            ('name', ''), ('type', ''), ('phone_number', ''), ('web_address', ''),
            ('address', ''), ('city', ''), ('province', ''), ('postal_code', ''), ('max_capacity', '')
        ]
        entries = {}
        for i, (label, _) in enumerate(fields):
            tk.Label(add_win, text=label).grid(row=i, column=0)
            entry = tk.Entry(add_win)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def submit():
            values = [entries[label].get() for label, _ in fields]
            query = """
                INSERT INTO Location (name, type, phone_number, web_address, address, city, province, postal_code, max_capacity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            try:
                self.cursor.execute(query, values)
                self.conn.commit()
                messagebox.showinfo("Success", "Location added!")
                add_win.destroy()
                self.show_table_data("Location")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(add_win, text="Submit", command=submit).grid(row=len(fields), columnspan=2)

    def edit_location(self):
        # Step 1: Select location_id to edit
        select_win = tk.Toplevel(self.root)
        select_win.title("Select Location to Edit")

        tk.Label(select_win, text="Enter Location ID:").pack()
        id_entry = tk.Entry(select_win)
        id_entry.pack()

        def proceed():
            location_id = id_entry.get()
            # Step 2: Fetch existing data
            self.cursor.execute("SELECT * FROM Location WHERE location_id = %s", (location_id,))
            row = self.cursor.fetchone()
            if not row:
                messagebox.showerror("Error", f"No location found with ID {location_id}")
                select_win.destroy()
                return

            select_win.destroy()
            edit_win = tk.Toplevel(self.root)
            edit_win.title(f"Edit Location ID {location_id}")

            fields = [
                'name', 'type', 'phone_number', 'web_address',
                'address', 'city', 'province', 'postal_code', 'max_capacity'
            ]
            entries = {}
            for i, label in enumerate(fields):
                tk.Label(edit_win, text=label).grid(row=i, column=0)
                entry = tk.Entry(edit_win)
                entry.insert(0, row[i + 1])  # row[0] is location_id
                entry.grid(row=i, column=1)
                entries[label] = entry

            def save():
                values = [entries[label].get() for label in fields] + [location_id]
                query = """
                    UPDATE Location SET
                    name=%s, type=%s, phone_number=%s, web_address=%s, address=%s, city=%s, province=%s, postal_code=%s, max_capacity=%s
                    WHERE location_id=%s
                """
                try:
                    self.cursor.execute(query, values)
                    self.conn.commit()
                    messagebox.showinfo("Success", "Location updated!")

                    self.show_table_data("Location")
                    edit_win.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(edit_win, text="Save", command=save).grid(row=len(fields), columnspan=2)

        tk.Button(select_win, text="Next", command=proceed).pack()

    def delete_location(self):
        del_win = tk.Toplevel(self.root)
        del_win.title("Delete Location")

        tk.Label(del_win, text="Enter Location ID to Delete:").pack(pady=5)
        id_entry = tk.Entry(del_win)
        id_entry.pack(pady=5)

        def delete():
            location_id = id_entry.get().strip()

            # 1. Validate input
            if not location_id.isdigit():
                messagebox.showerror("Error", "Please enter a valid numeric Location ID")
                return

            # 2. Check if the record exists
            self.cursor.execute("SELECT location_id FROM Location WHERE location_id = %s", (location_id,))
            result = self.cursor.fetchone()
            if not result:
                messagebox.showerror("Error", f"No Location found with ID {location_id}")
                return  # Don't close window yet so they can retry

            # 3. Confirm deletion
            if not messagebox.askyesno("Confirm", f"Delete Location with ID {location_id}?"):
                return

            # 4. Perform deletion safely
            try:
                self.cursor.execute("DELETE FROM Location WHERE location_id = %s", (location_id,))
                self.conn.commit()
                messagebox.showinfo("Success", f"Location {location_id} deleted!")

                # Refresh table after success
                self.show_table_data("Location")
                del_win.destroy()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(del_win, text="Delete", command=delete).pack(pady=5)

    ## Personnel

    # --- Personnel ---
    def add_personnel(self):
        win = tk.Toplevel(self.root)
        win.title("Add Personnel")

        fields = ["person_id", "location_id", "start_date", "role", "mandate", "end_date"]
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(win, text=field).grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries[field] = entry

        def save():
            try:
                self.cursor.execute("INSERT IGNORE INTO Personnel (person_id) VALUES (%s)",
                                    (entries["person_id"].get(),))
                self.cursor.execute("""
                    INSERT INTO personnel_location (personnel_id, location_id, start_date, end_date, role, mandate)
                    VALUES (
                        (SELECT personnel_id FROM Personnel WHERE person_id=%s),
                        %s, %s, %s, %s, %s
                    )
                """, (
                    entries["person_id"].get(),
                    entries["location_id"].get(),
                    entries["start_date"].get(),
                    entries["end_date"].get() or None,
                    entries["role"].get(),
                    entries["mandate"].get()
                ))
                self.conn.commit()
                messagebox.showinfo("Success", "Personnel added!")
                win.destroy()
                self.show_table_data("personnel_location")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Save", command=save).grid(row=len(fields), columnspan=2, pady=10)

    def edit_personnel(self):
        win = tk.Toplevel(self.root)
        win.title("Edit Personnel")

        tk.Label(win, text="Personnel ID:").grid(row=0, column=0)
        pid_entry = tk.Entry(win)
        pid_entry.grid(row=0, column=1)

        def load():
            self.cursor.execute("""
                SELECT location_id, start_date, role, mandate, end_date
                FROM personnel_location WHERE personnel_id=%s
            """, (pid_entry.get(),))
            result = self.cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "No personnel found.")
                return

            labels = ["location_id", "start_date", "role", "mandate", "end_date"]
            entries = {}
            for i, label in enumerate(labels):
                tk.Label(win, text=label).grid(row=i + 1, column=0)
                entry = tk.Entry(win)
                entry.insert(0, result[i] if result[i] else "")
                entry.grid(row=i + 1, column=1)
                entries[label] = entry

            def save():
                self.cursor.execute("""
                    UPDATE personnel_location
                    SET location_id=%s, start_date=%s, role=%s, mandate=%s, end_date=%s
                    WHERE personnel_id=%s
                """, (
                    entries["location_id"].get(),
                    entries["start_date"].get(),
                    entries["role"].get(),
                    entries["mandate"].get(),
                    entries["end_date"].get() or None,
                    pid_entry.get()
                ))
                self.conn.commit()
                messagebox.showinfo("Success", "Personnel updated!")
                win.destroy()
                self.show_table_data("personnel_location")

            tk.Button(win, text="Save", command=save).grid(row=len(labels) + 2, columnspan=2, pady=10)

        tk.Button(win, text="Load", command=load).grid(row=1, columnspan=2, pady=5)

    def delete_personnel(self):
        win = tk.Toplevel(self.root)
        win.title("Delete Personnel")

        tk.Label(win, text="Personnel ID:").grid(row=0, column=0)
        pid_entry = tk.Entry(win)
        pid_entry.grid(row=0, column=1)

        def delete():
            self.cursor.execute("DELETE FROM personnel_location WHERE personnel_id=%s", (pid_entry.get(),))
            self.cursor.execute("DELETE FROM Personnel WHERE personnel_id=%s", (pid_entry.get(),))
            self.conn.commit()
            messagebox.showinfo("Success", "Personnel deleted!")
            win.destroy()
            self.show_table_data("personnel_location")

        tk.Button(win, text="Delete", command=delete).grid(row=1, columnspan=2, pady=5)

    def display_personnel(self):
        if self.welcome_label.winfo_exists():
            self.welcome_label.pack_forget()
        if not self.data_frame.winfo_ismapped():
            self.data_frame.pack(fill="both", expand=True)

        # Clear previous data and reset columns (fix for crash)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree["columns"] = ()
        self.tree["displaycolumns"] = ()

        # Join query to get detailed personnel info
        query = """
            SELECT p.personnel_id, per.first_name, per.last_name, per.ssn, per.email
            FROM Personnel p
            JOIN Person per ON p.person_id = per.person_id
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            # Get column names dynamically from cursor description
            columns = [desc[0] for desc in self.cursor.description]

            # Configure Treeview columns
            self.tree["columns"] = columns
            self.tree["displaycolumns"] = columns
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor="w", minwidth=50)

            # Insert rows
            for row in results:
                self.tree.insert("", "end", values=row)
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            messagebox.showerror("Query Error", f"Failed to query Personnel details: {e}")


    ## family member

    # --- FAMILY MEMBER ---

    # --- Family Member ---
    def add_family_member(self):
        # Create main window with buttons to choose Primary or Secondary
        win = tk.Toplevel(self.root)
        win.title("Add FamilyMember")

        def add_primary():
            # Create a new Toplevel for Primary FamilyMember
            primary_win = tk.Toplevel(self.root)
            primary_win.title("Add Primary FamilyMember")

            tk.Label(primary_win, text="Person ID:").pack(pady=5)
            p_id_entry = tk.Entry(primary_win)
            p_id_entry.pack(pady=5)

            tk.Label(primary_win, text="Club Member ID (Minor):").pack(pady=5)
            cm_id_entry = tk.Entry(primary_win)
            cm_id_entry.pack(pady=5)

            tk.Label(primary_win, text="Relationship:").pack(pady=5)
            rel_entry = tk.Entry(primary_win)
            rel_entry.pack(pady=5)

            def save():
                try:
                    self.cursor.execute("INSERT IGNORE INTO FamilyMember (person_id) VALUES (%s)", (p_id_entry.get(),))
                    self.cursor.execute("""
                        INSERT INTO family_association (fm_id, cm_id, relationship, start_date)
                        VALUES ((SELECT fm_id FROM FamilyMember WHERE person_id=%s), %s, %s, CURDATE())
                    """, (p_id_entry.get(), cm_id_entry.get(), rel_entry.get()))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Primary FamilyMember added!")
                    primary_win.destroy()
                    self.show_table_data("family_association")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(primary_win, text="Save", command=save).pack(pady=10)
            tk.Button(primary_win, text="Cancel", command=primary_win.destroy).pack(pady=5)

        def add_secondary():
            # Create a new Toplevel for Secondary FamilyMember
            secondary_win = tk.Toplevel(self.root)
            secondary_win.title("Add Secondary FamilyMember")

            tk.Label(secondary_win, text="Secondary Family Member ID:").pack(pady=5)
            sec_id_entry = tk.Entry(secondary_win)
            sec_id_entry.pack(pady=5)

            tk.Label(secondary_win, text="Primary Family Member ID:").pack(pady=5)
            fm_id_entry = tk.Entry(secondary_win)
            fm_id_entry.pack(pady=5)

            def save():
                try:
                    self.cursor.execute("""
                        INSERT INTO secondary_fm (secondary_fm_id, fm_id) VALUES (%s, %s)
                    """, (sec_id_entry.get(), fm_id_entry.get()))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Secondary FamilyMember added!")
                    secondary_win.destroy()
                    self.show_table_data("secondary_fm")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(secondary_win, text="Save", command=save).pack(pady=10)
            tk.Button(secondary_win, text="Cancel", command=secondary_win.destroy).pack(pady=5)

        tk.Button(win, text="Add Primary Family Member", command=add_primary).pack(pady=5)
        tk.Button(win, text="Add Secondary Family Member", command=add_secondary).pack(pady=5)
        tk.Button(win, text="Cancel", command=win.destroy).pack(pady=5)

    def edit_family_member(self):
        win = tk.Toplevel(self.root)
        win.title("Edit Primary FamilyMember")

        tk.Label(win, text="Person ID:").grid(row=0, column=0)
        p_id_entry = tk.Entry(win)
        p_id_entry.grid(row=0, column=1)

        tk.Label(win, text="Club Member ID:").grid(row=1, column=0)
        cm_id_entry = tk.Entry(win)
        cm_id_entry.grid(row=1, column=1)

        def load():
            self.cursor.execute("""
                SELECT relationship FROM family_association
                WHERE fm_id = (SELECT fm_id FROM FamilyMember WHERE person_id=%s)
                AND cm_id = %s
            """, (p_id_entry.get(), cm_id_entry.get()))
            result = self.cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "No primary family member found.")
                return
            rel_entry = tk.Entry(win)
            rel_entry.insert(0, result[0])
            rel_entry.grid(row=2, column=1)
            tk.Label(win, text="Relationship:").grid(row=2, column=0)

            def save():
                self.cursor.execute("""
                    UPDATE family_association
                    SET relationship=%s
                    WHERE fm_id = (SELECT fm_id FROM FamilyMember WHERE person_id=%s)
                    AND cm_id = %s
                """, (rel_entry.get(), p_id_entry.get(), cm_id_entry.get()))
                self.conn.commit()
                messagebox.showinfo("Success", "FamilyMember updated!")
                win.destroy()
                self.show_table_data("family_association")

            tk.Button(win, text="Save", command=save).grid(row=3, columnspan=2)

        tk.Button(win, text="Load", command=load).grid(row=4, columnspan=2, pady=5)

    def delete_family_member(self):
        # Create main window with buttons to choose Primary or Secondary
        win = tk.Toplevel(self.root)
        win.title("Delete FamilyMember")

        def delete_primary():
            # Create a new Toplevel for Delete Primary FamilyMember
            primary_win = tk.Toplevel(self.root)
            primary_win.title("Delete Primary FamilyMember")

            tk.Label(primary_win, text="Family Member ID:").pack(pady=5)
            fm_id_entry = tk.Entry(primary_win)
            fm_id_entry.pack(pady=5)

            tk.Label(primary_win, text="Club Member ID:").pack(pady=5)
            cm_id_entry = tk.Entry(primary_win)
            cm_id_entry.pack(pady=5)

            def delete():
                fm_id = fm_id_entry.get().strip()
                cm_id = cm_id_entry.get().strip()
                if not fm_id or not cm_id:
                    messagebox.showerror("Error", "Please enter both Family Member ID and Club Member ID")
                    return

                try:
                    self.cursor.execute("SELECT fm_id, cm_id FROM family_association WHERE fm_id = %s AND cm_id = %s", (fm_id, cm_id))
                    if not self.cursor.fetchone():
                        messagebox.showerror("Error", f"No family association found with Family Member ID {fm_id} and Club Member ID {cm_id}")
                        return

                    self.cursor.execute("DELETE FROM family_association WHERE fm_id = %s AND cm_id = %s", (fm_id, cm_id))
                    self.conn.commit()
                    messagebox.showinfo("Success", f"Family association with Family Member ID {fm_id} and Club Member ID {cm_id} deleted!")
                    primary_win.destroy()
                    self.show_table_data("family_association")
                except mysql.connector.Error as e:
                    self.conn.rollback()
                    messagebox.showerror("Error", f"Failed to delete family association: {e}")

            tk.Button(primary_win, text="Delete", command=delete).pack(pady=10)
            tk.Button(primary_win, text="Cancel", command=primary_win.destroy).pack(pady=5)

        def delete_secondary():
            # Create a new Toplevel for Delete Secondary FamilyMember
            secondary_win = tk.Toplevel(self.root)
            secondary_win.title("Delete Secondary FamilyMember")

            tk.Label(secondary_win, text="Secondary Family Member ID:").pack(pady=5)
            sec_id_entry = tk.Entry(secondary_win)
            sec_id_entry.pack(pady=5)

            tk.Label(secondary_win, text="Primary Family Member ID:").pack(pady=5)
            fm_id_entry = tk.Entry(secondary_win)
            fm_id_entry.pack(pady=5)

            def delete():
                sec_id = sec_id_entry.get().strip()
                fm_id = fm_id_entry.get().strip()
                if not sec_id or not fm_id:
                    messagebox.showerror("Error", "Please enter both Secondary and Primary Family Member IDs")
                    return

                try:
                    self.cursor.execute("SELECT secondary_fm_id, fm_id FROM secondary_fm WHERE secondary_fm_id = %s AND fm_id = %s", (sec_id, fm_id))
                    if not self.cursor.fetchone():
                        messagebox.showerror("Error", f"No Secondary FamilyMember found with Secondary ID {sec_id} and Primary ID {fm_id}")
                        return

                    self.cursor.execute("DELETE FROM secondary_fm WHERE secondary_fm_id = %s AND fm_id = %s", (sec_id, fm_id))
                    self.conn.commit()
                    messagebox.showinfo("Success", f"Secondary FamilyMember with Secondary ID {sec_id} deleted!")
                    secondary_win.destroy()
                    self.show_table_data("secondary_fm")
                except mysql.connector.Error as e:
                    self.conn.rollback()
                    messagebox.showerror("Error", f"Failed to delete Secondary FamilyMember: {e}")

            tk.Button(secondary_win, text="Delete", command=delete).pack(pady=10)
            tk.Button(secondary_win, text="Cancel", command=secondary_win.destroy).pack(pady=5)

        tk.Button(win, text="Delete Primary Family Member", command=delete_primary).pack(pady=5)
        tk.Button(win, text="Delete Secondary Family Member", command=delete_secondary).pack(pady=5)
        tk.Button(win, text="Cancel", command=win.destroy).pack(pady=5)
    ## club member
    # --- Club Member ---
    # --- Club Member ---
    def add_club_member(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add ClubMember")

        tk.Label(add_win, text="Person ID:").grid(row=0, column=0)
        person_id_entry = tk.Entry(add_win)
        person_id_entry.grid(row=0, column=1)

        tk.Label(add_win, text="Height (cm):").grid(row=1, column=0)
        height_entry = tk.Entry(add_win)
        height_entry.grid(row=1, column=1)

        tk.Label(add_win, text="Weight (kg):").grid(row=2, column=0)
        weight_entry = tk.Entry(add_win)
        weight_entry.grid(row=2, column=1)

        tk.Label(add_win, text="Gender:").grid(row=3, column=0)
        gender_var = tk.StringVar()
        ttk.Combobox(add_win, textvariable=gender_var, values=["Male", "Female", "Other"], state="readonly").grid(row=3,
                                                                                                                  column=1)

        def submit():
            try:
                self.cursor.execute("""
                    INSERT INTO ClubMember (person_id, height, weight, gender, membership_status, last_paid_year)
                    VALUES (%s, %s, %s, %s, 'Active', YEAR(CURDATE()))
                """, (person_id_entry.get(), height_entry.get(), weight_entry.get(), gender_var.get()))
                self.conn.commit()
                messagebox.showinfo("Success", "ClubMember added!")
                add_win.destroy()
                self.show_table_data("ClubMember")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(add_win, text="Submit", command=submit).grid(row=4, columnspan=2, pady=10)

    def edit_club_member(self):
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit ClubMember")

        tk.Label(edit_win, text="Person ID:").grid(row=0, column=0)
        person_id_entry = tk.Entry(edit_win)
        person_id_entry.grid(row=0, column=1)

        tk.Label(edit_win, text="Height (cm):").grid(row=1, column=0)
        height_entry = tk.Entry(edit_win)
        height_entry.grid(row=1, column=1)

        tk.Label(edit_win, text="Weight (kg):").grid(row=2, column=0)
        weight_entry = tk.Entry(edit_win)
        weight_entry.grid(row=2, column=1)

        tk.Label(edit_win, text="Gender:").grid(row=3, column=0)
        gender_var = tk.StringVar()
        ttk.Combobox(edit_win, textvariable=gender_var, values=["Male", "Female", "Other"], state="readonly").grid(
            row=3, column=1)

        def load_data():
            self.cursor.execute("SELECT height, weight, gender FROM ClubMember WHERE person_id=%s",
                                (person_id_entry.get(),))
            row = self.cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "No ClubMember found for this Person ID")
                return
            height_entry.delete(0, tk.END)
            height_entry.insert(0, row[0])
            weight_entry.delete(0, tk.END)
            weight_entry.insert(0, row[1])
            gender_var.set(row[2])

        def save():
            try:
                self.cursor.execute("""
                    UPDATE ClubMember
                    SET height=%s, weight=%s, gender=%s
                    WHERE person_id=%s
                """, (height_entry.get(), weight_entry.get(), gender_var.get(), person_id_entry.get()))
                self.conn.commit()
                messagebox.showinfo("Success", "ClubMember updated!")
                edit_win.destroy()
                self.show_table_data("ClubMember")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(edit_win, text="Load", command=load_data).grid(row=4, column=0, pady=10)
        tk.Button(edit_win, text="Save", command=save).grid(row=4, column=1, pady=10)

    def delete_club_member(self):
        del_win = tk.Toplevel(self.root)
        del_win.title("Delete ClubMember")

        tk.Label(del_win, text="Enter Person ID to Delete:").pack()
        pid_entry = tk.Entry(del_win)
        pid_entry.pack()

        def delete():
            person_id = pid_entry.get()
            self.cursor.execute("SELECT cm_id FROM ClubMember WHERE person_id = %s", (person_id,))
            result = self.cursor.fetchone()
            if not result:
                messagebox.showerror("Error", f"No ClubMember found with Person ID {person_id}")
                return
            if not messagebox.askyesno("Confirm", f"Delete ClubMember with Person ID {person_id}?"):
                return
            try:
                self.cursor.execute("DELETE FROM ClubMember WHERE person_id = %s", (person_id,))
                self.conn.commit()
                messagebox.showinfo("Success", f"ClubMember for Person ID {person_id} deleted!")
                del_win.destroy()
                self.show_table_data("ClubMember")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(del_win, text="Delete", command=delete).pack()

    def add_team_formation(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add TeamFormation")

        # Fetch valid team IDs
        self.cursor.execute("SELECT team_id FROM Team")
        teams = [str(row[0]) for row in self.cursor.fetchall()]

        # Fetch valid session IDs
        self.cursor.execute("SELECT session_id FROM Sessions")
        sessions = [str(row[0]) for row in self.cursor.fetchall()]

        tk.Label(add_win, text="Team ID:").grid(row=0, column=0)
        team_var = tk.StringVar()
        ttk.Combobox(add_win, textvariable=team_var, values=teams, state="readonly").grid(row=0, column=1)

        tk.Label(add_win, text="Session ID:").grid(row=1, column=0)
        session_var = tk.StringVar()
        ttk.Combobox(add_win, textvariable=session_var, values=sessions, state="readonly").grid(row=1, column=1)

        tk.Label(add_win, text="Score:").grid(row=2, column=0)
        score_entry = tk.Entry(add_win)
        score_entry.grid(row=2, column=1)

        def submit():
            try:
                self.cursor.execute(
                    "INSERT INTO team_session (team_id, session_id, score) VALUES (%s, %s, %s)",
                    (team_var.get(), session_var.get(), score_entry.get() or None)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "TeamFormation added!")
                add_win.destroy()
                self.show_table_data("team_session")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(add_win, text="Submit", command=submit).grid(row=3, columnspan=2)

    def edit_team_formation(self):
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit TeamFormation")

        # Fetch existing team-session combinations
        self.cursor.execute("SELECT team_id, session_id FROM team_session")
        combinations = [f"{row[0]}-{row[1]}" for row in self.cursor.fetchall()]

        tk.Label(edit_win, text="Select Team-Session:").grid(row=0, column=0)
        combo_var = tk.StringVar()
        combo_dropdown = ttk.Combobox(edit_win, textvariable=combo_var, values=combinations, state="readonly")
        combo_dropdown.grid(row=0, column=1)

        tk.Label(edit_win, text="New Score:").grid(row=1, column=0)
        score_entry = tk.Entry(edit_win)
        score_entry.grid(row=1, column=1)

        def load_score(event=None):
            if combo_var.get():
                team_id, session_id = combo_var.get().split("-")
                self.cursor.execute("SELECT score FROM team_session WHERE team_id=%s AND session_id=%s",
                                    (team_id, session_id))
                row = self.cursor.fetchone()
                if row:
                    score_entry.delete(0, tk.END)
                    score_entry.insert(0, row[0] if row[0] is not None else "")

        combo_dropdown.bind("<<ComboboxSelected>>", load_score)

        def save():
            if not combo_var.get():
                messagebox.showerror("Error", "Please select a record")
                return
            team_id, session_id = combo_var.get().split("-")
            try:
                self.cursor.execute(
                    "UPDATE team_session SET score=%s WHERE team_id=%s AND session_id=%s",
                    (score_entry.get() or None, team_id, session_id)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "TeamFormation updated!")
                edit_win.destroy()
                self.show_table_data("team_session")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(edit_win, text="Save", command=save).grid(row=2, columnspan=2)

    def delete_team_formation(self):
        del_win = tk.Toplevel(self.root)
        del_win.title("Delete TeamFormation")

        # Fetch existing team-session combinations
        self.cursor.execute("SELECT team_id, session_id FROM team_session")
        combinations = [f"{row[0]}-{row[1]}" for row in self.cursor.fetchall()]

        tk.Label(del_win, text="Select Team-Session:").grid(row=0, column=0)
        combo_var = tk.StringVar()
        combo_dropdown = ttk.Combobox(del_win, textvariable=combo_var, values=combinations, state="readonly")
        combo_dropdown.grid(row=0, column=1)

        def delete():
            if not combo_var.get():
                messagebox.showerror("Error", "Please select a record")
                return
            team_id, session_id = combo_var.get().split("-")
            if not messagebox.askyesno("Confirm", f"Delete TeamFormation {team_id}-{session_id}?"):
                return
            try:
                self.cursor.execute("DELETE FROM team_session WHERE team_id=%s AND session_id=%s",
                                    (team_id, session_id))
                self.conn.commit()
                messagebox.showinfo("Success", "TeamFormation deleted!")
                del_win.destroy()
                self.show_table_data("team_session")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(del_win, text="Delete", command=delete).grid(row=1, columnspan=2)

    # Make Payment
    def make_payment(self):
        self.current_table = "Payment"
        # Get column metadata
        self.cursor.execute(f"SHOW COLUMNS FROM {self.current_table}")
        cols = self.cursor.fetchall()
        # Exclude AUTO_INCREMENT
        fields = [col[0] for col in cols if "auto_increment" not in col[5]]
        fields.remove("payment_date")
        fields.append("ClubMemberID")

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
            sql = f"INSERT INTO Payment (payment_method,payment_amount ,payment_date) VALUES ('{vals[0]}','{vals[1]}',CURDATE())"
            sql2 = f"INSERT INTO cm_payment (payment_id,cm_id ,membership_year) VALUES (last_insert_id(),{vals[2]},YEAR(CURDATE())+1)"
            try:
                self.cursor.execute(sql)
                self.conn.commit()
                self.cursor.execute(sql2)
                self.conn.commit()
                messagebox.showinfo("Success", "Record updated.")
                form.destroy()
                self.show_table_data(self.current_table)
                # print(self.conn.cmd_query(get_id))
            except mysql.connector.Error as e:
                messagebox.showerror("Insert Error", str(e))

        ttk.Button(form, text="Insert", command=do_insert).grid(
            row=len(fields), column=0, columnspan=2, pady=10
        )





    # Assign Player
    def assign_player(self):
        self.current_table = "team_player"
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
            sql = f"INSERT INTO {self.current_table} ({','.join(fields)}) VALUES ({','.join(['%s'] * len(fields))})"

            if self.recent_player.__len__() != 0:
                if self.recent_player.get(vals[1]) != None:
                    if (
                            self.recent_player.get(vals[1]) - datetime.today()
                    ).total_seconds() / 3600 < 3:
                        messagebox.showerror(
                            "Insert Error", "You need to wait before adding same player"
                        )
                        form.destroy()
                        self.show_table_data(self.current_table)
                        return
            try:
                self.cursor.execute(sql, vals)
                self.conn.commit()
                messagebox.showinfo("Success", "Record inserted.")
                form.destroy()
                self.show_table_data(self.current_table)
                self.recent_player[vals[1]] = datetime.today()
            except mysql.connector.Error as e:
                form.destroy()
                messagebox.showerror("Insert Error", str(e))

        ttk.Button(form, text="Insert", command=do_insert).grid(
            row=len(fields), column=0, columnspan=2, pady=10
        )

# Global exception handler
def handle_exception(exc_type, exc_value, exc_traceback):
    print(f"Exception occurred: {exc_type}, {exc_value}")




import sys

sys.excepthook = handle_exception

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseGUI(root)
    root.mainloop()
