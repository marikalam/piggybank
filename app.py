from flask import Flask, render_template, request, session, redirect, url_for
from config import PUBLIC_KEY, PRIVATE_KEY
import simplify
import json
import pygal



app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/")
def home():
    return render_template("home.html",key=PUBLIC_KEY)

@app.route('/something.svg')
def graph_something():
    bar_chart = pygal.Line()
    bar_chart.x_labels = '8/27', '8/28', '8/29', '8/30', '8/31', '9/1' #day, week, month
    #bar_chart.y_labels #dollars (today: start with US bank balance)
    bar_chart.add('Balance', [0, 8999, 7111, 40000, 50000, 25000]) #invoice payment+balance
    return bar_chart.render_response()


@app.route("/paymentsuccess")
def paymentSuccess():
    amount = session["amount"]/100
    return render_template("payment.html",amount=amount,id=session["id"])

@app.route("/makePayment",methods=["POST"])
def payment():
    token =  request.form["simplifyToken"]

    simplify.public_key = PUBLIC_KEY
    simplify.private_key = PRIVATE_KEY
    payment = simplify.Payment.create({
        "token" : token,
        "amount" : "1000",
        "description" : "Example on How to use",
        "currency" : "USD"
    })

    session["status"] = payment.paymentStatus
    session["id"] = payment.authCode
    session["amount"] = payment.amount

    if payment.paymentStatus == 'APPROVED':
        return redirect(url_for("paymentSuccess"))
    else:
        return "Payment not approved"

if __name__=="__main__":
    app.run("0.0.0.0",5000)
