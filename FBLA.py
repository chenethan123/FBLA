import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

class CreateAccountScreen:
    def __init__(self, parent_frame, app_instance):
        # Initialize the CreateAccountScreen with a parent frame and the main application instance
        self.parent_frame = parent_frame
        self.app_instance = app_instance


        # Create widgets for username, password, and create account button
        self.label_username = ttk.Label(self.parent_frame, text="Username:")
        self.label_password = ttk.Label(self.parent_frame, text="Password:")
        self.entry_username = ttk.Entry(self.parent_frame)
        self.entry_password = ttk.Entry(self.parent_frame, show="*")
        self.button_create_account = ttk.Button(self.parent_frame, text="Create Account", command=self.create_account)


        # Grid layout for widgets
        self.label_username.grid(row=0, column=0, pady=10)
        self.entry_username.grid(row=0, column=1, pady=10)
        self.label_password.grid(row=1, column=0, pady=10)
        self.entry_password.grid(row=1, column=1, pady=10)
        self.button_create_account.grid(row=2, column=1, pady=10)


    def create_account(self):
        # Get username and password from entry widgets
        username = self.entry_username.get()
        password = self.entry_password.get()


        # Check if the username or password is empty
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
        elif self.username_exists(username):
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            # Insert user data into the database
            self.app_instance.insert_user_data(username, password)
            messagebox.showinfo("Success", "Account created successfully!")
            self.app_instance.show_index()


    def username_exists(self, username):
        # Check if a username already exists in the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        conn.close()
        return existing_user is not None

class PartnerManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Partner Management System")
        self.create_users_table()
        self.create_partners_table()
        self.current_frame = None
        self.show_index()

    def create_users_table(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def create_partners_table(self):
        conn = sqlite3.connect('partners.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS partners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                resources TEXT,
                contact_name TEXT,
                contact_email TEXT,
                contact_phone TEXT
            )
        ''')
        conn.commit()
        conn.close()
    def show_index(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack()
        label = ttk.Label(self.current_frame, text="Partner Management System", font=('Arial', 18))
        label.pack(pady=20)
        login_button = ttk.Button(self.current_frame, text="Login", command=self.show_login)
        login_button.pack(pady=10)
        create_account_button = ttk.Button(self.current_frame, text="Create Account", command=self.show_create_account)
        create_account_button.pack(pady=10)
        quit_button = ttk.Button(self.current_frame, text="Quit", command=self.root.quit)
        quit_button.pack(pady=10)


    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack()
        label_username = ttk.Label(self.current_frame, text="Username:")
        label_password = ttk.Label(self.current_frame, text="Password:")
        self.entry_username = ttk.Entry(self.current_frame)
        self.entry_password = ttk.Entry(self.current_frame, show="*")
        button_login = ttk.Button(self.current_frame, text="Login", command=self.login_verify)
        label_username.grid(row=0, column=0, pady=10)
        self.entry_username.grid(row=0, column=1, pady=10)
        label_password.grid(row=1, column=0, pady=10)
        self.entry_password.grid(row=1, column=1, pady=10)
        button_login.grid(row=2, column=1, pady=10)

    def show_create_account(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack()
        CreateAccountScreen(self.current_frame, self)

    def login_verify(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if self.verify_user_credentials(username, password):
            self.show_main_application_screen(username)
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def verify_user_credentials(self, username, password):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def show_main_application_screen(self, username):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack()
        label_main = ttk.Label(self.current_frame, text="CTE Partner Management", font=('Arial', 18))
        label_main.pack(pady=20)
        label_username = ttk.Label(self.current_frame, text=f"Username: {username}")
        label_username.pack(pady=10)
        modifyButton = ttk.Button(self.current_frame, text="Modify Partners", command=self.choose_modify_or_add)
        modifyButton.pack(pady=10)
        viewButton = ttk.Button(self.current_frame, text="View Partners", command=self.viewPartner)
        viewButton.pack(pady=10)
        logout_button = ttk.Button(self.current_frame, text="Logout", command=self.show_index)
        logout_button.pack(pady=10)

    def choose_modify_or_add(self):
        # Create a new window
        choice_window = tk.Toplevel(self.root)
        choice_window.title("Modify or Add Partner")

        # Configure the new window layout
        choice_window.geometry('500x100')  # Adjust the size as needed

        # Add description label
        ttk.Label(choice_window, text="Choose an action:").pack(pady=10)

        # Add Partner Button
        add_button = ttk.Button(choice_window, text="Add Partner", command=lambda: [choice_window.destroy(), self.addPartner()])
        add_button.pack(side=tk.LEFT, padx=10, pady=20)

        # Modify Partner Button
        modify_button = ttk.Button(choice_window, text="Edit Partner", command=lambda: [choice_window.destroy(), self.modifyPartner()])
        modify_button.pack(side=tk.RIGHT, padx=10, pady=20)

        remove_button = ttk.Button(choice_window, text="Remove Partner", command=lambda: [choice_window.destroy(), self.removePartner()])
        remove_button.pack(side=tk.BOTTOM, padx=10, pady=20)
    def addPartner(self):
        add_partner_window = tk.Toplevel(self.root)
        add_partner_window.title("Add Partner")

        # Labels and entry widgets for partner details
        ttk.Label(add_partner_window, text="Name:").grid(row=0, column=0, pady=5)
        entry_name = ttk.Entry(add_partner_window)
        entry_name.grid(row=0, column=1, pady=5)

        ttk.Label(add_partner_window, text="Type (e.g., Supplier, Distributor):").grid(row=1, column=0, pady=5)
        entry_type = ttk.Entry(add_partner_window)
        entry_type.grid(row=1, column=1, pady=5)

        ttk.Label(add_partner_window, text="Resources (e.g., Financial, Material):").grid(row=2, column=0, pady=5)
        entry_resources = ttk.Entry(add_partner_window)
        entry_resources.grid(row=2, column=1, pady=5)

        ttk.Label(add_partner_window, text="Contact Name:").grid(row=3, column=0, pady=5)
        entry_contact_name = ttk.Entry(add_partner_window)
        entry_contact_name.grid(row=3, column=1, pady=5)

        ttk.Label(add_partner_window, text="Contact Email:").grid(row=4, column=0, pady=5)
        entry_contact_email = ttk.Entry(add_partner_window)
        entry_contact_email.grid(row=4, column=1, pady=5)

        ttk.Label(add_partner_window, text="Contact Phone:").grid(row=5, column=0, pady=5)
        entry_contact_phone = ttk.Entry(add_partner_window)
        entry_contact_phone.grid(row=5, column=1, pady=5)

        ttk.Button(add_partner_window, text="Back", command=lambda: [add_partner_window.destroy()]).grid(row = 7, column = 1, pady = 5)

        def insert_partner_data(name, type, resources, contact_name, contact_email, contact_phone):
            # Connect to the database
            conn = sqlite3.connect('partners.db')  # Adjust the database name as necessary
            cursor = conn.cursor()

            # SQL query to insert the new partner data
            query = """INSERT INTO partners (name, type, resources, contact_name, contact_email, contact_phone) 
                    VALUES (?, ?, ?, ?, ?, ?)"""

            # Execute the query and commit the changes
            try:
                cursor.execute(query, (name, type, resources, contact_name, contact_email, contact_phone))
                conn.commit()
                messagebox.showinfo("Success", "Partner added successfully.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                conn.close()

        def submit_partner():
            # Validate required fields
            if not entry_name.get() or not entry_type.get() or not entry_resources.get() or not entry_contact_name.get():
                messagebox.showerror("Error", "All fields except email and phone are required.")
                return
            if entry_contact_email.get() and not self.is_valid_email(entry_contact_email.get()):
                messagebox.showerror("Error", "Invalid email format.")
                return
            if entry_contact_phone.get() and not self.is_valid_phone(entry_contact_phone.get()):
                messagebox.showerror("Error", "Invalid phone number format.")
                return

            # Insert partner data into the database
            insert_partner_data(entry_name.get(), entry_type.get(), entry_resources.get(),
                                    entry_contact_name.get(), entry_contact_email.get(), entry_contact_phone.get())
            add_partner_window.destroy()
            messagebox.showinfo("Success", "Partner added successfully.")

        ttk.Button(add_partner_window, text="Submit", command=submit_partner).grid(row=6, column=1, pady=10)


    def get_partners_list(self):
        conn = sqlite3.connect('partners.db')  # Adjust the database name as necessary
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM partners")  # Assuming 'name' is the column you want to fetch
            partners = cursor.fetchall()
            # Extract partner names from the fetched tuples
            partners_list = [partner[0] for partner in partners]
        except sqlite3.Error as e:
            print("Database error:", e)
            partners_list = []
        finally:
            conn.close()
        return partners_list
    def modifyPartner(self):
        edit_partner_window = tk.Toplevel(self.root)
        edit_partner_window.title("Edit Partner")

        # Fetch partners list for the dropdown
        partners_list = self.get_partners_list()
        selected_partner_var = tk.StringVar(edit_partner_window)
        selected_partner_var.set("Select a partner")

        ttk.Label(edit_partner_window, text="Select Partner:").grid(row=0, column=0, pady=10)
        dropdown_partners = ttk.Combobox(edit_partner_window, textvariable=selected_partner_var, values=partners_list)
        dropdown_partners.grid(row=0, column=1, pady=10, padx=10)

        # Entry widgets for partner details
        ttk.Label(edit_partner_window, text="Name:").grid(row=1, column=0, pady=5)
        entry_name = ttk.Entry(edit_partner_window)
        entry_name.grid(row=1, column=1, pady=5)

        ttk.Label(edit_partner_window, text="Type:").grid(row=2, column=0, pady=5)
        entry_type = ttk.Entry(edit_partner_window)
        entry_type.grid(row=2, column=1, pady=5)

        ttk.Label(edit_partner_window, text="Resources:").grid(row=3, column=0, pady=5)
        entry_resources = ttk.Entry(edit_partner_window)
        entry_resources.grid(row=3, column=1, pady=5)

        ttk.Label(edit_partner_window, text="Contact Name:").grid(row=4, column=0, pady=5)
        entry_contact_name = ttk.Entry(edit_partner_window)
        entry_contact_name.grid(row=4, column=1, pady=5)

        ttk.Label(edit_partner_window, text="Contact Email:").grid(row=5, column=0, pady=5)
        entry_contact_email = ttk.Entry(edit_partner_window)
        entry_contact_email.grid(row=5, column=1, pady=5)

        ttk.Label(edit_partner_window, text="Contact Phone:").grid(row=6, column=0, pady=5)
        entry_contact_phone = ttk.Entry(edit_partner_window)
        entry_contact_phone.grid(row=6, column=1, pady=5)
        ttk.Button(edit_partner_window, text="Back", command=lambda: [edit_partner_window.destroy()]).grid(row = 8, column = 1, pady = 5)

        # Function to populate entry widgets with the selected partner's details
        def populate_partner_details():
            partner_name = selected_partner_var.get()
            partner_details = get_partner_details(partner_name)
            if partner_details:
                entry_name.delete(0, tk.END)
                entry_name.insert(0, partner_details[1])  # Assuming index 1 is name

                entry_type.delete(0, tk.END)
                entry_type.insert(0, partner_details[2])  # Assuming index 2 is type

                entry_resources.delete(0, tk.END)
                entry_resources.insert(0, partner_details[3])  # Assuming index 3 is resources

                entry_contact_name.delete(0, tk.END)
                entry_contact_name.insert(0, partner_details[4])  # Assuming index 4 is contact name

                entry_contact_email.delete(0, tk.END)
                entry_contact_email.insert(0, partner_details[5])  # Assuming index 5 is contact email

                entry_contact_phone.delete(0, tk.END)
                entry_contact_phone.insert(0, partner_details[6])  # Assuming index 6 is contact phone

        ttk.Button(edit_partner_window, text="Load Details", command=populate_partner_details).grid(row=0, column=2, padx=10, pady=10)

        def get_partner_details(partner_name):
            conn = sqlite3.connect('partners.db')  # Adjust the database name as necessary
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM partners WHERE name = ?", (partner_name,))
                partner_details = cursor.fetchone()
                return partner_details
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                return None
            finally:
                conn.close()
        # Function to update the partner details in the database
        def update_partner_details():
            # Validate required fields...
            if not all([entry_name.get(), entry_type.get(), entry_resources.get(), entry_contact_name.get()]):
                messagebox.showerror("Error", "Required fields cannot be empty.")
                return
            # Assuming 'self.update_partner_data' is your method to update partner details in the database
            self.update_partner_data(entry_name.get(), entry_type.get(), entry_resources.get(), entry_contact_name.get(), entry_contact_email.get(), entry_contact_phone.get())
            messagebox.showinfo("Success", "Partner details updated successfully.")
            edit_partner_window.destroy()

        ttk.Button(edit_partner_window, text="Update Partner", command=update_partner_details).grid(row=7, column=1, pady=10)

    def removePartner(self):
        remove_partner_window = tk.Toplevel(self.root)
        remove_partner_window.title("Remove Partner")

        # Fetch partners list for the dropdown
        partners_list = self.get_partners_list()  # Assuming this method returns a list of partner names
        selected_partner_var = tk.StringVar(remove_partner_window)
        selected_partner_var.set("Select a partner")

        ttk.Label(remove_partner_window, text="Select Partner:").pack(pady=5)
        dropdown_partners = ttk.Combobox(remove_partner_window, textvariable=selected_partner_var, values=partners_list)
        dropdown_partners.pack(pady=5)

        # Function to confirm and remove selected partner
        def confirm_and_remove():
            partner_name = selected_partner_var.get()
            if messagebox.askyesno("Confirm", "Are you sure you want to remove this partner?"):
                self.delete_partner_data(partner_name)
                remove_partner_window.destroy()
                messagebox.showinfo("Success", "Partner removed successfully.")

        # "Remove Partner" button
        ttk.Button(remove_partner_window, text="Remove Partner", command=confirm_and_remove).pack(pady=(10, 20))

        # "Back" button
        ttk.Button(remove_partner_window, text="Back", command=lambda: [remove_partner_window.destroy()]).pack(pady=10)
        def confirm_and_remove():
            partner_name = selected_partner_var.get()
            if messagebox.askyesno("Confirm", "Are you sure you want to remove this partner?"):
                self.delete_partner_data(partner_name)
                remove_partner_window.destroy()
                messagebox.showinfo("Success", "Partner removed successfully.")
    def delete_partner_data(self, partner_name):
        conn = sqlite3.connect('partners.db')  # Adjust as necessary
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM partners WHERE name = ?", (partner_name,))
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()



    def update_partner_data(self, name, type, resources, contact_name, contact_email, contact_phone):
        # Connect to the database
        conn = sqlite3.connect('partners.db')  # Adjust the database name as necessary
        cursor = conn.cursor()

        # SQL query to update the partner data
        query = """UPDATE partners 
                SET name = ?, type = ?, resources = ?, contact_name = ?, contact_email = ?, contact_phone = ? 
                """  

        # Execute the query and commit the changes
        try:
            cursor.execute(query, (name, type, resources, contact_name, contact_email, contact_phone))
            conn.commit()
            messagebox.showinfo("Success", "Partner details updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

        # Submit button for updating partner details
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
        return re.match(pattern, email) is not None

    def is_valid_phone(self, phone):
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None

    def viewPartner(self):
        view_partner_window = tk.Toplevel(self.root)
        view_partner_window.title("View Partners")

        # Search bar
        search_var = tk.StringVar()
        search_entry = ttk.Entry(view_partner_window, textvariable=search_var)
        search_entry.pack(pady=(10, 0))

        # Dropdown for specifying search criteria, including "No Filter" option
        search_criteria = tk.StringVar()
        criteria_options = ["No Filter", "Name", "Type", "Resources", "Contact Name", "Contact Email", "Contact Phone"]
        criteria_dropdown = ttk.Combobox(view_partner_window, textvariable=search_criteria, values=criteria_options)
        criteria_dropdown.set("No Filter")  # Default to no specific filter
        criteria_dropdown.pack(pady=(5, 10))

        # Treeview setup
        tree = ttk.Treeview(view_partner_window, columns=("Name", "Type", "Resources", "Contact Name", "Contact Email", "Contact Phone"), show="headings")
        for col in ("Name", "Type", "Resources", "Contact Name", "Contact Email", "Contact Phone"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(expand=True, fill='both', side='top')

    # Function to update displayed data based on search or show all if "No Filter" is selected
        def filter_displayed_data():
            query = search_var.get().lower()
            criteria = search_criteria.get()
            for item in tree.get_children():
                tree.delete(item)  # Clear existing data
            partners = self.get_partners_list_for_view()

            # If "No Filter" is selected, check the query against all fields
            if criteria == "No Filter" and query:
                filtered_partners = [partner for partner in partners if query in ' '.join(map(str.lower, partner)).lower()]
            elif criteria != "No Filter" and query:
                # Apply filtering based on the selected criteria and search query
                criteria_index = criteria_options.index(criteria) - 1  # Adjust for "No Filter" being the first option
                filtered_partners = [partner for partner in partners if query in str(partner[criteria_index]).lower()]
            else:
                # If no query is entered, or "No Filter" is selected with no query, show all partners
                filtered_partners = partners

            # Repopulate tree with filtered or all data
            for partner in filtered_partners:
                tree.insert('', 'end', values=partner)
        search_button = ttk.Button(view_partner_window, text="Search", command=filter_displayed_data)
        search_button.pack(pady=(0, 10))

        ttk.Button(view_partner_window, text="Back", command=lambda: [view_partner_window.destroy()]).pack(pady=(0,13))

        # Initially populate the treeview with all partners
        filter_displayed_data()  # Call this initially to load all partners by default


    def get_partners_list_for_view(self):
        # Example implementation (adjust based on your actual database schema)
        conn = sqlite3.connect('partners.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Type, Resources, Contact_Name, Contact_Email, Contact_Phone FROM partners")
        partners = cursor.fetchall()
        conn.close()
        return partners

    def get_partners_list_for_view(self):
        conn = sqlite3.connect('partners.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, type, resources, contact_name, contact_email, contact_phone FROM partners")
        partners = cursor.fetchall()
        conn.close()
        return partners

    def insert_user_data(self, username, password):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()



if __name__ == '__main__':
    # Create the root window and start the Tkinter main loop
    root = tk.Tk()
    app = PartnerManagementApp(root)
    root.mainloop()



