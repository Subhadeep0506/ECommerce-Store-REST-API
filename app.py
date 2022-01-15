from flask import Flask
# creating an app from Flask class
app = Flask(__name__)
# letting the application know what requests it will understand
@app.route('/')
def home():
  return "Hello World!"

# run the app in specified folder
app.run(port=5000)