from flask import Flask,jsonify
from flask import request
from pyngrok import ngrok
import mysql.connector

from flask.templating import render_template
app = Flask('__main__',template_folder='templates')
ngrok.set_auth_token("2Oev4Kw5hUjlGkNlwIAvXSxXg2o_4Cg9gA8HirQsrtLXh8WyF")
public_url =  ngrok.connect(5000).public_url

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='password',
    port='3306',
    database='project'
)

products = [
    {'name': 'Red Lipstick',
     'category': 'Lipstick',
     'price': 25,
     'color': 'Red'},
    {'name': 'Makeup Brush',
     'category': 'Brushes',
     'price': 40,
     'color': 'Black'},
]
myCursor = mydb.cursor()
myCursor.execute("SELECT * from Customer")
productCategories = myCursor.fetchall()
print(productCategories)

@app.route("/")
def home():
    return render_template('login_page.html')

@app.route("/login", methods=['GET','POST'])
def login():
  print('hi', request.form['username'])
  return render_template('1.html',data='welcome,'+request.form['username'])

@app.route("/signup", methods=['GET','POST'])
def signup():
  return render_template('1.html')

@app.route("/products", methods = ['GET', 'POST'])
def listRederedProducts() :
    return render_template('first.html', products = products )

@app.route("/categories", methods = ['GET','POST'])
def listProductCategories() :
    return render_template('Categories.html', categories = productCategories)


def loadSpecificCustomerFromDb(id):
    myCursor = mydb.cursor()
    myCursor.execute("SELECT * from Customer where Email = ?", (id))
    return myCursor.fetchall()


@app.route("/specificCustomer/<id>", methods = ['GET', 'POST'])
def listSpecificCustomer(id) :
    customer = loadSpecificCustomerFromDb(id)
    return jsonify(customer)

@app.route("/api/Products", methods = ['GET', 'POST'])
def list_products():
    return jsonify(products)

# @app.route('/purchases/<int:Customer_ID>', methods = ['GET', 'POST'])
# def purchases(Customer_ID):
#     #todo :: do purchases
#   if request.method == 'POST':
#     productsPurchased = fetchProductsForACustomerId(Customer_ID)
#     productDetails = []
#     for product in productsPurchased:
#         pro = {}
#         pro['ID'] = product[0]
#         pro['Name'] = product[2]
#         productDetails.append(pro)
#   return render_template('admin/products/purchaseHistory.html',Customer_ID=Customer_ID, products=productDetails)



print(f"To acces the Gloable link please click {public_url}")
if __name__=='__main__':
    app.run(port=5000)
    #
    # email = request.form['Email id']
    # fname = request.form['First Name']
    # lname = request.form['Last Name']
    # uname = request.form['username']
    # passwd = request.form['password']
    # try:
    #     myCursor.execute("insert into Customer(`Email`, `Fname`, `Lname`, `username`, `pwd`) values(?,?,?,?,?)",
    #                      (email, fname, lname, uname, passwd))
    #
    #     return render_template('login_page.html', data="signup successful please login")
    # except:
    #     return render_template('login_page.html', data="existing user,please login!")