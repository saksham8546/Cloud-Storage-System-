print("Cloud Storage System")
import boto3
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os

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

# Define User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Home route (index page)
@app.route('/')
def index():
    return render_template('index.html')

# Route to list all S3 buckets
@app.route('/buckets', methods=['GET'])
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
def download_file():
    filename = request.form['filename']
    local_path = os.path.join('downloads', filename)
    try:
        s3.download_file(S3_BUCKET, filename, local_path)
        return send_from_directory('downloads', filename)
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('index'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simplified user authentication
        if username == 'admin' and password == 'password':
            user = User(1)
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Invalid credentials')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
