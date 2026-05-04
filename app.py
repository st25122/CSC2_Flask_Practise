from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)
app.secret_key = '6305'  # Change this to a random secret key


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/invoice")
def invoice():
    return render_template("Invoice.html")


if __name__ == '__main__':
    app.run(debug=True)
