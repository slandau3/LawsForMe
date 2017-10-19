from flask import Flask, session, render_template, request
app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def hello_word():
    return render_template('home.html', user="steven")



if __name__ == '__main__':
    app.run(debug=True)
