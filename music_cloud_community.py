import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

class MusicApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Music App")
        self.root.geometry("800x600")
        
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Dar@2005',  
            'database': 'music_db'
        }
        
        # Start with login page
        self.show_login_page()

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_styled_frame(self):
        """Create a styled main frame"""
        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        return frame

    
    def show_login_page(self):
        """Display the login page"""
        self.clear_window()
        frame = self.create_styled_frame()

        # Title
        title_label = ttk.Label(frame, text="Login", font=('Helvetica', 24))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Email
        ttk.Label(frame, text="Email:").grid(row=1, column=0, pady=5, sticky="e")
        email_var = tk.StringVar()
        email_entry = ttk.Entry(frame, textvariable=email_var, width=30)
        email_entry.grid(row=1, column=1, pady=5)

    # Password
        ttk.Label(frame, text="Password:").grid(row=2, column=0, pady=5, sticky="e")
        password_var = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=password_var, show="*", width=30)
        password_entry.grid(row=2, column=1, pady=5)

    # Login button
        login_btn = ttk.Button(frame, text="Login", 
                           command=lambda: self.login(email_var.get(), password_var.get()))
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)

    # Skip Login button
        skip_btn = ttk.Button(frame, text="Skip Login", 
                           command=lambda: self.show_dashboard({}))  # Directly show dashboard
        skip_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

    # Register link
        register_link = ttk.Button(frame, text="Don't have an account? Register", 
                               command=self.show_register_page)
        register_link.grid(row=5, column=0, columnspan=2)

    # Ensure layout is flexible
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(4, weight=1)  # Allow row 4 to grow


    def show_register_page(self):
        """Display the registration page"""
        self.clear_window()
        frame = self.create_styled_frame()
        
        # Title
        title_label = ttk.Label(frame, text="Register", font=('Helvetica', 24))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Username
        ttk.Label(frame, text="Username:").grid(row=1, column=0, pady=5, sticky="e")
        username_var = tk.StringVar()
        username_entry = ttk.Entry(frame, textvariable=username_var, width=30)
        username_entry.grid(row=1, column=1, pady=5)
        
        # Email
        ttk.Label(frame, text="Email:").grid(row=2, column=0, pady=5, sticky="e")
        email_var = tk.StringVar()
        email_entry = ttk.Entry(frame, textvariable=email_var, width=30)
        email_entry.grid(row=2, column=1, pady=5)
        
        # Password
        ttk.Label(frame, text="Password:").grid(row=3, column=0, pady=5, sticky="e")
        password_var = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=password_var, show="*", width=30)
        password_entry.grid(row=3, column=1, pady=5)
        
        # Register button
        register_btn = ttk.Button(frame, text="Register", 
                                  command=lambda: self.register(username_var.get(), 
                                                                email_var.get(), 
                                                                password_var.get()))
        register_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Login link
        login_link = ttk.Button(frame, text="Already have an account? Login", 
                                command=self.show_login_page)
        login_link.grid(row=5, column=0, columnspan=2)

    
    def show_dashboard(self, user_data):
        """Display the dashboard"""
        self.clear_window()
        frame = self.create_styled_frame()
    
    # Check if username exists in user_data
        username = user_data.get('username', 'Guest')  # Default to 'Guest' if username is missing

    # Welcome message
        welcome_label = ttk.Label(frame, text=f"Welcome, {username}!", font=('Helvetica', 24))
        welcome_label.pack(pady=20)
    
        options = [
        ("Add Artist", self.show_add_artist_page),
        ("Add Song", self.show_add_song_page),
        ("Create Playlist", self.show_create_playlist_page)
        ]
        for option, command in options:
            ttk.Button(frame, text=option, command=command).pack(pady=10)
    
    # Logout button
        logout_btn = ttk.Button(frame, text="Logout", command=self.show_login_page)
        logout_btn.pack(pady=10)

        
        
    def show_add_artist_page(self):
        """Display the Add Artist form"""
        self.clear_window()
        frame = self.create_styled_frame()

        ttk.Label(frame, text="Add Artist", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        artist_name_var = tk.StringVar()
        ttk.Label(frame, text="Artist Name:").grid(row=1, column=0, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=artist_name_var, width=30).grid(row=1, column=1, pady=5)

        country_var = tk.StringVar()
        ttk.Label(frame, text="Country:").grid(row=2, column=0, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=country_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Button(
            frame,
            text="Add Artist",
            command=lambda: self.add_artist(artist_name_var.get(), country_var.get()),
        ).grid(row=3, column=0, columnspan=2, pady=20)

    def add_artist(self, artist_name, country):
        """Add artist to database"""
        if not artist_name or not country:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Artist (artist_name, country) VALUES (%s, %s)", (artist_name, country))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Artist added successfully!")
            self.show_dashboard({})
        except pymysql.Error as err:
            messagebox.showerror("Database Error", f"Failed to add artist: {err}")
            
    def show_add_song_page(self):
        """Display the Add Song form"""
        self.clear_window()
        frame = self.create_styled_frame()

    # Page Title
        ttk.Label(frame, text="Add Song", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

    # Song Title Input
        song_title_var = tk.StringVar()
        ttk.Label(frame, text="Song Title:").grid(row=1, column=0, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=song_title_var, width=30).grid(row=1, column=1, pady=5)

    # Artist Name Input
        artist_name_var = tk.StringVar()
        ttk.Label(frame, text="Artist Name:").grid(row=2, column=0, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=artist_name_var, width=30).grid(row=2, column=1, pady=5)

    # Add Song Button
        ttk.Button(
        frame,
        text="Add Song",
        command=lambda: self.add_song(song_title_var.get(), artist_name_var.get()),
        ).grid(row=3, column=0, columnspan=2, pady=20)

    def add_song(self, song_title, artist_name):
        """Add song to the database"""
        if not song_title or not artist_name:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            # Establish a database connection
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor()

        # Check if artist exists
            cursor.execute("SELECT artist_id FROM Artist WHERE artist_name = %s", (artist_name,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", f"Artist '{artist_name}' not found in the database.")
                return

            artist_id = result[0]

            # Insert song
            cursor.execute("INSERT INTO Song (title, artist_id) VALUES (%s, %s)", (song_title, artist_id))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", f"Song '{song_title}' added successfully!")
            self.show_dashboard({}) 

        except pymysql.Error as err:
            messagebox.showerror("Database Error", f"Failed to add song: {err}")

    def show_create_playlist_page(self):
        self.clear_window()
        frame = self.create_styled_frame()

        ttk.Label(frame, text="Create Playlist", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        playlist_name_var = tk.StringVar()
        ttk.Label(frame, text="Playlist Name:").grid(row=1, column=0, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=playlist_name_var, width=30).grid(row=1, column=1, pady=5)

        songs = self.fetch_songs()

        song_vars = []
        for index, song in enumerate(songs):
            song_var = tk.BooleanVar()
            song_vars.append(song_var)
            ttk.Checkbutton(frame, text=song['song_name'], variable=song_var).grid(row=2 + index, column=0, columnspan=2, pady=5, sticky="w")

        users = self.fetch_users()
        user_name_var = tk.StringVar()
        ttk.Label(frame, text="Select User:").grid(row=2 + len(songs), column=0, pady=5, sticky="e")
        user_dropdown = ttk.Combobox(frame, textvariable=user_name_var, values=[user['username'] for user in users], state="readonly", width=30)
        user_dropdown.grid(row=2 + len(songs), column=1, pady=5)

        ttk.Button(
        frame,
        text="Create Playlist",
        command=lambda: self.create_playlist(playlist_name_var.get(), song_vars, user_name_var.get()),
        ).grid(row=3 + len(songs), column=0, columnspan=2, pady=20)

    def fetch_songs(self):
        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT song_id, title FROM Song")
            songs = cursor.fetchall()
            cursor.close()
            conn.close()
            return [{'song_id': song[0], 'song_name': song[1]} for song in songs]
        except pymysql.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch songs: {err}")
            return []

    def fetch_users(self):
        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username FROM User")
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            return [{'user_id': user[0], 'username': user[1]} for user in users]
        except pymysql.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch users: {err}")
            return []

    def create_playlist(self, playlist_name, song_vars, user_name):
        if not playlist_name or not user_name:
            messagebox.showerror("Error", "Please fill in all fields")
            return

    # Fetch user_id based on the username
        user_id = self.get_user_id_by_name(user_name)
        if not user_id:
            messagebox.showerror("Error", "User not found")
            return

        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Playlist (playlist_name, user_id) VALUES (%s, %s)", (playlist_name, user_id))
            playlist_id = cursor.lastrowid  # Get the generated playlist_id
            conn.commit()

            for song_var in song_vars:
                if song_var.get():  
                    song_id = song_var.get()  # Assuming the song_var holds the song_id
                    cursor.execute("INSERT INTO PlaylistSongs (playlist_id, song_id) VALUES (%s, %s)", (playlist_id, song_id))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Playlist created successfully!")
            self.show_dashboard({})

        except pymysql.Error as err:
            messagebox.showerror("Database Error", f"Failed to create playlist: {err}")


    def get_user_id_by_name(self, user_name):
        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM User WHERE username = %s", (user_name,))
            user_id = cursor.fetchone()
            cursor.close()
            conn.close()
            return user_id[0] if user_id else None
        except pymysql.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch user ID: {err}")
            return None
     
    
    
    
    def login(self, email, password):
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            if user and user['password'] == password:
                messagebox.showinfo("Success", "Login successful!")
                self.show_dashboard(user)
            else:
                messagebox.showerror("Error", "Invalid email or password")
                
            cursor.close()
            conn.close()
        except pymysql.Error as err:
            messagebox.showerror("Database Error", f"Login failed: {err}")

    def register(self, username, email, password):
        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute('INSERT INTO user (username, email, password) VALUES (%s, %s, %s)', 
                           (username, email, password))
            conn.commit()
            
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Registration successful!")
            self.show_login_page()
        except pymysql.IntegrityError:
            messagebox.showerror("Error", "Email already exists")
        except pymysql.Error as err:
            messagebox.showerror("Database Error", f"Registration failed: {err}")

    
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MusicApp()
    app.run()







