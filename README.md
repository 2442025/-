# -# モバイルバッテリー貸し出しシステム

本リポジトリは、Practice #10 における
Web3層構造を用いたモバイルバッテリー貸し出しシステムの
設計資料を管理する。

## メンバー
2442025 菊地亜由美

2442033　今野早耶佳

2442037　佐藤心優

2442085　森本真理子
Simply Bookstore Application

This is a simple bookstore application developed for personal practice.
The project is a refactored and extended version of bookstore.py, focusing on basic Web application architecture, database design, and CRUD operations.

Overview

Application type: Bookstore management system

Architecture: Web-based 3 Layer architecture

Presentation Layer (GUI)

Application Layer (Python logic)

Data Layer (Relational Database)

Database type: RDB (Relational Database)

Main purpose: Practice of CRUD operations, database design, and system architecture

Functions
User Functions

Login with user account
LoginGUI() → StoreMainGUI()

Create a new user account
LoginGUI()

Edit user account information
StoreMainGUI() → UserInfoGUI()

Buy books
StoreMainGUI() → BuyBooksGUI()

Logout
→ LoginGUI()

Admin Functions

Login with admin account
LoginGUI() → AdminGUI()

Create user accounts
AdminGUI() → UserManageGUI(False)

Edit user accounts
AdminGUI() → UserManageGUI(True)

Register new books
AdminGUI() → BookManageGUI(False)

Edit book information
AdminGUI() → BookManageGUI(True)

View order history
AdminGUI() → ViewOrderGUI()

Logout
→ LoginGUI()

File Structure
main.py

Controls the entire application flow

Account creation

Login

GUI transitions

Classes

LoginGUI

StoreMainGUI

AdminGUI

Database tables used

accounts

customer.py

Handles all user-related functions

Functions

Login

Account creation

Edit user information

Buy books

Logout

Classes

BuyBooksGUI

UserInfoGUI

Database tables used

accounts

books

cards

checks

orders

admin.py

Handles all admin-related functions

Functions

Admin login

User management

Book management

Order viewing

Logout

Classes

UserManageGUI

BookManageGUI

ViewOrderGUI

Database tables used

accounts

books

cards

checks

orders

variables.py

Common variables and shared functions
(Acts like a header file in C++)

Database Design

This application uses a Relational Database (RDB).
ER diagram was created based on the following schema.

accounts
Column	Type	Description
user_id	text	Primary Key
password	text	NOT NULL
fname	text	First name
lname	text	Last name
email	text	Email address
saved_payment	int	Saved payment method

saved_payment values

0: None / Unsaved

1: Credit / Debit Card

2: Check

3: Cash (on delivery)

books
Column	Type	Description
book_id	int	Primary Key
title	text	Book title
author	text	Author
publisher	text	Publisher
price	float	Price
available	int	Stock quantity
sold	int	Number of sales
orders
Column	Type	Description
order_id	text	Primary Key
user_id	text	NOT NULL
booklist	text	Purchased book list
totalprice	float	Total price
shipaddress	text	Shipping address
payment	text	Payment method
cards
Column	Type	Description
user_id	text	Primary Key
name	text	Card holder name
cardnumber	text	Card number
exp_month	text	Expiration month
exp_year	text	Expiration year
bill_street	text	Billing street
bill_city	text	Billing city
bill_state	text	Billing state
bill_country	text	Billing country
bill_zip	text	ZIP code
bill_phone	text	Phone number
checks
Column	Type	Description
user_id	text	Primary Key
name	text	Bank name
acctype	text	Account type (Checking / Saving)
routing	text	Routing number
bankacc	text	Account number
Assignment Requirements Coverage

DB construction: Completed (RDB used)

ER diagram: Created based on above schema

CRUD operations: Fully implemented via Web/Python application

3 Layer Web architecture: Applied

System structure diagram: Can be derived from current architecture

RPO / RTO / Backup / Performance: Can be defined based on this structure
