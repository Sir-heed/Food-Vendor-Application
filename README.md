# Food-Vendor-Application
VGG Internship project (Food Vendor Application)

This a python web project implemented with the Django Rest Framework.
Projects details include creating end points for users (Vendor or Customer) to create account, set password, login (using the django
 default authentication), CRUD menu and order and other functionalities.
 
# Setting up the project
After downloading or cloning the project
Make sure you have python installed

Install pipenv with
pip install pipenv

create a virtual environment for the project
pipenv shell

change directory into the foodVendorApplication folder where you have pipfile and pipfile.lock
cd FoodVendorApplication

install the project dependencies
pipenv install

edit the env.py to suit your database details, though i used progress, other databases are allowed

To run the previous migrations change directory into the inner foodVendorApplication folder where you have the manage.py 
cd FoodVendorApplication

run the migrations for the account
python manage.py migrate accounts

run the migration for the app
python manage.py migrate app

If the above commands are successful, then you should be able to run the project successfully
python manage.py runserver

# End points
# Accounts End points
Signup a customer with
POST http://127.0.0.1:8000/customers/

Signup a vendor with
POST http://127.0.0.1:8000/vendors/

Get the list of customers with
GET http://127.0.0.1:8000/customers/

Get the list of vendor with 
GET http://127.0.0.1:8000/vendors/

Set password for both Vendors with
POST http://127.0.0.1:8000/password/

Logout both vendor and customer
http://127.0.0.1:8000/logout


# App End points (Authenticated)
After Logging in, a csrftoken is added to the cookies response
append this token to the request header with key "x-csrftoken" to perform action that require authentication

Create a Menu
POST http://127.0.0.1:8000/app/menu/

Get a list of all Menu
GET http://127.0.0.1:8000/app/menu/

Update a menu with an id
PATCH http://127.0.0.1:8000/app/menu/menuId/

Delete a menu with an id
DELETE http://127.0.0.1:8000/app/menu/menuId/

Create an order
POST http://127.0.0.1:8000/app/order/

Get all orders
GET http://127.0.0.1:8000/app/order/

Delete an order
DELETE http://127.0.0.1:8000/app/order/orderId/

Update an order
PATCH http://127.0.0.1:8000/app/order/orderId/

Cancel an order
GET http://127.0.0.1:8000/app/order/orderId/cancel/

Update an order status
GET http://127.0.0.1:8000/app/order/14/update/

Get notification for vendor or customer
GET http://127.0.0.1:8000/app/notification/users/userId/

Get daily sales report
GET http://127.0.0.1:8000/app/sales/report/
