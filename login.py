import os
from tkinter import Image

from flask import Flask, session, url_for
from flask import request
from pyngrok import ngrok
import mysql.connector

from flask.templating import render_template
from werkzeug.utils import secure_filename, redirect

app = Flask('__main__', static_folder='static', template_folder='templates')
ngrok.set_auth_token("2Oev4Kw5hUjlGkNlwIAvXSxXg2o_4Cg9gA8HirQsrtLXh8WyF")
public_url =  ngrok.connect(5000).public_url

dbConnection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='password',
    port='3306',
    database='shestoreproject'
)
myCursor = dbConnection.cursor()

@app.route("/")
def home():
    return render_template('login_page.html')

"""@app.route("/userlogin",methods=['GET','POST'])
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
        return render_template('user/signup_order.html',data='User doesn\'t exist please signup')
  except mysql.connector.Error as e:
    return render_template('generic/Error.html')"""


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    uname = request.form['username']
    passwd = request.form['password']
    myCursor.execute("select customer_id from customer where username=%s and pwd=%s", (uname, passwd,))
    c = list(myCursor.fetchall())
    if len(c) and len(c[0]):
        categories_data = fetch_categories()
        global customer_id
        customer_id = (c[0][0])
        session['logged_in'] = True
        return render_template('User_homepage.html', categories=categories_data)
    else:
        return render_template('signup.html', data='User doesnot exist please signup')

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
    global admin_id
    admin_id = result[0][0]
    session['logged_in'] = True
    return render_template('admin/Admin.html', data='welcome,'+uname)
  else:
    return render_template('login_page_old.html', data='invalid admin credentials !')

@app.route('/renderAdminHomePage', methods = ['GET', 'POST'])
def renderAdminHomePage():
    myCursor.execute("select * from admin where Admin_ID = %s",( admin_id,))
    result = myCursor.fetchall()
    for res in result:
        uname = res[5]
    return render_template('admin/Admin.html', data='welcome,'+uname)

@app.route("/signup",methods=['GET','POST'])
def signup():
  return render_template('signup_order.html')

"""@app.route("/adduser",methods=['GET','POST'])
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
    return render_template('login_page_old.html',data="signup successful please login")
  except mysql.connector.Error as error:
    if error.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
        return render_template('login_page_old.html',data="existing user,please login!")
    else:
        return render_template('login_page_old.html',data="An error occurred while inserting the user data")"""

@app.route("/adduser",methods=['GET','POST'])
def adduser():
  email=request.form['Email id']
  fname=request.form['First Name']
  lname=request.form['Last Name']
  uname=request.form['username']
  passwd=request.form['password']
  try:
    try:
      myCursor.execute("insert into customer(Email,Fname,Lname,username,pwd) values(%s,%s,%s,%s,%S)",(email,fname,lname,uname,passwd,))
      dbConnection.commit()
    except:
      myCursor.execute("insert into customer(Email,Fname,Lname,username,pwd) values(%s,%s,%s,%s,%s)",(email,fname,lname,uname,passwd))
      dbConnection.commit()
    return render_template('login_page.html',data="signup successful please login")
  except:
    return render_template('login_page.html',data="existing user,please login!")
@app.route('/logout')
def logout():
  session['logged_in']=False
  return redirect('/')

# LIPS_FOLDER = os.path.join('static', 'lips_photo')
# app.config['UPLOAD_FOLDER'] = LIPS_FOLDER
STATIC_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = STATIC_FOLDER

@app.route("/test")
def homeht():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'lips_photo.jpg')
    return render_template('user/User_homepage_old.html',lips_image = full_filename)
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
    return render_template('product_details_old.html', product=product)

@app.route('/listProducts',methods=['GET','POST'])
def listProducts():
    products = []
    product = {
        'id': 1,
        'name': "lipstick",
        'description': "TestingProduct",
    }
    products.append(product)
    print(products)

    # Render a template that displays the list of products
    return render_template('product_page_old.html', data=products)

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
    if request.method == 'POST':
        try:
           categoryId = request.form['categoryID']
           name = request.form['productName']
           description = request.form['productDescription']
           color = request.form['productColor']
           brand = request.form['productBrand']
           quantity = request.form['productQuantity']
           rating = request.form['rating']
           price = request.form['price']
           product_pic = request.files['product_pic']
        except KeyError as e:
            return "Bad request: missing form field - {}".format(e), 400
    # Save uploaded image of the product to static folder
    if product_pic.filename != '':
        filename = secure_filename(name+'.JPG')
        product_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    query = "INSERT INTO Products (Category_ID, Name, Description,Color,Brand,Quantity,Rating, Price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    data = (categoryId, name, description, color, brand, quantity, rating, price)
    try:
        myCursor.execute(query, data)
        dbConnection.commit()
        return render_template('admin/products/insertproducts.html', data = "Product inserted successfully!")
    except Exception as e:
        dbConnection.rollback()
        return render_template('admin/products/insertproducts.html', data = "Error inserting product: {}".format(e))

