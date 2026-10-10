# ⚡ ShopZone - Full-Stack E-Commerce Web Application

A full-stack, responsive E-commerce web application built for college project demonstration and evaluation. Built using **Python (Django)** on the backend, **HTML5 / CSS3 / JavaScript (Vanilla)** on the frontend, and **SQLite** as the database.

---

## 📌 Project Overview

**ShopZone** is an online shopping platform designed to demonstrate modern web engineering concepts, session management, RESTful interactions, object-relational mapping (ORM), and transaction processing.

### Key Features
1. **Product Catalog & Categorization**
   - Live category filtering (Electronics, Audio, Wearables, Books, etc.)
   - Real-time search bar (by title, description, or category)
   - Dynamic sorting (Price Low to High, High to Low, Name, Newest)
   - Stock badges (In Stock vs. Sold Out) and percentage discount calculations.

2. **Interactive Product Details**
   - High-resolution gallery and specifications
   - Dynamic quantity stepper (+ / - controls)
   - Customer ratings and verified review indicators
   - Related products recommendation section.

3. **Session-Based Shopping Cart**
   - Seamless cart session engine (works for both guests and authenticated users)
   - Instant AJAX "Add to Cart" with floating toast feedback
   - Real-time quantity adjustment and item removal
   - Automatic subtotal, shipping fee, and grand total recalculations (Free delivery on orders > $50).

4. **Order Processing & Checkout**
   - Complete multi-field shipping details form
   - Multiple payment options (Cash on Delivery, Simulated Card, Simulated UPI)
   - Stock verification on checkout to prevent overselling
   - Automatic inventory deduction upon order placement
   - Unique alphanumeric order confirmation code generation (`ORD-XXXXXXXX`)
   - Printable invoice / receipt view.

5. **User Authentication & Customer Dashboard**
   - User Registration & Login with secure password hashing (`PBKDF2`)
   - "My Orders" customer panel with live fulfillment status tracking (`Pending`, `Processing`, `Shipped`, `Delivered`).

6. **Django Admin Management Dashboard**
   - Full CRUD capability for Products, Categories, and Orders
   - Inline order items display
   - Editable product pricing and inventory stock straight from list view.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Modern Flexbox & CSS Grid), JavaScript (Vanilla ES6+) |
| **Backend** | Python 3.14+, Django 6.1 (MVT Architecture) |
| **Database** | SQLite3 (Zero-configuration relational database) |
| **Session & Auth** | Django Sessions & Built-in PBKDF2 Authentication |

---

## 📂 Project Directory Structure

```text
ecommerce_store/
├── .venv/                         # Virtual environment
├── core/                          # Django project configuration
│   ├── settings.py                # Main settings & installed apps
│   ├── urls.py                    # Root URL router
│   ├── wsgi.py                    # WSGI entry point
│   └── asgi.py                    # ASGI entry point
├── store/                         # E-commerce application
│   ├── admin.py                   # Django admin dashboard configuration
│   ├── cart.py                    # Session-based shopping cart manager
│   ├── context_processors.py      # Global cart & category context
│   ├── forms.py                   # Checkout and registration forms
│   ├── models.py                  # Category, Product, Order, OrderItem models
│   ├── views.py                   # Catalog, cart, checkout, and auth views
│   ├── urls.py                    # Store route mappings
│   ├── tests.py                   # Automated unit test suite
│   └── management/
│       └── commands/
│           └── populate_data.py   # Database seeder script
├── templates/                     # HTML templates
│   └── store/
│       ├── base.html              # Base navigation, alerts & footer layout
│       ├── product_list.html      # Catalog grid, filters & search
│       ├── product_detail.html    # Single product view & specs
│       ├── cart.html              # Shopping cart table & summary
│       ├── checkout.html          # Shipping form & payment methods
│       ├── order_confirmation.html# Order receipt & printable view
│       ├── login.html             # User login page
│       ├── register.html          # User registration page
│       └── my_orders.html         # Customer order history
├── static/                        # Static assets
│   ├── css/
│   │   └── style.css              # Custom responsive stylesheet
│   └── js/
│       └── main.js                # AJAX cart, steppers, and toast notifications
├── db.sqlite3                     # SQLite database file
├── manage.py                      # Django CLI management script
├── requirements.txt               # Python package dependencies
└── README.md                      # Project documentation
```

---

## 🚀 How to Run the Project

### 1. Open Terminal in Project Folder
```bash
cd "C:\Users\Buddharaj\.gemini\antigravity\scratch\ecommerce_store"
```

### 2. Activate the Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

### 3. (Optional) Run Tests
Verify all components are working:
```bash
python manage.py test store
```

### 4. Start the Development Server
```bash
python manage.py runserver
```

### 5. Access the Web Application
- **Storefront:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin Portal:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Default Credentials

### Admin Superuser (For Demo / Viva):
- **Username:** `admin`
- **Password:** `admin123`
*(Use this to log into the `/admin` portal to create products, change order status, or edit prices)*

---

## 🎓 Viva / Presentation Q&A Cheatsheet

1. **Q: Why did you choose Django for the backend?**
   - *A:* Django follows the Model-View-Template (MVT) architectural pattern and provides out-of-the-box ORM, an administrative interface for back-office management, CSRF protection, and a session framework without requiring third-party libraries.

2. **Q: How does the shopping cart persist items before checkout?**
   - *A:* We utilize Django's session framework (`request.session['cart']`). It serializes product IDs and quantities into the session cookie. This allows users to add items without having to log in first (guest shopping), preserving cart state across page visits.

3. **Q: How do you prevent overselling or race conditions during order placement?**
   - *A:* In `views.py -> checkout()`, the server validates current database inventory against the cart quantities before committing the `Order` record, and decrements `product.stock` atomically.

4. **Q: How does the frontend communicate with the backend for cart actions?**
   - *A:* We use Vanilla JavaScript `fetch()` with `X-Requested-With: XMLHttpRequest` headers. If JavaScript is disabled or fails, it gracefully falls back to native HTTP POST form submission.
