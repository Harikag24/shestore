from flask import Flask
from flask import request
from pyngrok import ngrok

from flask.templating import render_template
app = Flask('__main__',template_folder='/Users/swarna/Downloads')
ngrok.set_auth_token("2Oev4Kw5hUjlGkNlwIAvXSxXg2o_4Cg9gA8HirQsrtLXh8WyF")
public_url =  ngrok.connect(5000).public_url

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

print(f"To acces the Gloable link please click {public_url}")
if __name__=='__main__':
    app.run(port=5000)