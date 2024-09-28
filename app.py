# # print("Cloud Storage System")
# # import boto3
# # from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# # from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# # import os

# # # Correct Flask app initialization
# # app = Flask(__name__)

# # # Set secret key for session management
# # app.secret_key = 'QnoYBXsyoOPAxI0f+n8qn5ZI4x0/t8jxApGgw0JS'

# # # Configure AWS S3
# # S3_BUCKET = "cloud-storage-buk1"
# # S3_REGION = "us-east-1"
# # s3 = boto3.client('s3', region_name=S3_REGION)

# # # Initialize Flask-Login
# # login_manager = LoginManager()
# # login_manager.init_app(app)

# # # Define User class
# # class User(UserMixin):
# #     def __init__(self, id):
# #         self.id = id

# # # User loader function for Flask-Login
# # @login_manager.user_loader
# # def load_user(user_id):
# #     return User(user_id)

# # # Home route (index page)
# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # # Route to list all S3 buckets
# # @app.route('/buckets', methods=['GET'])
# # def list_buckets():
# #     try:
# #         # List all buckets in S3
# #         response = s3.list_buckets()
# #         buckets = [bucket['Name'] for bucket in response['Buckets']]
# #         return {"buckets": buckets}, 200
# #     except Exception as e:
# #         return {"error": str(e)}, 500

# # # Upload file route
# # @app.route('/upload', methods=['POST'])
# # def upload_file():
# #     if 'file' not in request.files:
# #         flash('No file part')
# #         return redirect(url_for('index'))
    
# #     file = request.files['file']
    
# #     if file.filename == '':
# #         flash('No selected file')
# #         return redirect(url_for('index'))

# #     try:
# #         s3.upload_fileobj(file, S3_BUCKET, file.filename)
# #         flash('File uploaded successfully!')
# #     except Exception as e:
# #         flash(f'Error uploading file: {str(e)}')
    
# #     return redirect(url_for('index'))

# # # Download file route
# # @app.route('/download', methods=['POST'])
# # def download_file():
# #     filename = request.form['filename']
# #     local_path = os.path.join('downloads', filename)
# #     try:
# #         s3.download_file(S3_BUCKET, filename, local_path)
# #         return send_from_directory('downloads', filename)
# #     except Exception as e:
# #         flash(f'Error downloading file: {str(e)}')
# #         return redirect(url_for('index'))

# # # Login route
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
        
# #         # Simplified user authentication
# #         if username == 'admin' and password == 'password':
# #             user = User(1)
# #             login_user(user)
# #             return redirect(url_for('index'))
        
# #         flash('Invalid credentials')
    
# #     return render_template('login.html')

# # # Logout route
# # @app.route('/logout')
# # @login_required
# # def logout():
# #     logout_user()
# #     flash('Logged out successfully.')
# #     return redirect(url_for('index'))

# # # Run the application
# # if __name__ == "__main__":
# #     app.run(debug=True)



# print("Cloud Storage System")
# import boto3
# from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# import sqlite3

# # Correct Flask app initialization
# app = Flask(__name__)

# # Set secret key for session management
# app.secret_key = 'QnoYBXsyoOPAxI0f+n8qn5ZI4x0/t8jxApGgw0JS'

# # Configure AWS S3
# S3_BUCKET = "cloud-storage-buk1"
# S3_REGION = "us-east-1"
# s3 = boto3.client('s3', region_name=S3_REGION)

# # Initialize Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'signup'  # Set signup as the first page for unauthenticated users

# # Create a SQLite database and table for storing users
# DATABASE = 'users.db'

# def init_db():
#     conn = sqlite3.connect(DATABASE)
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             email TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # Initialize the database
# init_db()

# # Define User class
# class User(UserMixin):
#     def __init__(self, id):
#         self.id = id

# # User loader function for Flask-Login
# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect(DATABASE)
#     c = conn.cursor()
#     c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
#     user = c.fetchone()
#     conn.close()
#     if user:
#         return User(user[0])
#     return None

# # Home route (index page) - requires login
# @app.route('/')
# @login_required
# def index():
#     return render_template('index.html')

# # Signup route
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         hashed_password = generate_password_hash(password)  # Hash the password

