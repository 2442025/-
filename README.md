## メンバー
2442025 菊地亜由美

2442033　今野早耶佳

2442037　佐藤心優

2442085　森本真理子
# Battery Rental Web Application

This is a simple battery rental web application developed for practice purposes.
The application is built using Python, SQLAlchemy, and PostgreSQL, and deployed using GitHub and Render.

---

## Overview

This application allows users to rent batteries from stations, manage their balance, and view rental history.
Administrators can manage users, stations, batteries, and monitor rental activity.

---

## Functions

### User

- Login with user account  
  `Login()` → `Home()`

- View account information and balance  
  `Home()` → `UserInfo()`

- Rent a battery  
  `Home()` → `RentBattery()`

- Return a battery  
  `RentBattery()` → `ReturnBattery()`

- Charge balance  
  `Home()` → `ChargeBalance()`

- Logout  
  → `Login()`

---

### Admin

- Login with admin account  
  `Login()` → `AdminDashboard()`

- Manage user accounts (view / edit)  
  `AdminDashboard()` → `UserManage()`

- Register and edit stations  
  `AdminDashboard()` → `StationManage()`

- Register and edit batteries  
  `AdminDashboard()` → `BatteryManage()`

- View rental history  
  `AdminDashboard()` → `RentalHistory()`

- Logout  
  → `Login()`

---

## File Structure

### main.py
Controls the overall application flow.
- Login
- Authentication
- Page routing

### models.py
Defines database models using SQLAlchemy ORM.

### db.py
Manages database connection and session handling.

### variables.py
Stores common variables and configuration values.

---

## Classes

### User-related
- User
- Rental
- ChargeHistory

### Station / Battery-related
- Station
- Battery

---

## Database

### Database Type
- RDB (Relational Database)
- PostgreSQL (Production on Render)
- SQLite (Local development)

ORM: SQLAlchemy

---

## Database Tables

### users
| Column | Type | Description |
|------|----|-----------|
| id | INTEGER (PK) | User ID |
| email | VARCHAR | Login email |
| password_hash | VARCHAR | Hashed password |
| balance_cents | INTEGER | User balance |
| created_at | TIMESTAMP | Created time |

---

### stations
| Column | Type | Description |
|------|----|-----------|
| id | INTEGER (PK) | Station ID |
| name | VARCHAR | Station name |
| location | VARCHAR | Address |
| lat | FLOAT | Latitude |
| lng | FLOAT | Longitude |

---

### batteries
| Column | Type | Description |
|------|----|-----------|
| id | INTEGER (PK) | Battery ID |
| serial | VARCHAR | Serial number |
| station_id | INTEGER (FK) | Station reference |
| available | BOOLEAN | Availability |
| battery_level | INTEGER | Battery level |
| extra_info | TEXT | Extra info |

---

### rentals
| Column | Type | Description |
|------|----|-----------|
| id | INTEGER (PK) | Rental ID |
| user_id | INTEGER (FK) | User reference |
| battery_id | INTEGER (FK) | Battery reference |
| start_at | TIMESTAMP | Start time |
| end_at | TIMESTAMP | End time |
| status | VARCHAR | ongoing / returned |
| price_cents | INTEGER | Rental price |

---

### charge_histories
| Column | Type | Description |
|------|----|-----------|
| id | INTEGER (PK) | History ID |
| user_id | INTEGER (FK) | User reference |
| amount_cents | INTEGER | Charged amount |
| created_at | TIMESTAMP | Charged time |

---

## ER Diagram

ER diagram is based on the SQLAlchemy models and reflects the actual database schema.

---

## Notes

- Monetary values are stored as integers (cents) to avoid floating-point errors.
- Database schema is normalized to maintain data consistency.
- Designed for extensibility and future feature expansion.

---

## Environment

- Python
- SQLAlchemy
- PostgreSQL
- Render
- GitHub
