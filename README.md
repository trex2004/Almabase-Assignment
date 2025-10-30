# SDE Intern Assignment  
**by Swayam Poddar**

## 📘 Overview

**SDE Intern Assignment** is a Django + Django REST Framework project demonstrating a secure REST API architecture for managing users, marking spam contacts, and searching phone numbers.  
It supports JWT-based authentication, efficient trigram search, pagination, and user interaction tracking.

This project explores core backend concepts such as authentication, pagination, deduplication, and text similarity queries, using **PostgreSQL** with trigram search support.

---

## ⚙️ Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL (used for trigram similarity search)  
- **Authentication:** JWT (SimpleJWT)  
- **Language:** Python 3.10+  

---

## 🧠 Core Features

### 1. **User Authentication**
- `/api/user/signup` – Register new users.  
- `/api/user/login` – Login existing users; auto-creates new users if not found.  
- JWT tokens used for authenticated requests.  

### 2. **Spam Reporting**
- `/api/spam` – Report any phone number as spam, even if not linked to a user.  

### 3. **Search**
- `/api/search?q=<query>&limit=0` – Search by phone number or name using trigram similarity.  
- `/api/search/detail/<uuid:id>/` – Fetch detailed user/contact info.  
- Supports pagination and deduplication by phone number.  

### 4. **Contacts**
- `/api/contact` – Create or register new contacts for a user.  

### 5. **Interactions**
- `/api/interactions/create` – Log new interactions between users.  
- `/api/interactions/recent/<uuid:user_id>` – Retrieve recent interactions (with pagination and optional filtering).  
- `/api/interactions/top/<uuid:user_id>` – Return top most-contacted users.  
- `/api/interactions/spam` – Aggregate spam reports for users or phone numbers.  

### 6. **Dashboard**
- `/dashboard/` – HTML dashboard for viewing user interactions.  
- `/login/` & `/logout/` – Simple user login/logout pages.  

---

## 🔐 Authentication Rules

| Endpoint | Authentication |
|-----------|----------------|
| `/api/user/signup` | ❌ Public |
| `/api/user/login` | ❌ Public |
| All other `/api/*` routes | ✅ JWT Required |

---

## 📦 Setup Instructions

### 1. Clone Repository
```bash
git clone <your-bitbucket-repo-url>
cd <repo-folder>
```
### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Database Configuration
Set your PostgreSQL environment variable:
```bash
# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=hiring_challenge
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_SSLMODE=disable

# Django
SECRET_KEY=dev-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```
Or configure directly inside settings.py.

Enable trigram extension in PostgreSQL:
```bash
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Start the Server
```bash
python manage.py runserver
```
Server runs locally at http://127.0.0.1:8000/

## 🚀 API Endpoints

| Method   | Endpoint                                  | Description                          | Auth |
| -------- | ----------------------------------------- | ------------------------------------ | ---- |
| **POST** | `/api/user/signup`                        | Register new user                    | ❌   |
| **POST** | `/api/user/login`                         | Login or auto-create user            | ❌   |
| **POST** | `/api/spam`                               | Report a phone number as spam        | ✅   |
| **GET**  | `/api/search?q=`                          | Search user/contact by name or phone | ✅   |
| **GET**  | `/api/search/detail/<uuid:id>/`           | Get detailed profile info            | ✅   |
| **POST** | `/api/contact`                            | Create contact                       | ✅   |
| **POST** | `/api/interactions/create`                | Log user interaction                 | ✅   |
| **GET**  | `/api/interactions/recent/<uuid:user_id>` | List recent interactions             | ✅   |
| **GET**  | `/api/interactions/top/<uuid:user_id>`    | Top N most-contacted users           | ✅   |
| **GET**  | `/api/interactions/spam`                  | Aggregate spam reports               | ✅   |
| **GET**  | `/dashboard/`                             | User dashboard (HTML)                | ✅   |
| **GET**  | `/login/`                                 | Login page                           | ❌   |
| **GET**  | `/logout/`                                | Logout page                          | ✅   |

## 📄 Some Example API Requests & Responses

### /api/user/signup (POST)
#### Request
```bash
{
  "phone_number": "9830509185",
  "password": "pass123"
}
```
#### Response
```bash
{
  "id": "0b6b6667-78de-48b3-9741-4c42d2f1af4c",
  "phone_number": "9830509185",
  "token": "<jwt-token>"
}
```
### /api/search?q=9830509185 (GET)
#### Response
```bash
{
  "count": 1,
  "results": [
    {
      "id": "0b6b6667-78de-48b3-9741-4c42d2f1af4c",
      "name": "Swayam Poddar",
      "is_registered": true,
      "phone_number": "9830509185",
      "spammed_by_count": 0
    }
  ]
}
```
## Key Features Recap

### JWT Authentication
### Auto User Creation on Login
### Secure REST API Design
### Trigram Search for Name Matching
### Pagination Support
### Spam Reporting System
### Interaction Logging & Analytics
### HTML Dashboard for User