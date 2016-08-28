from flask import Flask, render_template, request, session, redirect, url_for
from config import PUBLIC_KEY, PRIVATE_KEY
import simplify
from datetime import datetime, time
import time
import datetime
import json


import pygal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
import requests as r



app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'



# @app.route('/')
# def graphSomething():
#     minWorkingCapital = go.Scatter( #regular blue
#         x=['8/15', '8/16', '8/17','8/18','8/19','8/20','8/21','8/22', '8/23', '8/24',
#         '8/25','8/26','8/27','8/28','8/29','8/30', '9/1','9/2', '9/3', '9/4', '9/5', 
#         '9/6', '9/7', '9/8', '9/9', '9/10', '9/11', '9/12','9/13','9/14','9/15','9/16','9/17',
#         '9/18','9/19','9/20','9/21','9/22', '9/23', '9/24',
#         '9/25','9/26','9/27','9/28','9/29'],

#         y=['$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000','$2,000',],        
#         marker=dict(color='rgba(169,169,169, 1)'),
#         name='Minimum Working Capital',

#         line = dict(
#         color = ('rgba(169,169,169, 1)'),
#         width = 4,
#         dash = 'dash')

#     )

#     cashOnHand = go.Scatter( #regular blue
#         x=['8/15', '8/16', '8/17','8/18','8/19','8/20','8/21','8/22', '8/23', '8/24',
#         '8/25','8/26','8/27','8/28','8/29','8/30', '9/1','9/2', '9/3', '9/4', '9/5', 
#         '9/6', '9/7', '9/8', '9/9', '9/10', '9/11', '9/12','9/13','9/14','9/15','9/16','9/17',
#         '9/18','9/19','9/20','9/21','9/22', '9/23', '9/24',
#         '9/25','9/26','9/27','9/28','9/29'],

#         y=['$2,000', '$3,000', '$2,500', '$7,500', '$4,500', '$5,250', '$5,800', '$5,470', '$6,220', '$6,720', '$5,720', '$6,040', '$6,990', '$7,290', '$6,865', '$3,865', '$4,365', '$4,615', '$8,615', '$7,965', '$7,265', '$7,065', '$3,065', '$1,065', '$1,565', '$4,065', '$4,515', '$8,015', '$2,015', '$1,615', '$1,265', '$1,065', '$915', '$615', '$1,115', '$5,115', '$5,565', '$2,565', '$3,115', '$3,415', '$5,415', '$6,915', '$6,415', '$6,415', '$6,455', '$6,805'],
        
#         marker=dict(color='rgba(91,192,222,1)'),
#         name='Working Capital',
#     )


#     expense = go.Bar( #gray
#         x=['8/15', '8/16', '8/17','8/18','8/19','8/20','8/21','8/22', '8/23', '8/24',
#         '8/25','8/26','8/27','8/28','8/29','8/30', '9/1','9/2', '9/3', '9/4', '9/5', 
#         '9/6', '9/7', '9/8', '9/9', '9/10', '9/11', '9/12','9/13','9/14','9/15','9/16','9/17',
#         '9/18','9/19','9/20','9/21','9/22', '9/23', '9/24',
#         '9/25','9/26','9/27','9/28','9/29'],

#        y=['$2000', '$1000', '$500', '$3500', '$250', '$50', '$330', '750$', '$100'
#         , '$750', '$100', '$1100', '$180', '$50', '$150'],

#         marker=dict(color='rgba(217,83,79,1)'),
#         name='Expense'
#     )

#     invoice = go.Bar( # blue 
#         x=['8/15', '8/16', '8/17','8/18','8/19','8/20','8/21','8/22', '8/23', '8/24',
#         '8/25','8/26','8/27','8/28','8/29','8/30', '9/1','9/2', '9/3', '9/4', '9/5', 
#         '9/6', '9/7', '9/8', '9/9', '9/10', '9/11', '9/12','9/13','9/14','9/15','9/16','9/17',
#         '9/18','9/19','9/20','9/21','9/22', '9/23', '9/24',
#         '9/25','9/26','9/27','9/28','9/29'],

#         y=['$3000', '$500', '$5500', '$500', '$1000','$600', '$0', 
#         '$1500', '$600', '$100', '$500', '$1000', '$450'],

#         marker=dict(color='rgba(66,139,202,1)'),
#         name='Income'
#     )


#     data = [cashOnHand, minWorkingCapital, expense, invoice]

#     layout = {

#     'xaxis': {
#         'range': [0,10]
#     },
#     'yaxis': {
#         'range': [0, 8000]
#     },
#     'shapes': [
#         {
#             'type': 'rect',
#             'xref': 'x',
#             'yref': 'y',
#             'x0': '8/28',
#             'y0': 0,
#             'x1': '8/29',
#             'y1': 8000,
#             'line': {
#                 'color': 'rgb(55, 128, 191)',
#                 'width': 3,
#             },
#             'fillcolor': 'rgba(55, 128, 191, 0.6)',
#         },
#     ],
#     'title':'Working Capital',
          
#         'yaxis':dict(
#             titlefont=dict(
#                 size=16,
#                 color='rgb(107, 107, 107)'
#             ),
#             tickfont=dict(
#                 size=14,
#                 color='rgb(107, 107, 107)'
#             )
#         ),

#         'xaxis':dict(
#             titlefont=dict(
#                 size=16,
#                 color='rgb(107, 107, 107)'
#             ),
#             tickfont=dict(
#                 size=14,
#                 color='rgb(107, 107, 107)'
#             )
#         ),
#     }


#     layout = go.Layout(
#         title='Working Capital',
          
#         yaxis=dict(
#             titlefont=dict(
#                 size=16,
#                 color='rgb(107, 107, 107)'
#             ),
#             tickfont=dict(
#                 size=14,
#                 color='rgb(107, 107, 107)'
#             )
#         ),

#         xaxis=dict(
#             titlefont=dict(
#                 size=16,
#                 color='rgb(107, 107, 107)'
#             ),
#             tickfont=dict(
#                 size=14,
#                 color='rgb(107, 107, 107)'
#             )
#         ),

#     )


#     fig = go.Figure(data = data, layout=layout)
#     return py.plot(fig, filename='style-bar')




@app.route("/", methods=['GET'])
def home():
    # If you're not logged in, go back to login page
    if 'username' not in session.keys() or session['username'] == '':
        return render_template('login.html')
    else: # If you are logged in 
        if 'invoice' in session.keys():
            if session['invoice'] == '':
                return render_template('home.html', user=session['username'])
            else:
                return render_template('home.html', invoice=session['invoice'], user=session['username'])
        else:
            return render_template('home.html', user=session['username'])




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
        session['username'] = username
        return render_template('home.html', user=session['username'])
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

    return render_template("loans.html")

@app.route("/invoiceReview")
def invoice_summary():
    return render_template("invoice_review.html")


@app.route('/invoice', methods=['GET'])
def invoice_home():
    if 'username' not in session.keys() or session['username'] == '':
        return render_template('login.html')
    session['invoice'] = ''
    return render_template("invoice.html", key=PUBLIC_KEY, user=session['username'])

@app.route('/makeInvoice', methods=['POST'])
def invoice():
    memo = request.form["memo"]
    email = request.form["email"]
    amount = request.form["amount"]

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
        "name" : "Customer",
        "dateCreated" : dateCreated,
        "dueDate" : dueDate,
        "reference" : "Ref2",
        "currency" : "USD"
    }) 
 
    print invoice
    session['invoice'] = invoice.id
    return render_template("home.html", user=session['username'])


if __name__=="__main__":
    app.run("0.0.0.0",5000)
