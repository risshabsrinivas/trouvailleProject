from django.shortcuts import render
import sqlite3,smtplib,random,yagmail

import requests
import random
#import ssl
# Create your views here.
#from django.http import HttpResponse
email_msg1='''We've received your request for a single-use code to use with your Trouvaille Account.

Your single-use code is: '''
email_msg2='''
If you didn't request this code, you can safely ignore this email. Someone else might have typed your email address by mistake.

Thanks,
The Trouvaille Account Team.
'''

'''
def index(request):
    return HttpResponse("Hello, world. You're at the TRIALS index.")
    '''
def home(request):
    return render(request,'trialscs/Homepage.html')
def verification(request):
        global username
        username= request.POST["user"]
        password = request.POST["pass"]
        global mess
        mess=random.randint(100000,999999)
        if '@' in username and '.com' in username:
            yag = yagmail.SMTP('trouvaille.cscproject@gmail.com')
            yag.send(username, subject='Verification Code', contents=email_msg1+str(mess)+email_msg2)
            veriDict={'user':username,'password':password}

            return render(request,'trialscs/verification.html',veriDict)
        else:
            return render(request,'trialscs/error.html')
        #'trouvaille.cscproject@gmail.com','trouvaillecscpro'
def index(request):
      return render(request, 'trialscs/Login.html')

def validate(request):
    conn=sqlite3.connect('FlightDataStorage.sqlite3')
    cur=conn.cursor()
    #cur.execute('''CREATE TABLE Data (
        #snNo INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        #UserMailID TEXT,
        #password TEXT)''')
    if request.method == 'POST':
        otp=request.POST["otp"]
        if int(otp)==mess:
            dict = {
             'username': username
             }

            #for row in cur.execute(sqlstr):
            #    lst.append(str(row[0]))
           # if (str(username) not in lst):
            #    cur.execute('''INSERT INTO Data(UserMailID,password) VALUES(?,?)''',(username,password))
          #      conn.commit()'''
            return render(request, 'trialscs/validate.html', dict)
        else:
            dict={'otp':otp}
            return render(request,'trialscs/error.html',dict)
def results(request):
    if request.method=='POST':
        froms=request.POST["from"]
        to=request.POST["to"]
        dict1={
            'froms':froms,
            'to':to}
        return render(request, 'trialscs/results.html', dict1)


def travel_information(request):
    return render(request,'trialscs/travel_information.html')