@app.route('/deleteProducts', methods = ['GET','POST'])
def deleteProducts():
    #todo :: do validations and remove from the db
  if request.method == 'POST':
    productId = request.form['productID']
    delete_query = "delete from Products where ID = %s"
    try:
      myCursor.execute(delete_query, (productId,))
      dbConnection.commit()
    except:
        return render_template('admin/products/deleteProducts.html', data = "Error deleting product.")
    return render_template('admin/products/deleteProducts.html', data="Product deleted Successfully !!")
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
    if request.method == 'POST':
      try:
       productId = request.form['productID']
       categoryId = request.form['categoryID']
       name = request.form['productName']
       description = request.form['productDescription']
       color = request.form['productColor']
       brand = request.form['productBrand']
       quantity = request.form['productQuantity']
       rating = request.form['rating']
       price = request.form['price']
       product_pic = request.files['product_pic']
      except KeyError as e:
           return "Bad request: missing form field - {}".format(e), 400
      # Save uploaded image of the product to static folder
      if product_pic.filename != '':
          filename = secure_filename(product_pic.filename)
          product_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      query = "UPDATE Products SET Category_ID = %s, Name = %s,Description = %s, Color = %s, Brand = %s, Quantity = %s, Rating = %s, Price = %s where ID = %s"
      data = (categoryId, name,description, color,brand,quantity, rating, price, productId)
      try:
        myCursor.execute(query, data)
        dbConnection.commit()
        return render_template('admin/products/modifyproducts.html', data = "Product Modified Successfully!")
      except:
          return render_template('admin/products/modifyproducts.html', data = "Error Occurred while modifying product info !")
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
    products_query = "SELECT * FROM Products"
    myCursor.execute(products_query)
    products = myCursor.fetchall()
    productsData = []
    for product in products:
        productsData.append(product[0])
    return render_template('admin/products/modifyproducts.html',
                              categories = categories1, admins = admins2, products = productsData)

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
    return render_template('admin/manageCustomers/managecustomers.html',data = "The total no of registered users are ", customersCount = customersCount)

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

@app.route('/viewPurchasesMadeByEachCustomer', methods = ['GET', 'POST'])
def viewPurchasesMadeByEachCustomer():
    purchases_query = "select Customer_ID, count(*) from purchase group by 1"
    myCursor.execute(purchases_query)
    result = myCursor.fetchall()
    customerDetails = []
    for customer in result:
       cus = {}
       cus['Customer_ID'] = customer[0]
       cus['count'] = customer[1]
       customerDetails.append(cus)
    return render_template('admin/manageCustomers/viewProductsPurchasedByEachCustomer.html', customerDetails = customerDetails)

@app.route('/avgRatingForEachCategory', methods = ['GET', 'POST'])
def avgRatingForEachCategory():
    avg_query = "SELECT pc.Description, COUNT(p.ID) AS Num_Products," \
                " AVG(p.Rating) AS Avg_Rating FROM Product_Categories pc" \
                " LEFT JOIN Products p ON p.Category_ID = pc.Category_ID GROUP BY pc.Category_ID"
    myCursor.execute(avg_query)
    result = myCursor.fetchall()
    ratingDetails = []
    for res in result:
        rating = {}
        rating['Description'] = res[0]
        rating['Count'] = res[1]
        rating['avg_rating'] = res[2]
        ratingDetails.append(rating)
    return render_template('admin/manageCustomers/avgRatingForEachCategory.html',ratingDetails = ratingDetails )

