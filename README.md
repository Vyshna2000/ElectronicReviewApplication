📌 Electronic Review Application

A web-based platform for users to explore, review, and rate electronic products. Admins can manage products, categories, and user activities with a dedicated dashboard.

🚀 Tech Stack
Backend: Django (Python)

Database: SQLite

Frontend: HTML, CSS, Bootstrap

Authentication: Django Auth, Google Sign-In, OTP-based Forgot Password

✅ Features
👥 User Features
Register and securely log in

Sign in using Google OAuth2

OTP-based Forgot Password and Reset

View products and detailed reviews

Like other users’ reviews

Sort and search through products and reviews

Edit and delete own reviews

🔐 Admin Features
Admin dashboard with control over:

Products and their updates

Product categories

Customer reviews

User accounts

Review moderation (edit/delete)

Product management (add/edit/delete)

🛠️ Getting Started
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/electronic-review-app.git
cd electronic-review-app
2. Create and Activate a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run Migrations
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
5. Run the Development Server
bash
Copy
Edit
python manage.py runserver
Visit: http://127.0.0.1:8000/

🔐 Environment Variables
Create a .env file to store sensitive information:

env
Copy
Edit
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret



