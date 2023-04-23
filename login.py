import os
from tkinter import Image

from flask import Flask
from flask import request
from pyngrok import ngrok
import mysql.connector

from flask.templating import render_template
from werkzeug.utils import secure_filename

app = Flask('__main__',template_folder='templates')
ngrok.set_auth_token("2Oev4Kw5hUjlGkNlwIAvXSxXg2o_4Cg9gA8HirQsrtLXh8WyF")
public_url =  ngrok.connect(5000).public_url

dbConnection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='password',
    port='3306',
    database='shestore'
)
myCursor = dbConnection.cursor()

@app.route("/")
def home():
    return render_template('login_page.html')

@app.route("/userlogin",methods=['GET','POST'])
def userlogin():
  uname=request.form['username']
  passwd=request.form['password']
  myCursor.execute("select * from Customer where username = %s", (uname,))
  username = myCursor.fetchall();
  myCursor.execute("select * from Customer where pwd = %s", (passwd,))
  password = myCursor.fetchall();
  if len(username)==0 or len(password) ==0 :
      return render_template('user/LoginError.html')
  myCursor.execute("select * from Customer where username = %s and pwd = %s",(uname,passwd))
  result = myCursor.fetchall();
  try:
     if len(result) != 0:
        return render_template('user/home.html',data='welcome,' + uname)
     else:
        return render_template('user/signup.html',data='User doesn\'t exist please signup')
  except mysql.connector.Error as e:
    return render_template('generic/Error.html')

@app.route("/adminlogin",methods=['GET','POST'])
def adminlogin():
  return render_template('admin/login/admin_login_page.html',data='please login with your admin credentials')

@app.route('/verifyadminlogin',methods=['GET','POST'])
def verifyadminlogin():
  print('verifying admin login')
  uname=request.form['username']
  passwd=request.form['password']
  myCursor.execute("select * from Admin where username=%s and pwd=%s",(uname,passwd))
  result = myCursor.fetchall()
  if len(result) != 0:
    return render_template('admin/Admin.html',data='welcome,'+uname)
  else:
    return render_template('login_page.html',data='invalid admin credentials !')

@app.route("/signup",methods=['GET','POST'])
def signup():
  return render_template('user/signup.html')

@app.route("/adduser",methods=['GET','POST'])
def adduser():
  email=request.form['Email id']
  fname=request.form['First Name']
  lname=request.form['Last Name']
  uname=request.form['username']
  passwd=request.form['password']
  try:
    myCursor.execute("INSERT INTO Customer (`Email`, `Fname`, `Lname`, `username`, `pwd`) VALUES (%s,%s,%s,%s,%s)",
                     (email,fname,lname,uname,passwd))
    dbConnection.commit()
    return render_template('login_page.html',data="signup successful please login")
  except mysql.connector.Error as error:
    if error.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
        return render_template('login_page.html',data="existing user,please login!")
    else:
        return render_template('login_page.html',data="An error occurred while inserting the user data")

LIPS_FOLDER = os.path.join('static', 'lips_photo')
app.config['UPLOAD_FOLDER'] = LIPS_FOLDER

@app.route("/test")
def homeht():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'lips_photo.jpg')
    return render_template('user/User_homepage.html',lips_image = full_filename)
@app.route("/addAdminFunc", methods = ['GET','POST'])
def addAdminFunc():
    return render_template("admin/addAdmin/AddAdmin.html")
@app.route("/addAdmin", methods=['GET','POST'])
def addAdmin():
    fname = request.form['FirstName']
    lname = request.form['LastName']
    age = request.form['Age']
    uname = request.form['username']
    passwd = request.form['password']
    phoneNumber = request.form['PhoneNumber']
    try:
        myCursor.execute("INSERT INTO `Admin` ( `Phone_number`, `Age`, `Fname`, `Lname`, `username`, `pwd`) VALUES (%s,%s,%s,%s,%s,%s)",
                         (phoneNumber, age, fname, lname, uname, passwd))
        dbConnection.commit()
        return render_template('admin/addAdmin/AddAdmin.html', data="Admin added successfully !!")
    except mysql.connector.Error as error:
        if error.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            return render_template('admin/addAdmin/AddAdmin.html', data="existing user,please login!")
        else:
            return render_template('admin/addAdmin/AddAdmin.html', data = "An error occurred while inserting the admin data")

@app.route("/cancelAdmin", methods =['GET', 'POST'])
def cancelAdmin():
    return render_template('admin/addAdmin/AddAdmin.html')


# product details are
@app.route('/product/<int:product_id>',methods = ['GET','POST'])
def product(product_id):
    # Fetch product details from a database or data source
    # Replace the following lines with your own code
    myCursor.execute("select * from Products where ID = %s ",(product_id,))
    row = myCursor.fetchone()
    product = {
        'ID': row[0],
        'name': row[2],
        'description': "TestingProduct",
    }
    # Render a template that displays the product details
    return render_template('product_details.html', product=product)

@app.route('/listProducts',methods=['GET','POST'])
def listProducts():
    # Fetch a list of products from the database or data source
    # Replace the following lines with your own code
    # myCursor.execute("select * from Products")
    products = []
    # for row in myCursor:
    product = {
        'id': 1,
        'name': "lipstick",
        'description': "TestingProduct",
    }
    products.append(product)
    print(products)
    # Render a template that displays the list of products
    return render_template('product_page.html', data=products)

#manage products
@app.route('/manageProducts', methods = ['GET','POST'])
def manageProducts():
    return render_template('admin/products/manageproducts.html')

@app.route('/insertProducts', methods = ['GET', 'POST'])
def insertProducts():
    if request.method == 'POST':
       categoryId = request.form['categoryID']
       name = request.form['productName']
       rating = request.form['rating']
       price = request.form['price']
       adminId = request.form['adminId']
       query = "INSERT INTO Products (Category_ID, Name, Rating, Price, Admin_ID) VALUES (%s, %s, %s, %s, %s)"
       data = (categoryId, name, rating, price, adminId)
       myCursor.execute(query, data)
       dbConnection.commit()
       return render_template('admin/products/productInserted.html', data = "Product Inserted Successfully")
    #query database to get available options for dropdowns
    category_options_query = "SELECT * FROM Product_Categories"
    myCursor.execute(category_options_query)
    categories2 = myCursor.fetchall()
    categories1 = []
    for category in categories2:
        categories1.append(category[0])
    admin_options_query = "SELECT * FROM Admin"
    myCursor.execute(admin_options_query)
    admins1 = myCursor.fetchall()
    admins2 = []
    for admin in admins1:
        admins2.append(admin[0])
    return render_template('admin/products/insertproducts.html',
                              categories = categories1, admins = admins2)

@app.route('/addProduct', methods = ['GET','POST'])
def addProduct():
    categoryId = request.form['categoryID']
    name = request.form['productName']
    rating = request.form['rating']
    price = request.form['price']
    adminId = request.form['adminId']
    query = "INSERT INTO Products (Category_ID, Name, Rating, Price, Admin_ID) VALUES (%s, %s, %s, %s, %s)"
    data = (categoryId, name, rating, price, adminId)
    myCursor.execute(query, data)
    dbConnection.commit()
    return render_template ('admin/products/insertproducts.html', data = "Product inserted successfully!")
@app.route('/deleteProducts', methods = ['GET','POST'])
def deleteProducts():
    #todo :: do validations and remove from the db
  if request.method == 'POST':
    productId = request.form['productID']
    delete_query = "delete from Products where ID = %s"
    myCursor.execute(delete_query, (productId,))
    dbConnection.commit()
    return render_template('admin/products/deleteProducts.html', data = "Product deleted Successfully !!")
    # query database to get available options for dropdowns
  products_query = "SELECT * FROM Products"
  myCursor.execute(products_query)
  products = myCursor.fetchall()
  productsData = []
  for product in products:
      productsData.append(product[0])
  return render_template('admin/products/deleteProducts.html',products = productsData)


@app.route('/modifyProducts', methods = ['GET', 'POST'])
def modifyProducts():
    #Todo waiting on thushara for the templates
    if request.method == 'POST':
       productId = request.form['productID']
       categoryId = request.form['categoryID']
       name = request.form['productName']
       rating = request.form['rating']
       price = request.form['price']
       adminId = request.form['adminId']
       query = "UPDATE Products SET Category_ID = %s, Name = %s, Rating = %s, Price = %s, Admin_ID = %s where" \
               "ID = %s"
       data = (categoryId, name, rating, price, adminId, productId)
       myCursor.execute(query, data)
       dbConnection.commit()
       return render_template('admin/products/productInserted.html', data = "Product Inserted Successfully")
    # query database to get available options for dropdowns
    category_options_query = "SELECT * FROM Product_Categories"
    myCursor.execute(category_options_query)
    categories2 = myCursor.fetchall()
    categories1 = []
    for category in categories2:
        categories1.append(category[0])
    admin_options_query = "SELECT * FROM Admin"
    myCursor.execute(admin_options_query)
    admins1 = myCursor.fetchall()
    admins2 = []
    for admin in admins1:
        admins2.append(admin[0])
    return render_template('admin/products/modifyproducts.html',
                              categories = categories1, admins = admins2)

@app.route('/homePurchases', methods = ['GET'])
def homePurchases():
    return render_template('admin/products/purchases.html', Customer_ID = 4)

@app.route('/purchaseHistory', methods = ['GET','POST'])
def purchaseHistory():
    if request.method == 'POST':
        customerId = request.form['Customer_ID']
        productsPurchased = fetchProductsForACustomerId(customerId)
        productDetails = []
        for product in productsPurchased:
            pro = {}
            pro['ID'] = product[0]
            pro['Name'] = product[2]
            productDetails.append(pro)
    return render_template('admin/products/purchaseHistory.html', products=productDetails)

