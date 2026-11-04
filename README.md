# 🩺 LifeVault – Digital Emergency Medical Information System

LifeVault is a web-based emergency medical information management system developed using Django and MySQL. It aims to make essential patient information accessible during medical emergencies through a unique LifeVault ID and QR code.

The system provides separate access for patients and doctors, with doctor verification to help protect sensitive medical information.

## 🚀 Features

- **Patient Registration & Login:** Secure patient account creation and authentication.
- **Doctor Registration & Login:** Separate authentication for doctors.
- **LifeVault ID Generation:** Unique identification ID for every patient and doctor.
- **QR Code Generation:** QR code linked to the patient's emergency access page.
- **Patient Dashboard:** Manage basic patient information.
- **Patient Profile:** Store blood group, blood pressure, age, address and emergency contact details.
- **Doctor Verification:** Doctor accounts require administrator verification before accessing the doctor dashboard.
- **Emergency Access:** QR-based entry point for emergency medical access.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL |
| QR Code | Python QR Code Library |
| Version Control | Git, GitHub |

## 📂 Project Structure

```text
LifeVault/
│
├── accounts/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ananth-Naik/LifeVault.git
cd LifeVault
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

- Create a MySQL database for LifeVault.
- Configure the database connection in Django settings using your own environment variables.
- Keep database credentials and Django secret keys out of GitHub.

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open your browser:

```text
http://127.0.0.1:8000/
```

## 🔐 Security

- Django password hashing for user authentication.
- Role-based access for patients and doctors.
- Doctor verification status before dashboard access.
- Sensitive configuration and uploaded patient data should remain outside the public repository.

## 📌 Project Status

**Currently under development.**

Upcoming improvements:
- Admin dashboard for doctor verification.
- Medical information management.
- Authorized doctor access to emergency medical records.
- Emergency access logs.
- Patient access history.
- Improved security and deployment.

## 👨‍💻 Developer

**Anantha Naik**

- GitHub: [Ananth-Naik](https://github.com/Ananth-Naik)

---

*LifeVault – Making essential medical information accessible when every second matters.*
