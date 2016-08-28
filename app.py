from flask import Flask, render_template, request, session, redirect, url_for
from config import PUBLIC_KEY, PRIVATE_KEY
import simplify
from datetime import datetime, time
import time
import datetime
import json
import pandas as pd
import pygal


app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/", methods=['GET'])
def home():
    # If you're not logged in, go back to login page
    if 'username' not in session.keys() or session['username'] == '':
        return render_template('login.html')
    else: # If you are logged in 
        with open('invoices.json') as data_file:    
            data = json.load(data_file)
            invoices = data['invoices']

        if 'invoice' in session.keys():
            if session['invoice'] == '':
                return render_template('home.html', user=session['username'], invoices=invoices)
            else:
                return render_template('home.html', invoice=session['invoice'], user=session['username'], invoices=invoices)
        else:
            return render_template('home.html', user=session['username'], invoices=invoices)


@app.route('/something.svg')
def graph_something():
    bar_chart = pygal.Line()
    bar_chart.x_labels = '8/27', '8/28', '8/29', '8/30', '8/31', '9/1' #day, week, month
    #bar_chart.y_labels #dollars (today: start with US bank balance)
    bar_chart.add('Balance', [0, 8999, 7111, 40000, 50000, 25000]) #invoice payment+balance
    return bar_chart.render_response()


@app.route("/login", methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']

        with open('users.json') as data_file:    
            data = json.load(data_file)
        for user in data['users']:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return render_template('home.html', user=session['username'])
        return render_template('login.html')  
    else:
        return render_template('login.html')

@app.route("/logout", methods=['GET'])
def logout():
    session['username'] = ''
    return render_template('login.html')


@app.route("/payment")
def payment_home():
    # If you're not logged in, go back to login page
    if 'username' not in session.keys() or session['username'] == '':
        return render_template('login.html')
    session['invoice'] = ''
    return render_template("payment.html",key=PUBLIC_KEY, user=session['username'])

@app.route("/makePayment",methods=["POST"])
def payment():

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

    print session['id']
    print session['amount']
    print token

    if payment.paymentStatus == 'APPROVED':
        return redirect(url_for("paymentSuccess"))
    else:
        return "Payment not approved"

@app.route("/paymentsuccess")
def paymentSuccess():
    amount = session["amount"]/100
    return render_template("payment_success.html",amount=amount,id=session["id"])

@app.route('/loans', methods=['GET'])
def loans():
    loans = []
    vendors = {}
    total = 0
    with open('invoices.json') as data_file:    
            data = json.load(data_file)
            invoices = data['invoices']
            for invoice in invoices:
                if(invoice['customer']['name'] not in vendors.keys()):
                    loans.append({
                    "Vendor": invoice['customer']['name'],
                    "AccountRecievable": invoice['amount'],
                    "Score": "Low Risk",
                    "Haircut": 20.0,
                    "Loan": invoice['amount']*10.0*0.2
                    })
                    total += invoice['amount'] * 10 * 0.2
                    vendors[invoice['customer']['name']] = True
                else: 
                    # loop through and find the vendor who needs their invoice calculated
                    for loan in loans:
                        if loan['Vendor'] == invoice['customer']['name']:
                            loan['AccountRecievable'] += invoice['amount']
                
    print loans

    return render_template("loans.html", loans=loans, total=total)


@app.route('/invoice', methods=['GET'])
def invoice_home():
    if 'username' not in session.keys() or session['username'] == '':
        return render_template('login.html')
    session['invoice'] = ''
    company = ''
    phone = ''
    address = ''
    with open('users.json') as data_file:    
            data = json.load(data_file)
            for user in data['users']:
                if user['username'] == session['username']:
                    company = user['company']
                    phone = user['phone']
                    address = user['address']
    return render_template("invoice.html", key=PUBLIC_KEY, user=session['username'], company=company, phone=phone, address=address)

@app.route('/makeInvoice', methods=['POST'])
def invoice():
    memo = request.form["memo"]
    email = request.form["email"]
    amount = request.form["amount"]
    name = request.form["name"]

    dueDate = str(int(time.time()) + (24 * 60 * 60 * int(request.form["dueDate"])))
   
    dateCreated = str(int(time.time()))

    simplify.public_key = PUBLIC_KEY
    simplify.private_key = PRIVATE_KEY

    invoice = simplify.Invoice.create({
        "memo" : memo,
        "items" : [
           {
              "amount" : amount,
              "quantity" : "1"
           }
        ],
        "email" : email,
        "name" : name,
        "dateCreated" : dateCreated,
        "dueDate" : dueDate,
        "reference" : "Ref2",
        "currency" : "USD"
    }) 
 
    print invoice

    invoice_json = {
        "customer": {
            "email": invoice['customer']['email'],
            "id": invoice['customer']['id'],
            "name": invoice['customer']['name']
        },
        "dateCreated": invoice['dateCreated'],
        "dueDate": invoice['dueDate'],
        "invoiceID": invoice['invoiceId'],
        "memo": invoice['memo'],
        "amount": invoice['items'][0]['amount'],
        "status": "Pending",
        "username": session['username']
    }


    with open('invoices.json') as data_file:    
            data = json.load(data_file)

    data['invoices'].append(invoice_json)

    with open('invoices.json', 'w') as f:
        json.dump(data, f)

    session['invoice'] = invoice.id
    return render_template("home.html", user=session['username'])


if __name__=="__main__":
    app.run("0.0.0.0",5000)
