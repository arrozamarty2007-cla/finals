# THREADLINE — Online Clothing Store

This project follows the folder and coding style of the two supplied class ZIPs:
- React frontend follows the Session 8 Vite structure (`App.jsx`, `pages/`, `components/`, `routes/`, `main.jsx`, `index.css`).
- Django backend follows the Session 11 structure (`core/`, `accounts/`, `models.py`, `serializers.py`, `views.py`, `urls.py`).
- The database models follow the supplied ERD: `base_users`, `carts`, `cart_products`, `products`, `transactions`, and `product_transactions`.

## Project folders

```text
threadline_clothing_shop/
├── docs/
│   └── database_erd.png      # Supplied database diagram
├── backend/
│   ├── core/                 # Django settings and root URL configuration
│   ├── accounts/             # ERD models, serializers, API views and routes
│   ├── manage.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/              # API connection and headers
    │   ├── components/       # Login popup and product card
    │   ├── context/          # Login state and authentication
    │   ├── pages/            # Shop, Cart and Orders pages
    │   ├── routes/           # React Router configuration
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── package.json
    └── vite.config.js
```

## 1. Run Django backend

Open a terminal in `backend`:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations accounts
python manage.py migrate
python manage.py seed_products
python manage.py createsuperuser
python manage.py runserver
```

Backend API: `http://127.0.0.1:8000/api/`
Admin: `http://127.0.0.1:8000/admin/`

## 2. Run React frontend

Open another terminal in `frontend`:

```bash
npm install
npm run dev
```

Open `http://localhost:5173/`.

## Main API routes

| Method | Route | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Register a customer |
| POST | `/api/auth/login/` | Log in and receive a token |
| POST | `/api/auth/logout/` | Log out |
| GET | `/api/auth/me/` | Current account |
| GET | `/api/products/` | Product list, search and category filter |
| GET | `/api/products/<id>/` | Product details |
| GET, POST | `/api/cart/` | View cart / add product |
| PATCH, DELETE | `/api/cart/items/<id>/` | Update or remove a cart line |
| POST | `/api/checkout/` | Create an order and reduce stock |
| GET | `/api/transactions/` | Current customer's order history |

## ERD relationship mapping

- `BaseUser` owns many `Cart` records and many `Transaction` records.
- `Cart` contains `CartProduct` records.
- `CartProduct` points to one `Product` and stores its quantity.
- `Transaction` contains `ProductTransaction` records.
- `ProductTransaction` points to one `Product`, stores quantity and the purchase-time unit price.

Every model uses an explicit `UniqueID` primary key, matching the ERD. The React API serializers expose that key as `id` so it is convenient to use in the frontend. The database table names are explicitly set to the six ERD table names. The product category shown in the shop is derived from the SKU prefix (TOP, BTM or OUT), so no extra category column is added to the ERD. The order status and displayed unit price are also API display values; they are not extra database columns.

This is a local development project. It uses SQLite and a development secret key. Configure production secrets, HTTPS, allowed hosts, CORS, image storage and a real payment provider before deployment. The checkout endpoint records an order for demonstration; it does not process real payments.
