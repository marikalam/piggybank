from flask import Flask, render_template, request, session, redirect, url_for
from config import PUBLIC_KEY, PRIVATE_KEY
import simplify
import datetime
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/payment")
def payment_home():
    return render_template("payment_home.html",key=PUBLIC_KEY)

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

@app.route("/paymentsuccess")
def paymentSuccess():
    amount = session["amount"]/100
    return render_template("payment.html",amount=amount,id=session["id"])


@app.route('/invoice', methods=['GET'])
def invoice_home():
    return render_template("invoice.html", key=PUBLIC_KEY)

@app.route('/makeInvoice', methods=['POST'])
def invoice():
    memo = request.form["memo"]
    email = request.form["email"]
    amount = request.form["amount"]
    dueDate = datetime.date.today() + datetime.timedelta(days=int(request.form["dueDate"]))
    dateCreated = datetime.date.today()

    simplify.public_key = PUBLIC_KEY
    simplify.private_key = PRIVATE_KEY

    invoice = simplify.Invoice.create({
        "memo" : memo,
        "items" : [
           {
              "amount" : amount,
              "dateCreated": dateCreated,
              "quantity" : "1"
           }
        ],
        "email" : email,
        "dueDate" : dueDate,
        "currency" : "USD"
    })
 
print invoice

@app.route('/balance', methods=['GET'])
def balance():
    return render_template('balance.html')

if __name__=="__main__":
    app.run("0.0.0.0",5000)
