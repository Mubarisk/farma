# Medical Shop Billing API

## Project Setup

### Prerequisites
- Python 3.10+
- Django & Django REST Framework
- PostgreSQL or SQLite (for local development)

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mubarisk/farma.git
   cd farma
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser for admin access:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

### Additional Setup
- **Create a `logs` directory in the project root:**
  ```bash
  mkdir logs
  ```
- **Ensure `.env` file is configured for database & JWT settings**

## API Endpoints

### Authentication
- `POST /api/auth/register/` → Admin registers new users
- `POST /api/auth/login/` → Login with JWT authentication
- `POST /api/auth/logout/` → Logout and invalidate token

### Medicine Management (Inventory Manager)
- `POST /api/medicines/` → Add new medicine
- `GET /api/medicines/` → List all medicines
- `GET /api/medicines/{id}/` → Get medicine details
- `PUT /api/medicines/{id}/` → Update medicine details
- `DELETE /api/medicines/{id}/` → Delete medicine

### Billing (Staff Only)
- `POST /api/billing/` → Create a bill

### Dashboard (Admin Only)
- `GET /api/dashboard/stock/` → Get stock availability
- `GET /api/dashboard/reports/` → Generate sales report (date range, staff-wise billing)