#         try:
#             # Store user data in the database
#             conn = sqlite3.connect(DATABASE)
#             c = conn.cursor()
#             c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
#             conn.commit()
#             conn.close()
#             flash('Signup successful! Please log in.')
#             return redirect(url_for('templates/login'))
#         except sqlite3.IntegrityError:
#             flash('Email already registered.')
#         except Exception as e:
#             flash(f'Error during signup: {str(e)}')
    
#     return render_template('signup.html')

# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         # Check user credentials in the database
#         conn = sqlite3.connect(DATABASE)
#         c = conn.cursor()
#         c.execute('SELECT * FROM users WHERE email = ?', (email,))
#         user = c.fetchone()
#         conn.close()

#         if user and check_password_hash(user[2], password):
#             login_user(User(user[0]))
#             return redirect(url_for('index'))
        
#         flash('Invalid credentials')
    
#     return render_template('login.html')

# # Route to list all S3 buckets
# @app.route('/buckets', methods=['GET'])
# @login_required
# def list_buckets():
#     try:
#         # List all buckets in S3
#         response = s3.list_buckets()
#         buckets = [bucket['Name'] for bucket in response['Buckets']]
#         return {"buckets": buckets}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500

# # Upload file route
# @app.route('/upload', methods=['POST'])
# @login_required
# def upload_file():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(url_for('index'))
    
#     file = request.files['file']
    
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(url_for('index'))

#     try:
#         s3.upload_fileobj(file, S3_BUCKET, file.filename)
#         flash('File uploaded successfully!')
#     except Exception as e:
#         flash(f'Error uploading file: {str(e)}')
    
#     return redirect(url_for('index'))

# # Download file route
# @app.route('/download', methods=['POST'])
# @login_required
# def download_file():
#     filename = request.form['filename']
#     local_path = os.path.join('downloads', filename)
#     if not os.path.exists('downloads'):
#         os.makedirs('downloads')
#     try:
#         s3.download_file(S3_BUCKET, filename, local_path)
#         return send_from_directory('downloads', filename)
#     except Exception as e:
#         flash(f'Error downloading file: {str(e)}')
#         return redirect(url_for('index'))

# # Logout route
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Logged out successfully.')
#     return redirect(url_for('login'))

# # Run the application
# if __name__ == "__main__":
#     app.run(debug=True)



print("Cloud Storage System")
import boto3
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

# Correct Flask app initialization
app = Flask(__name__)

# Set secret key for session management
app.secret_key = 'QnoYBXsyoOPAxI0f+n8qn5ZI4x0/t8jxApGgw0JS'

# Configure AWS S3
S3_BUCKET = "cloud-storage-buk1"
S3_REGION = "us-east-1"
s3 = boto3.client('s3', region_name=S3_REGION)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signup'  # Set signup as the first page for unauthenticated users

# Create a SQLite database and table for storing users
DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Define User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user[0])
    return None

# Main route redirects to signup if not logged in
@app.route('/')
def main_page():
    # Redirect unauthenticated users to signup page
    if not current_user.is_authenticated:
        return redirect(url_for('signup'))
    return redirect(url_for('signup'))

# Home route (index page) - requires login
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)  # Hash the password

        try:
            # Store user data in the database
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
            conn.commit()
            conn.close()
            flash('Signup successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered.')
        except Exception as e:
            flash(f'Error during signup: {str(e)}')
    
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check user credentials in the database
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            login_user(User(user[0]))
            return redirect(url_for('index'))
        
        flash('Invalid credentials')
    
    return render_template('login.html')

# Route to list all S3 buckets
@app.route('/buckets', methods=['GET'])
@login_required
def list_buckets():
    try:
        # List all buckets in S3
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return {"buckets": buckets}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# Upload file route
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    try:
        s3.upload_fileobj(file, S3_BUCKET, file.filename)
        flash('File uploaded successfully!')
    except Exception as e:
        flash(f'Error uploading file: {str(e)}')
    
    return redirect(url_for('index'))

# Download file route
@app.route('/download', methods=['POST'])
@login_required
def download_file():
    filename = request.form['filename']
    local_path = os.path.join('downloads', filename)
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    try:
        s3.download_file(S3_BUCKET, filename, local_path)
        return send_from_directory('downloads', filename)
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('index'))

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