@app.route('/viewTicketsResolved', methods = ['GET','POST'])
def viewTicketsResolved():
    ticket_query = "SELECT DISTINCT c.Fname, c.Lname FROM Customer c INNER JOIN Tickets t ON c.Customer_ID = t.Customer_ID INNER JOIN Admin a ON a.Admin_ID = t.Admin_ID WHERE t.status = 'RESOLVED';"
    myCursor.execute(ticket_query)
    result = myCursor.fetchall()
    ticketDetails = []
    for ticket in result:
        t = {}
        t['Fname'] = ticket[0]
        t['Lname'] = ticket[1]
        ticketDetails.append(t)
    return render_template('admin/manageCustomers/viewTicketsResolvedQuery.html', ticketDetails=ticketDetails)

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
    ticket_query = "UPDATE Tickets SET Admin_ID = %s, status = %s, comment = %s where Ticket_ID = %s"
    data = (admin_id, status, comment, ticketId)
    myCursor.execute(ticket_query, data)
    dbConnection.commit()
  return render_template('admin/manageTickets/resolveTicket.html', ticket_ID = ticketId, data = "Ticket Resolved!!")

#manage categories
@app.route('/manageCategories', methods = ['GET', 'POST'])
def manageCategories():
    if request.method == 'POST':
       description = request.form['Description']
       category_pic = request.files['category_pic']

       # Save uploaded image to static folder
       if category_pic.filename != '':
           filename = secure_filename(description+'.JPG')
           category_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

       query = "INSERT INTO Product_Categories (Description, Admin_ID) VALUES (%s, %s)"
       data = (description,admin_id )
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


@app.route('/getfilteredproducts', methods=['get', 'post'])
def getfilteredproducts():
    category_id = (request.args.get('id'))
    print(category_id)
    filtered_products_data = []
    try:
        myCursor.execute("select * from products where category_id=%s", (category_id,))
        c = myCursor.fetchall()
    except:
         myCursor.execute("select * from products where category_id=%s", (category_id))
         c= myCursor.fetchall()
    products_data, brand_data, color_data = fetch_products(c)
    brand_filter = (request.form.getlist('Brand'))
    brand_ids = []
    color_filter = (request.form.getlist('Color'))
    color_ids = []
    rating_filter = (request.form.getlist('star'))
    rating_ids = []
    sort_filter = (request.form.getlist('Sort'))
    price_filter = (request.form.getlist('Price'))
    price_ids = []
    if len(brand_filter) == 0 and len(color_filter) == 0 and len(rating_filter) == 0 and len(sort_filter) == 0 and len(
            price_filter) == 0:
        ###########################################################################3
        return render_template('noproducts.html', message="no filter chosen to display products!")
    data = {}
    for brand in brand_filter:
        try:
            myCursor.execute('select id from products where brand=%s and category_id=%s', (brand, category_id,))
            c=myCursor.fetchall()
        except:
            myCursor.execute('select id from products where brand=%s and category_id=%s', (brand, category_id))
            c = myCursor.fetchall()
        for row in c:
            brand_ids.append(row[0])
    if len(brand_ids):
        data['brand_ids'] = set(brand_ids)
    if len(brand_filter) > 0 and len(brand_ids) == 0:
        data['brand_ids'] = set()
    for color in color_filter:
        try:
            myCursor.execute('select id from products where color=%s and category_id=%s', (color, category_id,))
            c = myCursor.fetchall()
        except:
            myCursor.execute('select id from products where color=%s and category_id=%s', (color, category_id))
            c = myCursor.fetchall()
        for row in c:
            color_ids.append(row[0])
    if len(color_ids):
        data['color_ids'] = set(color_ids)
    if len(color_filter) > 0 and len(color_ids) == 0:
        data['color_ids'] = set()
    for star in rating_filter:
        try:
            myCursor.execute('select id from products where rating >= %s and category_id=%s', (star, category_id,))
            c = myCursor.fetchall()
        except:
            myCursor.execute('select id from products where rating >= %s and category_id=%s', (star, category_id))
            c = myCursor.fetchall()
        for row in c:
            rating_ids.append(row[0])
    if len(rating_ids):
        data['rating_ids'] = set(rating_ids)
    if len(rating_filter) > 0 and len(rating_ids) == 0:
        data['rating_ids'] = set()
    for price in price_filter:
        if price == '1':
            min = 1
            max = 20
        elif price == '2':
            min = 20
            max = 50
        else:
            min = 50
            max = 100
        try:
            myCursor.execute('select id from products where category_id=%s and price between %s and %s ',
                             (category_id, min, max,))
            c = myCursor.fetchall()
        except:
            myCursor.execute('select id from products where category_id=%s and price between %s and %s ',
                             (category_id, min, max))
            c = myCursor.fetchall()
        for row in c:
            price_ids.append(row[0])
    if len(price_ids):
        data['price_ids'] = set(price_ids)
    if len(price_filter) > 0 and len(price_ids) == 0:
        data['price_ids'] = set()

    print('products after applyig brand,rating,price', data)
    product_id = {}
    product_ids = list(data.values())
    if len(product_ids):
        product_id = product_ids[0]
    for new_id in product_ids[1:]:
        product_id = product_id.intersection(new_id)
    product_ids = (tuple(product_id))
    print(product_ids)
    if len(product_ids):
        for product_id in product_ids:
            d = {}
            try:
                myCursor.execute('select * from products where id=%s', (str(product_id),))
                c = myCursor.fetchall()
            except:
                myCursor.execute('select * from products where id=%s', (str(product_id)))
                c = myCursor.fetchall()
            for row in c:
                print('hello data', row)
                d['id'] = row[0]
                d['image_name'] = row[2]+".JPG"
                d['name'] = row[2]
                d['price'] = "$ " + str(row[8])
            filtered_products_data.append(d)
        print(filtered_products_data)
        # return render_template("product_page.html",cat_id=category_id,data=products_data,brand=brand_data,color=color_data)
    if len(list(sort_filter)):
        print("hi")
        print(products_data)
        sort = list(sort_filter)[0]
        if len(filtered_products_data):
            products_data = filtered_products_data
        if sort == "0":  # high to low sorting
            products_data = (sorted(products_data, key=lambda i: float(i['price'].replace('$ ','')), reverse=True))
        else:
            products_data = (sorted(products_data, key=lambda i: float(i['price'].replace('$ ',''))))

        return render_template("product_page.html", selected_brand=brand_filter, selected_color=color_filter,
                               selected_price=price_filter, selected_rating=rating_filter, selected_sort=sort_filter,
                               cat_id=category_id, data=products_data, brand=brand_data, color=color_data)
    print('filtered_products_data', filtered_products_data)
    if len(filtered_products_data):
        return render_template("product_page.html", selected_brand=brand_filter, selected_color=color_filter,
                               selected_price=price_filter, selected_rating=rating_filter, selected_sort=sort_filter,
                               cat_id=category_id, data=filtered_products_data, brand=brand_data, color=color_data)

    else:
        ############################################################
        return render_template('noproducts.html',
                               message="no products found matching your filters please try with other filters")


