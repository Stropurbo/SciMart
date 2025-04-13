readme_content = """
# 🛒 SciMart – E-commerce API with Django REST Framework

SciMart is a fully functional e-commerce backend built with **Django** and **Django REST Framework (DRF)**. It includes a wide range of APIs for managing products, categories, orders, and reviews, with secure **JWT-based authentication** using **Djoser**. The project also features interactive API documentation using **drf-yasg (Swagger)**.

---

## 🚀 Features

- 🔐 JWT Authentication with Djoser  
- 📦 Product Management (CRUD for admin, browse/filter/search for users)  
- 🗂️ Category Management with product count  
- 🛍️ Order Management with user-specific filtering  
- 📝 Product Reviews with permission control  
- 📷 Product Image Uploads  
- 🔍 Search, Filter & Ordering support  
- 🧾 Swagger/OpenAPI interactive documentation  
- ✅ Role-Based Access Control (Admin vs Regular User)

---

## 🛠 Technologies Used

| Technology                  | Purpose                                           |
|-----------------------------|---------------------------------------------------|
| **Python**                  | Core programming language                         |
| **Django**                  | Web framework for building backend logic          |
| **Django REST Framework**   | Creating RESTful APIs                             |
| **Djoser**                  | User authentication and JWT token management      |
| **Simple JWT**              | JWT-based authentication for secure access        |
| **drf-yasg**                | Auto-generated Swagger/OpenAPI documentation      |
| **django-filter**           | Filtering capabilities in API views               |
| **SQLite / PostgreSQL**     | Database management (default SQLite for dev)      |
| **Swagger UI**              | Interactive API testing and documentation tool    |
| **Virtualenv**              | Isolated Python environment for dependency control |

---

### Auth Endpoints:

- `POST /auth/users/` – Register new user  
- `POST /auth/jwt/create/` – Get JWT access & refresh tokens  
- `POST /auth/jwt/refresh/` – Refresh access token  
- `GET /auth/users/me/` – Get authenticated user profile 

---

## 📦 Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/products/` | List, search, filter, order products |
| `/api/products/{id}/` | Retrieve, update, delete product (admin only) |
| `/api/categories/` | View categories with product counts |
| `/api/products/{product_id}/reviews/` | Add/view product reviews |
| `/api/products/{product_id}/images/` | Upload product images (admin only) |
| `/api/orders/` | Create and manage orders (authenticated users only) |
| `/auth/` | All Djoser JWT auth routes |

---

## 🛠 Installation

1. **Clone the repo**

```bash
git clone https://github.com/your-username/SciMart.git
```

2. **Create virtual environment**
python -m venv venv
# On Windows
venv\\Scripts\\activate
# On macOS/Linux
source venv/bin/activate

3. **Install dependencies**
```
pip install -r requirements.txt

```
**Create superuser (for admin access)**
python manage.py createsuperuser

**🔐 Environment Variables**

# Django settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_HOST = your email hosts

# Database (SQLite default or use PostgreSQL for production)
DATABASE_NAME=Your Database Name
DATABASE_USER=username
DATABASE_PASSWORD=db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# JWT Settings
DJANGO_SECRET_KEY=your-secret-key
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=5
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=1

# Email settings (optional if using email verification)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-email-password
