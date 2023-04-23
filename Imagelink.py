# from pyngrok import ngrok
# import mysql.connector
#
# from flask.templating import render_template
# app = Flask('__main__',template_folder='templates')
# ngrok.set_auth_token("2Oev4Kw5hUjlGkNlwIAvXSxXg2o_4Cg9gA8HirQsrtLXh8WyF")
# public_url =  ngrok.connect(5000).public_url
#
# dbConnection = mysql.connector.connect(
#     host='127.0.0.1',
#     user='root',
#     password='password',
#     port='3306',
#     database='shestore'
# )
# myCursor = dbConnection.cursor()
# @app.route('/product/<int:product_id>')
# def show_product_details(product_id):
#     # Fetch product details from a database or data source
#     # Replace the following lines with your own code
#     product = []
#     myCursor.execute("select * from Products where ID = %s ",(product_id,) )
#     myCursor.fetchall()
#     for row in myCursor:
#         d = {}
#         name = row[2]
#         d['name'] = name
#         d['description'] = "TestingProduct"
#         d['Price'] = row[4]
#         product.append(d)
#     # Render a template that displays the product details
#     return render_template('product_details.html', product=product)
#
# @app.route('/listProducts')
# def listProducts():
#     render_template('product_page.html',product_id = 4)
#
# print(f"To acces the Gloable link please click {public_url}")
# app.run(port=6000)
#
#