@app.route('/checkout', methods=['get', 'post'])
def checkout():
    order_value = request.args.get('order_value')
    print(order_value)
    try:
        myCursor.execute('select count(*) from cart where customer_id=%s', (customer_id,))
        c = myCursor.fetchall()
    except:
        myCursor.execute('select count(*) from cart where customer_id=%s', (customer_id))
        c = myCursor.fetchall()
    cart_size = 0
    order_count = 0
    for row in c:
        cart_size = row[0]
    if cart_size == 0:
        return redirect(url_for('displaycart', message="cannot checkout empty cart"))
    else:
        try:
            myCursor.execute('select * from cart where customer_id=%s', (customer_id,))
            c = myCursor.fetchall()
        except:
            myCursor.execute('select * from cart where customer_id=%s', (customer_id))
            c = myCursor.fetchall()

        myCursor.execute('select count(distinct(order_id)) from orders')
        c1 = myCursor.fetchall()
        for row in c1:
            order_count = row[0]
        for row in c:
            try:
                myCursor.execute('insert into orders(order_id,customer_id,product_id,quantity,status) values(%s,%s,%s,%s,%s)',
                                 (order_count + 1, row[0], row[1], row[2],"order placed",))
                dbConnection.commit()
            except:
                myCursor.execute('insert into orders(order_id,customer_id,product_id,quantity,status) values(%s,%s,%s,%s,%s)',
                                 (order_count + 1, row[0], row[1], row[2],"order placed"))
                dbConnection.commit()

            try:
                try:
                    myCursor.execute('insert into purchase values(%s,%s)', (row[0], row[1],))
                    dbConnection.commit()
                except:
                    myCursor.execute('insert into purchase values(%s,%s)', (row[0], row[1]))
                    dbConnection.commit()
            except:
                pass

        return redirect(url_for('displayordersuccesful', order_id=order_count + 1))


@app.route('/displayproduct', methods=['get', 'post'])
def displayproduct():
    id = request.args.get('id')
    message = request.args.get('message')
    if message == None:
        message = ''
    try:
        myCursor.execute("select * from products where id=%s", (id,))
        c = myCursor.fetchall()
    except:
        myCursor.execute("select * from products where id=%s", (id))
        c = myCursor.fetchall()
    product_details = get_product_details(c)
    return render_template('product_details.html', message=message, product_id=id, data=product_details)


