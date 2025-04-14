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
- Backend: **Python + Flask + Firebase (Firestore)**  
- Frontend: **Django** with a simple UI  
- Role-based login and restricted access to routes


---

## ✨ Features

### 🏢 **Librarian Features**
- 🔍 Search books by title
- 📥 Borrow and 📤 return books
- 👤 Register new library users

### 🔧 **Admin Features**
- 📘 Add, ✏️ edit, ❌ delete books
- 🔑 Manage user roles

### 🔒 **Security**
- Role-based access (Admin & Librarian)
- Basic password protection (to be enhanced with encryption)

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

### 🔹 Step 1: Run the Django Frontend(lms_django)
cd lms_django

### Apply Migrations for Django
python manage.py makemigrations
python manage.py migrate

### 🔹 🔹 Step 2: Run the Django Server (Frontend - lms_django)
python manage.py runserver

### 🔹 Step 3: Run the Flask Backend (Backend - lms)
cd lms_backend
source ../.venv/bin/activate  # On Windows use `../.venv/Scripts/activate`

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
