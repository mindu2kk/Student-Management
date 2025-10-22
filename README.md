# Student Management - Flask + MySQL

Minimal API to manage students, classes, departments, lecturers, courses, sections, registrations, and grades.

## Prerequisites
- Python 3.11+
- MySQL 8+
- PowerShell (Windows) or a shell

## Setup
1. Create database:
   ```sql
   CREATE DATABASE student_mgmt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Configure environment (adjust credentials):
   - Create a `.env` file in project root:
     ```env
     FLASK_DEBUG=1
     DATABASE_URL=mysql+pymysql://root:password@localhost:3306/student_mgmt
     ```
3. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize DB with migrations:
   ```bash
   set FLASK_APP=run.py  # on PowerShell: $env:FLASK_APP="run.py"
   flask db init
   flask db migrate -m "init schema"
   flask db upgrade
   ```
5. Run server:
   ```bash
   python run.py
   ```

## API Overview
- Health: `GET /health`
- Departments: `POST/GET /api/khoas`
- Classes: `POST/GET /api/lops`
- Students: `POST/GET /api/sinhviens`
- Lecturers: `POST/GET /api/giangviens`
- Courses: `POST/GET /api/monhocs`
- Course sections: `POST/GET /api/lophocphans`
- Registration: `POST /api/dangky`, `GET /api/dangky/by-student/<MaSinhVien>`
- Grades: `POST /api/bangdiem`, `GET /api/bangdiem/by-registration/<MaDangKy>`

## Web UI
- Open `http://localhost:5000/`
- Manage:
  - Khoa: list/create/edit/delete
  - Lop: list/create/edit/delete
  - SinhVien: list/create/edit/delete

## Notes
- Dates accept ISO format `YYYY-MM-DD`.
- Unique identifiers follow provided schema; no soft delete.
- Add authentication/validation as needed for production.