@app.route('/displaycart', methods=['GET', 'POST'])
def displaycart():
    message = request.args.get('message')
    if message == None:
        message = ''
    try:
        myCursor.execute('select * from cart where customer_id=%s', (customer_id,))
        c = myCursor.fetchall()
    except:
        myCursor.execute('select * from cart where customer_id=%s', (customer_id))
        c = myCursor.fetchall()
    pid = []
    qty = []
    cartdata = []
    cart_value = 0
    for row in c:
        pid.append(row[1])
        qty.append(row[2])
    for i in range(len(pid)):
        try:
            myCursor.execute('select * from products where id=%s', (str(pid[i]),))
            c = myCursor.fetchall()
        except:
            myCursor.execute('select * from products where id=%s', (str(pid[i])))
            c = myCursor.fetchall()
        for row in c:
            data = {}
            data['name'] = row[2]
            data['description'] = row[3]
            data['pid'] = row[0]
            data['quantity'] = qty[i]
            if int(data['quantity']) <= 0:
                try:
                    myCursor.execute('delete from cart where customer_id=%s and product_id=%s', (customer_id, row[0],))
                    dbConnection.commit()
                except:
                    myCursor.execute('delete from cart where customer_id=%s and product_id=%s', (customer_id, row[0]))
                    dbConnection.commit()
                continue
            data['price'] = row[8]
            data['amount'] = (float(data['quantity']) * float(data['price']))
            cart_value += data['amount']
            data['image_name'] = row[2] + ".JPG"
            cartdata.append(data)
    return render_template("cart.html", cart_data=cartdata, message=message, cart_value=cart_value)


@app.route('/displayorders', methods=['get', 'post'])
def displayorders():
    try:
        myCursor.execute('select * from orders where customer_id=%s order by order_id desc', (customer_id,))
        c = myCursor.fetchall()
    except:
        myCursor.execute('select * from orders where customer_id=%s order by order_id desc', (customer_id))
        c = myCursor.fetchall()
    pid = []
    qty = []
    status = []
    ordersdata = []
    for row in c:
        pid.append(row[2])
        qty.append(row[3])
        status.append(row[5])
    for i in range(len(pid)):
        try:
            myCursor.execute('select * from products where id=%s', (str(pid[i]),))
            c = myCursor.fetchall()
        except:
            myCursor.execute('select * from products where id=%s', (str(pid[i])))
            c = myCursor.fetchall()
        for row in c:
            data = {}
            data['name'] = row[2]
            data['description'] = row[3]
            data['pid'] = row[0]
            data['quantity'] = qty[i]
            data['status'] = status[i]
            data['price'] = row[8]
            data['amount'] = (float(data['quantity']) * float(data['price']))
            data['image_name'] = row[2] + ".JPG"
            ordersdata.append(data)
    return render_template("myorders.html", orders_data=ordersdata)


@app.route('/displayordersuccesful', methods=['get', 'post'])
def displayordersuccesful():
    order_id = request.args.get('order_id')
    try:
        myCursor.execute('select * from cart where customer_id=%s', (customer_id,))
        c2= myCursor.fetchall()
    except:
        myCursor.execute('select * from cart where customer_id=%s', (customer_id))
        c2= myCursor.fetchall()
    pid = []
    qty = []
    ordersdata = []
    for row in c2:
        pid.append(row[1])
        qty.append(row[2])
    for i in range(len(pid)):
        try:
            myCursor.execute('update products set quantity=quantity-%s where id=%s', (int(qty[i]), str(pid[i]),))
            dbConnection.commit()
        except:
            print('error in update in ordsucc')
            myCursor.execute('update products set quantity=quantity-%s where id=%s', (int(qty[i]), str(pid[i])))
            dbConnection.commit()
        try:
            myCursor.execute('select * from products where id=%s', (str(pid[i]),))
            c = myCursor.fetchall()
            for row in c:
                print('row data', row)
                data = {}
                data['name'] = row[2]
                data['description'] = row[3]
                data['pid'] = row[0]
                data['quantity'] = qty[i]
                data['price'] = row[8]
                data['amount'] = (float(data['quantity']) * float(data['price']))
                data['image_name'] = row[2] + ".JPG"
                ordersdata.append(data)
        except:
            print('error in selecti updatesucc')
            myCursor.execute('select * from products where id=%s', (str(pid[i])))
            c = myCursor.fetchall()
            for row in c:
                print('row data', row)
                data = {}
                data['name'] = row[2]
                data['description'] = row[3]
                data['pid'] = row[0]
                data['quantity'] = qty[i]
                data['price'] = row[8]
                data['amount'] = (float(data['quantity']) * float(data['price']))
                data['image_name'] = row[2] + ".JPG"
                ordersdata.append(data)
        print('orders data', ordersdata)
        try:
            myCursor.execute('delete from cart where customer_id=%s', (customer_id,))
            dbConnection.commit()
        except:
            myCursor.execute('delete from cart where customer_id=%s', (customer_id))
            dbConnection.commit()
    return render_template("ordersuccesful.html", orders_data=ordersdata,
                           message="order placed with order id:" + str(order_id))