#manage customers
@app.route('/manageCustomers', methods = ['GET', 'POST'])
def manageCustomers():
    return render_template('admin/manageCustomers/managecustomers.html')

@app.route('/viewCustomersCount', methods = ['GET', 'POST'])
def viewCustomersCount():
    customers = fetchCustomers()
    customersCount = len(customers)
    return render_template('admin/manageCustomers/customersCount.html', customersCount = customersCount)

#Todo :: map these fields to an object in c
#Customer_ID,Email, Fname, Lname, username, pwd
@app.route('/viewAllCustomers', methods = ['GET', 'POST'])
def viewAllCustomers():
    customers = fetchCustomers()
    customerDetails = []
    for customer in customers:
        cus = {}
        cus['Customer_ID'] = customer[0]
        cus['Email'] = customer[1]
        cus['Fname'] = customer[2]
        cus['Lname'] = customer[3]
        cus['username'] = customer[4]
        cus['pwd'] = customer[5]
        customerDetails.append(cus)
    return render_template('admin/manageCustomers/viewCustomers.html', customerDetails = customerDetails)

#manage tickets
#status for a ticket can be PENDING, RESOLVED
#view tickets
@app.route('/viewTickets', methods = ['GET', 'POST'])
def viewTickets():
    # adminId = request.form['adminId']
    #Todo::praharsha :: if an admin can see only his tickets
    tickets = fetchTicketsOfAnAdmin()
    ticketDetails = []
    for ticket in tickets:
        ticket1 = {}
        ticket1['Ticket_ID'] = ticket[0]
        ticket1['Customer_ID'] = ticket[1]
        ticket1['Product_ID'] = ticket[2]
        ticket1['Type'] = ticket[3]
        ticket1['Description'] = ticket[4]
        ticket1['Admin_ID'] = ticket[5]
        ticket1['status'] = ticket[6]
        ticket1['comment'] = ticket[7]
        ticketDetails.append(ticket1)
    return render_template('admin/manageTickets/viewTickets.html', ticketDetails = ticketDetails)

@app.route('/renderResolveTicket/<int:ticketId>', methods = ['GET', 'POST'])
def renderResolveTicket(ticketId):
    return render_template('admin/manageTickets/resolveTicket.html', ticket_ID = ticketId)
@app.route('/resolveTicket/<int:ticketId>', methods = ['GET','POST'])
def resolveTicket(ticketId):
  if request.method == 'POST':
    comment = request.form['Comment']
    status = request.form['Status']
    adminId = request.form['AdminId']
    ticket_query = "UPDATE Tickets SET Admin_ID = %s, status = %s, comment = %s where Ticket_ID = %s"
    data = (adminId, status, comment, ticketId)
    myCursor.execute(ticket_query, data)
    dbConnection.commit()
  return render_template('admin/manageTickets/TicketResolved.html', data = "Ticket Resolved")

#manage categories
@app.route('/manageCategories', methods = ['GET', 'POST'])
def manageCategories():
    if request.method == 'POST':
       description = request.form['Description']
       AdminId = request.form['adminId']
       category_pic = request.files['category_pic']

       # Save uploaded image to static folder
       if category_pic.filename != '':
           filename = secure_filename(category_pic.filename)
           category_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

       query = "INSERT INTO Product_Categories (Description, Admin_ID) VALUES (%s, %s)"
       data = (description, AdminId)
       myCursor.execute(query, data)
       dbConnection.commit()
       return render_template('admin/manageCategories/ManageCategories.html', data="Category added Successfully")
    #query database to get available options for AdminID
    admin_options_query = "SELECT * FROM Admin"
    myCursor.execute(admin_options_query)
    admins1 = myCursor.fetchall()
    admins2 = []
    for admin in admins1:
        admins2.append(admin[0])
    return render_template('admin/manageCategories/ManageCategories.html',
                               admins = admins2)

@app.route('/file',methods=['GET','POST'])
def file():
  print(request.form['category_pic'])
  im1 = Image.open(r"static/Lips.JPG")
  im1=im1.save('static/'+request.form['category_pic'])

def fetchCustomers():
    customers_query = "select * from Customer"
    myCursor.execute(customers_query)
    result = myCursor.fetchall()
    return result

def fetchTicketsOfAnAdmin():
    tickets_query = "select * from Tickets "
    # where Admin_ID = %s"
    myCursor.execute(tickets_query)
    result = myCursor.fetchall()
    return result

def fetchProductsForACustomerId(customerId):
    purchase_query = "SELECT Product_ID FROM Purchase WHERE Customer_ID = %s"
    myCursor.execute(purchase_query, (customerId,))
    result = myCursor.fetchall()
    productIds = []
    for productId in result:
        productIds.append(productId[0])
    products_query = "SELECT * FROM Products WHERE ID IN (%s)" % (','.join(['%s'] * len(productIds)))
    myCursor.execute(products_query, tuple(productIds))
    return myCursor.fetchall()


print(f"To acces the Gloable link please click {public_url}")
app.run(port=8000)