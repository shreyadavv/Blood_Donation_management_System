# 🩸 Blood Donation Management System

A simple **Flask + SQLite** based web application to manage blood donors and requests.  
This project allows users to register as donors, search for available donors by blood group, and request blood in case of emergencies.  

---

## 🚀 Features
- Donor registration with details: name, age, gender, blood group, contact, location.
- Search donors by blood group.
- Submit blood requests.
- Admin dashboard to view all donors and requests.
- Lightweight and easy to deploy (Flask + SQLite).

---

## 🛠 Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML, Bootstrap, Jinja2 templates
- **Version Control**: Git + GitHub

---

## 📂 Project Structure
Blood_Donation_management_System/
│── app.py # Main Flask app
│── database.db # SQLite database
│── static/
│ └── style.css # Custom styles (optional)
│── templates/
│ ├── base.html # Layout template
│ ├── index.html # Home page
│ ├── register.html # Donor registration
│ ├── search.html # Search donors
│ ├── request.html # Request blood
│ └── admin.html # Admin dashboard
│── README.md # Project documentation