@app.route('/addquantity', methods=['GET', 'POST'])
def addquantity():
    id = request.args.get('id')
    present_quantity = request.args.get('present_quantity')
    message = ''
    try:
        myCursor.execute('select quantity from products where id=%s', (id,))
        c = myCursor.fetchall()
    except:
        myCursor.execute('select quantity from products where id=%s', (id))
        c = myCursor.fetchall()
    max_qty = ''
    for row in c:
        qty = row[0]
    max_qty = int(qty)
    if max_qty > int(present_quantity):
        try:
            try:
                myCursor.execute('update cart set quantity=quantity+1 where customer_id=%s and product_id=%s',
                                 (customer_id, id,))
                dbConnection.commit()
            except:
                myCursor.execute('update cart set quantity=quantity+1 where customer_id=%s and product_id=%s',
                                 (customer_id, id))
                dbConnection.commit()
        except:
            message = 'unable to increase product quantity'
    else:
        message = 'product  maximum limit reached'
    return redirect(url_for('displaycart', message=message))


@app.route('/reducequantity', methods=['GET', 'POST'])
def reducequantity():
    id = request.args.get('id')
    message = ''
    try:
        try:
            myCursor.execute('update cart set quantity=quantity-1 where customer_id=%s and product_id=%s',
                             (customer_id, id,))
            dbConnection.commit()
        except:
            myCursor.execute('update cart set quantity=quantity-1 where customer_id=%s and product_id=%s',
                             (customer_id, id))
            dbConnection.commit()
    except:
        message = 'unable to decrease product quantity'
    return redirect(url_for('displaycart', message=message))


@app.route('/removefromcart', methods=['GET', 'POST'])
def removefromcart():
    id = request.args.get('id')
    message = ''
    try:
        try:
            myCursor.execute('delete from cart where customer_id=%s and product_id=%s', (customer_id, id,))
            dbConnection.commit()
        except:
            myCursor.execute('delete from cart where customer_id=%s and product_id=%s', (customer_id, id))
            dbConnection.commit()
        message = 'product deleted from cart'
    except:
        message = 'unable to remove product'
    return redirect(url_for('displaycart', message=message))


@app.route('/movetowishlist', methods=['GET', 'POST'])
def movetowishlist():
    id = request.args.get('id')
    message = ''
    try:
        myCursor.execute('delete from cart where customer_id=%s and product_id=%s', (customer_id, id,))
        dbConnection.commit()
    except:
        myCursor.execute('delete from cart where customer_id=%s and product_id=%s', (customer_id, id))
        dbConnection.commit()
    try:
        try:
            myCursor.execute('insert into wishlist values(%s,%s)', (customer_id, id,))
            dbConnection.commit()
        except:
            myCursor.execute('insert into wishlist values(%s,%s)', (customer_id, id))
            dbConnection.commit()
        message = 'product moved to wishlist'
    except:
        message = 'product already in wishlist'
    return redirect(url_for('displaycart', message=message))


@app.route('/removefromwishlist', methods=['GET', 'POST'])
def removefromwishlist():
    id = request.args.get('id')
    message = ''
    try:
        try:
            myCursor.execute('delete from wishlist where customer_id=%s and product_id=%s', (customer_id, id,))
            dbConnection.commit()
        except:
            myCursor.execute('delete from wishlist where customer_id=%s and product_id=%s', (customer_id, id))
            dbConnection.commit()
        message = 'item deleted from wishlist'
    except:
        message = 'deletion unsuccesful'
    return redirect(url_for('displaywishlist', message=message))


@app.route('/movetocart', methods=['GET', 'POST'])
def movetocart():
    id = (request.args.get('id'))
    message = ''
    try:
        try:
            myCursor.execute('insert into cart values(%s,%s,1)', (customer_id, id))
            dbConnection.commit()
        except:
            myCursor.execute('insert into cart values(%s,%s,1)', (customer_id, id,))
            dbConnection.commit()
    except:
        try:
            myCursor.execute('update cart set quantity=quantity+1 where customer_id=%s and product_id=%s',
                             (customer_id, id,))
            dbConnection.commit()
        except:
            myCursor.execute('update cart set quantity=quantity+1 where customer_id=%s and product_id=%s',
                             (customer_id, id))
            dbConnection.commit()

    try:
        try:
            myCursor.execute('delete from wishlist where customer_id=%s and product_id=%s', (customer_id, id,))
            dbConnection.commit()
        except:
            myCursor.execute('delete from wishlist where customer_id=%s and product_id=%s', (customer_id, id))
            dbConnection.commit()

        message = 'item moved to cart '
    except:
        message = 'move to cart unsuccesful'
    return redirect(url_for('displaywishlist', message=message))


@app.route('/displaywishlist', methods=['GET', 'POST'])
def displaywishlist():
    message = request.args.get('message')
    if message == None:
        message = ''
    try:
        myCursor.execute('select * from wishlist where customer_id=%s', (customer_id,))
        c = myCursor.fetchall()
    except:
        myCursor.execute('select * from wishlist where customer_id=%s', (customer_id))
        c = myCursor.fetchall()
    pid = []
    wishlistdata = []
    for row in c:
        pid.append(row[1])
    for id in pid:
        try:
            myCursor.execute('select * from products where id=%s', (str(id),))
            c = myCursor.fetchall()
        except:
            myCursor.execute('select * from products where id=%s', (str(id)))
            c = myCursor.fetchall()
        for row in c:
            data = {}
            data['name'] = row[2]
            data['description'] = row[3]
            data['pid'] = row[0]
            data['image_name'] = row[2] + ".JPG"
            wishlistdata.append(data)
    return render_template("wishlist.html", wishlist_data=wishlistdata, message=message)


@app.route('/addtocart', methods=['get', 'post'])
def addtocart():
    id = (request.args.get('id'))
    message = ''
    try:
        try:
            myCursor.execute('insert into cart values(%s,%s,1)', (customer_id, id,))
            dbConnection.commit()
        except:
            myCursor.execute('insert into cart values(%s,%s,1)', (customer_id, id))
            dbConnection.commit()
        message = 'product added to cart'
    except:
        try:
            myCursor.execute('select quantity from products where id=%s', (id,))
            c = myCursor.fetchall()
        except:
            myCursor.execute('select quantity from products where id=%s', (id))
            c = myCursor.fetchall()
        max_qty = 0
        for row in c:
            max_qty = int(row[0])
        try:
            myCursor.execute('select quantity from cart where customer_id= %s and product_id=%s', (customer_id, id,))
            c = myCursor.fetchall()
        except:
            myCursor.execute('select quantity from cart where customer_id= %s and product_id=%s', (customer_id, id))
            c = myCursor.fetchall()

        present_qty = 0
        for row in c:
            present_qty = int(row[0])
        if max_qty > present_qty:
            try:
                myCursor.execute('update cart set quantity=quantity+1 where customer_id=%s and product_id=%s',
                                 (customer_id, id,))
                dbConnection.commit()
            except:
                myCursor.execute('update cart set quantity=quantity+1 where customer_id=%s and product_id=%s',
                                 (customer_id, id))
                dbConnection.commit()

            message = 'product added to cart'
        else:
            message = 'product maximum limit reached'
    return redirect(url_for('displayproduct', id=id, message=message))


@app.route('/addtowishlist', methods=['get', 'post'])
def addtowishlist():
    id = (request.args.get('id'))
    message = ''
    try:
        try:
            myCursor.execute('insert into wishlist values(%s,%s)', (customer_id, id,))
            dbConnection.commit()
        except:
            myCursor.execute('insert into wishlist values(%s,%s)', (customer_id, id))
            dbConnection.commit()

        message = 'product added to wishlist'
    except:
        message = 'product already in wishlist'
    return redirect(url_for('displayproduct', id=id, message=message))


@app.route('/verifycategory', methods=['GET', 'POST'])
def verifycategory():
    id = (request.args.get('id'))
    try:
        myCursor.execute("select * from products where category_id=%s", (id,))
        c = myCursor.fetchall()

    except:
        myCursor.execute("select * from products where category_id=%s", (id,))
        c = myCursor.fetchall()

    products_data, brand, color = fetch_products(c)
    print(brand)
    return render_template("product_page.html", cat_id=id, data=products_data, brand=brand, color=color)

@app.route('/homepage',methods=['GET','POST'])
def homepage():
  categories_data=fetch_categories()
  return render_template('User_homepage.html',categories=categories_data)


