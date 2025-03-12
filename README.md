# 📚 Library Management System (LMS)

The **Library Management System (LMS)** is a book inventory system designed for librarians and administrators. It allows efficient management of book records, borrowing status tracking, and inventory updates.

---

## 📖 Table of Contents
- [📖 Overview](#-overview)
- [✨ Features](#-features)
- [💾 Installation](#-installation)
- [🚀 Running the Project](#-running-the-project)
- [🖥 Usage](#-usage)
- [🛣 Roadmap](#-roadmap)
- [🔧 Maintenance](#-maintenance)
- [📜 License](#-license)
- [📬 Contact](#-contact)
- [👥 Contributors](#-contributors)

---

## 📖 Overview

LMS helps library staff streamline book tracking and management. 
It is built in **Python** using **Flask** for the backend and integrates with **Firebase** for real-time database management. The frontend is implemented using **Django** with a simple UI for managing book operations.



---

## ✨ Features

### 🏢 **Librarian Features**
- 🔍 **Search Books** by title, author, or genre.
- 📖 **Check Book Availability** and borrowing history.
- 📥 **Borrow Books** and track due dates.
- 📤 **Return Books** after completion.
- 👤 **Register New Clients** (Library Users).

### 🔧 **Admin Features**
- 📘 **Add New Books** with metadata (Title, Author, Genre).
- ✏️ **Update Book Information** when needed.
- ❌ **Remove Books** that are no longer available.
- 🔑 **User Role Management**: Assign librarians and administrators.

### 🔒 **Security Features**
- 🔑 **Role-Based Access Control**: Only admins can modify book records.
- 🔐 **Password Encryption**: Secure librarian and admin accounts.

---

## 💾 Installation

### 🔹 **Prerequisites**
Ensure you have the following installed:
- **Python 3.7+**
- **pip** (Python Package Manager)
- **Git**
- **Firebase Account** (for Firestore database)
- **Virtual Environment (`venv`)**

### 🔹 **Clone the Repository**

git clone https://github.com/yourusername/LMS.git
cd LMS

### 🔹 Create a Virtual Environment
python -m venv venv
source venv/bin/activate

### 🔹 Clone the Repository
git clone https://github.com/yourusername/LMS.git


 ### 🔹 Create a Virtual Environment
python -m venv venv

### 🔹 Install Dependencies
pip install -r requirements.txt

## 🚀 Running the Project

### 🔹 Step 1: Apply Migrations for Django (Frontend - lms_django)
cd lms_django

### Apply Migrations for Django
python manage.py makemigrations
python manage.py migrate

### 🔹 🔹 Step 2: Run the Django Server (Frontend - lms_django)
python manage.py runserver

### 🔹 Step 3: Run the Flask Backend (Backend - lms)
cd lms  # Go to the backend folder
source ../venv/bin/activate  # Activate virtual environment

#### Run the backend server:
python app.py

📬 Contact
For support, reach out to the contributors.


## 👥 Contributors

| Name           | Email                      |
|---------------|----------------------------|
| Claudia Saleem | clau050994@gmail.com       |
| Yang Tortrong | yang.tortrong@yahoo.com    |
| Amilcar Pena  | amilcarjpp@gmail.com       |
| Jorge Diaz    | jorgediaz7125@gmail.com    |
