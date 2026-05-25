# ⚡ Electra — E-Commerce Website for Electronic Gadgets

> IGNOU MCA Online Project (MCSP-232)  
> **Student:** Joseph James | **Enrolment No:** 2452427589  
> **Guide:** As per project submission

---

## 📌 Project Overview

**Electra** is a full-featured e-commerce web application built with **Django (Python)** for selling electronic gadgets. It supports product browsing, cart management, Razorpay payment integration, order tracking, reviews, and an admin dashboard.

---

## 🚀 Features

- 🛍️ Product listing with search & category filter
- 🔐 User registration, login, and session management
- 🛒 Shopping cart with quantity management
- 💳 Razorpay payment gateway integration
- 📦 Order placement and status tracking
- ⭐ Product reviews and ratings
- 👤 Customer profile / shipping address management
- 🛠️ Admin panel (manage products, orders, users)

---

## 🏗️ Tech Stack

| Technology | Version |
|---|---|
| Python | 3.11.9 |
| Django | 5.2.12 |
| Pillow | 12.1.1 |
| Razorpay SDK | 2.0.1 |
| Bootstrap | 5.3 (CDN) |
| SQLite | 3.x (built-in) |

---

## 📁 Project Structure

```
electra/
├── electra/              ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app/                  ← Main application
│   ├── models.py         ← Database models
│   ├── views.py          ← View functions
│   ├── forms.py          ← Form definitions
│   ├── urls.py           ← URL patterns
│   ├── admin.py          ← Admin configuration
│   ├── tests.py          ← 37 unit & system tests
│   ├── migrations/
│   └── templates/app/    ← HTML templates
├── static/               ← Static files (CSS, JS)
├── media/                ← Uploaded product images
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/electra.git
cd electra
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Razorpay keys
Open `electra/settings.py` and update:
```python
RAZORPAY_KEY_ID = 'your_razorpay_key_id'
RAZORPAY_KEY_SECRET = 'your_razorpay_key_secret'
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser (admin)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**

---

## 🔗 Access URLs

| URL | Description |
|---|---|
| `/` | Homepage |
| `/products/` | Product listing |
| `/login/` | Login |
| `/register/` | Registration |
| `/cart/` | Shopping cart |
| `/checkout/` | Checkout & payment |
| `/orders/` | My orders |
| `/profile/` | User profile |
| `/contact/` | Contact form |
| `/admin/` | Admin panel |

---

## 🧪 Running Tests

```bash
python manage.py test app --verbosity=2
```

**37 tests — 13 unit tests + 24 system tests — all pass.**

---

## 📦 Data Models

- **Product** — Title, price, discounted price, brand, category, image
- **Customer** — Shipping address linked to user
- **Cart** — Cart items per user
- **Payment** — Razorpay transaction records
- **OrderPlaced** — Confirmed orders with status tracking
- **ProductReview** — Star ratings and text reviews
- **ContactUs** — Customer inquiries

---

## 🔒 Security

- CSRF protection on all forms
- Password hashing (PBKDF2-SHA256, 600,000 iterations)
- `@login_required` on cart, checkout, orders, and profile
- Django ORM parameterized queries (SQL injection prevention)
- Payment data handled entirely by Razorpay over TLS/SSL

---

## 📜 License

This project is submitted as part of IGNOU MCA academic coursework (MCSP-232). For educational purposes only.