@app.route('/displayprofile', methods=['get', 'post'])
def displayprofile():
    return render_template("profile.html")


@app.route('/showuserdetails', methods=['get', 'post'])
def showuserdetails():
    data = {}
    try:
        myCursor.execute("select * from customer where customer_id=%s", (customer_id,))
        c = myCursor.fetchall()
    except:
        myCursor.execute("select * from customer where customer_id=%s", (customer_id))
        c = myCursor.fetchall()
    for row in c:
        data['fname'] = row[2]
        data['lname'] = row[3]
        data['uname'] = row[4]
        data['email'] = row[1]

    return render_template("ViewDetails.html", data=data)


@app.route('/displaycustomersupport', methods=['get', 'post'])
def displaycustomersupport():
    return render_template("customersupport.html")


@app.route('/viewtickets', methods=['get', 'post'])
def viewtickets():
    ticketdata = []
    try:
        myCursor.execute("select * from tickets where customer_id=%s order by ticket_id desc", (customer_id,))
        c = myCursor.fetchall()
    except:
        myCursor.execute("select * from tickets where customer_id=%s order by ticket_id desc", (customer_id))
        c = myCursor.fetchall()

    for row in c:
        data = {}
        data['ticket_id'] = row[0]
        data['type'] = row[3]
        data['description'] = row[4]
        data['status'] = row[6]
        data['comment'] = row[7]
        id = row[2]
        data['id'] = id
        name = ''
        try:
            myCursor.execute("select name from products where id=%s", (id,))
            c1= myCursor.fetchall()
        except:
            myCursor.execute("select name from tickets where id=%s", (id))
            c1 = myCursor.fetchall()
        for row in c1:
            name = row[0]
        data['name'] = name

        ticketdata.append(data)

    return render_template("viewtickets.html", data=ticketdata)


@app.route('/raiseticket', methods=['get', 'post'])
def raiseticket():
    productdata = []
    try:
        myCursor.execute("select product_id from orders where customer_id=%s order by order_id desc", (customer_id,))
        c = myCursor.fetchall()
    except:
        myCursor.execute("select product_id from orders where customer_id=%s order by order_id desc", (customer_id))
        c = myCursor.fetchall()
    for row in c:
        data = {}
        id = row[0]
        name = ''
        try:
            myCursor.execute("select name from products where id=%s", (id,))
            c1 = myCursor.fetchall()
        except:
            myCursor.execute("select name from tickets where id=%s", (id))
            c1 = myCursor.fetchall()
        for row in c1:
            name = row[0]
            data['id'] = id
            data['name'] = name
        productdata.append(data)

    return render_template("raiseticket.html", products_data=productdata)


@app.route('/ticketraisesuccesful', methods=['get', 'post'])
def ticketraisesuccesful():
    description = str(request.form['Description'])
    query_type = str(request.form['Type'])
    id = int(request.form['product'])
    print()
    try:
        myCursor.execute("insert into tickets(customer_id,product_id,type,description) values(%s,%s,%s,%s)",
                         (customer_id, id, query_type, description,))
        dbConnection.commit()
    except:
        myCursor.execute("insert into tickets(customer_id,product_id,type,description) values(%s,%s,%s,%s)",
                         (customer_id, id, query_type, description))
        dbConnection.commit()
    return redirect(url_for('viewtickets'))


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

def fetch_categories():
  data=[]
  myCursor.execute("select * from product_categories")
  c = myCursor.fetchall()
  for row in c:
    d={}
    id=row[0]
    d['id']=id
    name=row[1]
    d['name']=name
    name=name+".JPG"
    d['image_name'] = name
    data.append(d)
  print(data)
  return data
def fetch_products(c):
  data=[]
  brand=[]
  color=[]
  for row in c:
    d={}
    if row[6]>0:
      d['id']=row[0]
      d['image_name']=row[2]+".JPG"
      color.append(row[4])
      brand.append(row[5])
      d['name']=row[2]
      d['price']="$ "+str(row[8])
      data.append(d)
  brand=list(set(brand))
  color=list(set(color))
  return (data,brand,color)
def get_product_details(c):
  data={}
  for row in c:
    data['product_id']=row[0]
    data['name']=row[2]
    data['image_name']=row[2]+".JPG"
    data['description']=row[3]
    data['rating']=row[7]
    data['price']='$ '+str(row[8])
  print(data)
  return data
print(f"To acces the Gloable link please click {public_url}")
if __name__=='__main__':
    app.secret_key=os.urandom(12)
    app.run(port=8000)