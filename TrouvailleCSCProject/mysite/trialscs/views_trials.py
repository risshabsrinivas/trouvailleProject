from django.shortcuts import render
import mysql.connector as m
import sqlite3,yagmail
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime, os
import requests
import random
mainList=[]
booking_id,fav=0,0
departure,arrival,data=None,None,None
dict3,dict2={},{}
d3={}

entuser, entpass,='',''
email_msg1='''We've received your request for a single-use code to register with Trouvaille Inc.

Your single-use code is: '''
email_msg2='''
If you didn't request this code, you can safely ignore this email. Someone else might have typed your email address by mistake.

Thanks,
The Trouvaille Account Team.
'''
conn=sqlite3.connect('userdetails.sqlite3',check_same_thread=False)
cur=conn.cursor()
conn1=m.connect(host='localhost',user='root',password='chinju97',database='flightstorage')
cur1=conn1.cursor()
def regTableMySql():
    cur1.execute('''
    CREATE TABLE if not exists userdetails
    (snNo INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
     UserMailID VARCHAR(30),
     Username VARCHAR(100),
     Password VARCHAR(120)
    ''')
def createTableforRegistration():
    cur.executescript('''
    CREATE TABLE userdetails
    (snNo INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
     UserMailID TEXT,
     Username TEXT,
     Password TEXT)
    ''')
def createTableForFlights():
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS flightdetails
    (snNo INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
     UserMailID TEXT,
     Username TEXT,
     tickID TEXT,
     destin CHAR(3),
     dateOfTravel TEXT,
     arr CHAR(3),
     dateOfBooking TEXT,
     currency CHAR(3),
     fare TEXT)
    ''')
# cur.execute('''INSERT INTO flightdetails () VALUES ()''',())
#createTableforRegistration()
createTableForFlights()
def home(request):
    return render(request,'trialscs/Homepage.html')
def signup(request):
    return render(request,'trialscs/Sign-up.html')
def twu(request):
    return render(request,'trialscs/Travel-with-us.html')
def verification(request):
    if request.method == 'POST':
        global mailID,name,password,OTP
        mailID=request.POST['mail']
        name=request.POST['name']
        password=request.POST['password']
        OTP=random.randint(100000,999999)
        yag = yagmail.SMTP('trouvaille.cscproject@gmail.com','urrjdcmqpuynrpmo')
        yag.send(mailID, subject='Verification Code', contents=email_msg1 + str(OTP) + email_msg2)
        reqDict={'mail':mailID}
        return render(request,'trialscs/verification.html',reqDict)
def auth(request):
    if request.method == 'POST':
        givenOTP=request.POST['OTP']
        '''sqlstr=('SELECT * from userdetails')
        mainLst=[]
        for row in sqlstr:
            subLst=[row[1],row[2],row[3]]
            mainLst.append(subLst)'''
        if str(givenOTP)==str(OTP):
            cur.execute('''INSERT INTO userdetails (UserMailID,Username,Password) values(?,?,?)''',(mailID,name,password))
            conn.commit()
            cur1.execute('''INSERT INTO userdetails (UserMailID,Username,Password) values('{}','{}','{}')'''.format(mailID, name, password))
            conn1.commit()
            return render(request,'trialscs/auth_true.html')
        else:
            return render(request,'trialscs/auth_false.html')
#
def repa(request):
    return render(request,'trialscs/repa.html')
def login(request):
    return render(request,'trialscs/Login.html')
def ourteam(request):
    return render(request,'trialscs/Ourteam.html')
def userdashboard(request):
    if request.method == 'POST':
        global entuser, entpass
        entuser=request.POST['user']
        entpass=request.POST['pass']
        dictre={'user':entuser[:-10]}
        sqlstr = ('SELECT * from userdetails')
        userpassdit={}
        for row in cur.execute(sqlstr):
            a=str(row[1])
            userpassdit[a]=str(row[3])

        for i in userpassdit:
            if entuser==str(i) and entpass==userpassdit[i]:
                return render(request,'trialscs/userdashboard.html',dictre)
        else:
            return render(request,'trialscs/Login.html')
def flights1(request):
    return render(request,'trialscs/flightsbooking.html')
def flightsresults(request):
    if request.method == 'POST':
        global convert_currency, cabinclass
        global departure,arrival
        departure=request.POST['from']
        arrival=request.POST['to']
        dateoftravel=request.POST['date']
        fis4=str(dateoftravel)[0:4]
        las2=str(dateoftravel)[8:]
        mid=str(dateoftravel)[4:8]
        dateoftravel2=str(las2+mid+fis4)
        cabinclass=request.POST['class']
        nop=request.POST['nop']

        convert_currency=request.POST['cars']
        url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures"
        querystring = {"departure_date": dateoftravel, "sid": "iSiX639", 'number_of_itineraries': 1000, "adults": int(nop),
                       "destination_airport_code": str(arrival).upper(), "origin_airport_code": str(departure).upper(),
                       'convert_currency': str(convert_currency), 'cabin_class': str(cabinclass).lower()}
        headers = {
            'x-rapidapi-host': "priceline-com-provider.p.rapidapi.com",
            'x-rapidapi-key': "b5e745bc4bmsh64d83593ab94886p117e88jsn9e769946e56d"
        }
        global data
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        global destinCity,destinAirport,destinCountry,destinCode, originCity, originAirport,originCountry,originCode
        destinCity = data['getAirFlightDepartures']['results']['result']['search_data']['search_0']['destination']['city']
        destinAirport=data['getAirFlightDepartures']['results']['result']['search_data']['search_0']['destination']['name']
        destinCountry= data['getAirFlightDepartures']['results']['result']['search_data']['search_0']['destination']['country']
        destinCode=data['getAirFlightDepartures']['results']['result']['search_data']['search_0']['destination']['code']

        originCity = data['getAirFlightDepartures']['results']['result']['search_data']['search_0']['origin']['city']
        originAirport = data['getAirFlightDepartures']['results']['result']['search_data']['search_0']['origin']['name']
        originCountry = data['getAirFlightDepartures']['results']['result']['search_data']['search_0']['origin']['country']
        originCode = data['getAirFlightDepartures']['results']['result']['search_data']['search_0']['origin']['code']
        global mainList
        mainList=[]
        id=0
        totalFlights=len(data['getAirFlightDepartures']['results']['result']['itinerary_data'])
        for i in data['getAirFlightDepartures']['results']['result']['itinerary_data']:
            symbol = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['price_details']['display_symbol']
            airname =data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['airline']['name']
            timeOfDept = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['departure']['datetime']['time_12h']
            timeOfArr = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['arrival']['datetime']['time_12h']
            Tdur = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['info']['duration']
            dateOfDept = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['departure']['datetime']['date']
            dateOfArr = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['arrival']['datetime']['date']
            fare=data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['price_details']['display_total_fare']
            conf=data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['info']['connection_count']
            aircraft=data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']["flight_data"]["flight_0"]["info"]["aircraft"]
            mid1=''
            if data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['info']['connection_count'] ==1:
                for j in data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['flight_data']:
                    POD = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['flight_data'][j]['departure']['airport']['code']
                    POA = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['flight_data'][j]['arrival']['airport']['code']
                    mid1=POA+str(',')
                    break
            elif data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['info']['connection_count'] ==2:
               POD = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['flight_data']['flight_0']['arrival']['airport']['code']
               POA = data['getAirFlightDepartures']['results']['result']['itinerary_data'][i]['slice_data']['slice_0']['flight_data']['flight_1']['arrival']['airport']['code']
               mid1=POD+str(', ')+POA+str(',')

            dict1 = {'symbol': symbol, 'airname': airname, 'timeofDept': timeOfDept, 'timeofar': timeOfArr,'Tdur': Tdur, 'dateoDept': dateOfDept, 'dateofarr': dateOfArr, 'fare': fare, 'conf': conf,'aircraft': aircraft, 'id': id,'mid':mid1[:-1]}
            mainList.append(dict1)
            print(dict1)


            id+=1
            if id==10:
                break
        global d3
        d3={'dep':departure,'ar':arrival,'date':str(dateoftravel2),'cc':cabinclass,'nop':nop,'placeofdep':originCity,'placeofar':destinCity,'lst':mainList}
        redict={'dep':departure,'ar':arrival,'date':str(dateoftravel2),'cc':cabinclass,'nop':nop,'placeofdep':originCity,'placeofar':destinCity,'lst':mainList,'tf':totalFlights}
        return render(request,'trialscs/flightssecondpage.html',redict)

def flightchoice(request):
    if request.method == 'POST':
        global fav
        fav=request.POST['hello']
        global dict2
        dict2=mainList[int(fav)]
        global dict3
        dict3=mainList[int(fav)]
        co=dict2['conf']
        if co==int(0):
            d1={'dep':departure,'ar':arrival}
            dict2.update(d1)
            return render(request ,'trialscs/ftpc0.html',dict2)
        elif co==int(1):
            lst1,lst2,lst3,lst4=[],[],[],[]
            for j in data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_'+str(int(fav))]['slice_data']['slice_0']['flight_data']:
                POD = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_'+str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['departure']['airport']['code']
                POA = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_'+str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['arrival']['airport']['code']
                t1 = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_'+str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['departure']['datetime']['time_12h']
                t2 = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_'+str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['arrival']['datetime']['time_12h']
                dur = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_'+str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['info']['duration']
                T1 = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['departure']['datetime']['date']
                T2 = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['arrival']['datetime']['date']
                lst1.append(POD)
                lst1.append(POA)
                lst2.append(t1)
                lst2.append(t2)
                lst3.append(dur)
                lst4.append(T1)
                lst4.append(T2)
            d2={'dep':lst1[0],'mid':lst1[1],'arr':lst1[3],'t1':lst2[0],'t2':lst2[1],'t3':lst2[2],'t4':lst2[3],'dur1':lst3[0],'dur2':lst3[1],'T1':lst4[0],'T2':lst4[1],'T3':lst4[2],'T4':lst4[3]}
            dict2.update(d2)
            return render(request ,'trialscs/ftpc1.html',dict2)
        elif co==int(2):
            lst1, lst2, lst3, lst4 = [], [], [], []
            for j in data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data']:
                POD = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['departure']['airport']['code']
                POA = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['arrival']['airport']['code']
                t1 = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['departure']['datetime']['time_12h']
                t2 = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['arrival']['datetime']['time_12h']
                dur = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['info']['duration']
                T1 = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['departure']['datetime']['date']
                T2 = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data'][j]['arrival']['datetime']['date']
                lst1.append(POD)
                lst1.append(POA)
                lst2.append(t1)
                lst2.append(t2)
                lst3.append(dur)
                lst4.append(T1)
                lst4.append(T2)
            d2 = {'dep': lst1[0], 'mid1': lst1[1], 'mid2': lst1[3],'arr':lst1[5], 't1': lst2[0], 't2': lst2[1], 't3': lst2[2],'t5':lst2[4],'t6':lst2[5],
                  't4': lst2[3], 'dur1': lst3[0], 'dur2': lst3[1],'dur3':lst3[2], 'T1': lst4[0], 'T2': lst4[1], 'T3': lst4[2],
                  'T4': lst4[3],'T5':lst4[4],'T6':lst4[5]}
            dict2.update(d2)
            return render(request ,'trialscs/ftps2.html',dict2)
def flightspayment(request):
    if request.method == 'POST':
        name=request.POST['name']
        givmail=request.POST['name-1']
        dob=request.POST['text']
        nationality=request.POST['text-1']
        contactnum=request.POST['text-2']
        passnum=request.POST['text-4']
        d3.update(dict3)
        return render(request,'trialscs/fpp.html',d3)
def flightscon(request):
    if request.method == 'POST':
        cardname=request.POST['name']
        cardno=request.POST['number']
        cvv=request.POST['cvv']
        global booking_id
        booking_id = random.randint(1000000, 9999999)
        bookingrefnum = str(booking_id) + entuser[:4]
        d4 = {'bookingrefnum': bookingrefnum}
        date=datetime.datetime.now()
        def fileDel(x):
            # Deletes the passed file.
            if os.path.exists(x):
                os.remove(x)
                print('Deleted')
            else:
                print("The file does not exist")

        # Open an Image


        txt_1 = 'BLR'
        # Call draw Method to add 2D graphics in an image


        # Add Text to an image

        # Display edited image
        #img.show()

        # Save the edited image

        '''
        0 stops -
            Name - 231,214
            Date - 253, 276
            Booking ref - 351, 340
            Flight - 81, 867
            Departure Time -843,643
            Seat Class - 78,966
            Place of Departure -622, 870
            Arrival Time - 348,999
            Place of Arrival - 618,1002
            Total Fare - 374, 1255

                '''

        '''
            1 stop -
                    Name - 231,214
                    Date - 253, 276
                    Booking ref - 351, 340
                    Flight1 - 81, 867
                    Departure Time1 -843,643
                    Seat Class1 - 78,966
                    Place of Departure1 -622, 870
                    Arrival Time1 - 348,999
                    Place of Arrival1 - 618,1002
                    
                    Via - 142, 1137
                    Flight2 - 81,1328
                    Dept time - 350,1320
                    Dept place - 621, 1330
                    Seat class -  93,1433
                    Arrival Time 2 - 352,1462
                    Place of Arrival - 621,1460



            2 stops -
            
                
                        '''
        if dict2['conf']==0:
            fno=data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data']['flight_0']['info']["flight_number"]
            img1 = Image.open('trialscs/ticketpages/0stopspage1.png')
            img2 = Image.open('trialscs/ticketpages/0stopspage2.png')
            I1 = ImageDraw.Draw(img1)
            Tdur = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['info']['duration']
            title_font = ImageFont.truetype('trialscs/Fonts/Antonio/antonio.ttf', 40)
            title_font1 = ImageFont.truetype('trialscs/Fonts/Antonio/antonio.ttf', 30)
            title_font2 = ImageFont.truetype('trialscs/Fonts/Antonio/antonio.ttf', 20)
            #dict1 = {'symbol': symbol, 'airname': airname, 'timeofDept': timeOfDept, 'timeofar': timeOfArr,'Tdur': Tdur, 'dateoDept': dateOfDept, 'dateofarr': dateOfArr, 'fare': fare, 'conf': conf,'aircraft': aircraft, 'id': id,'mid':mid1[:-1]}
            I1.text((231,184), entuser, (0, 0, 0), font=title_font1)
            I1.text((253, 248), str(date)[:-6], (0, 0, 0), font=title_font1)
            I1.text((351, 310), bookingrefnum, (0, 0, 0), font=title_font1)
            I1.text((81, 867), dict2['airname']+' '+str(fno), (0, 0, 0), font=title_font1)
            I1.text((360,867), str(dict2['dateoDept'])+' '+dict2['timeofDept'], (0, 0, 0), font=title_font1)
            I1.text((78,966), 'A23', (0, 0, 0), font=title_font)
            I1.text((622, 870), dict2['dep'], (0, 0, 0), font=title_font)
            I1.text((348,999), str(dict2['dateofarr'])+' '+dict2['timeofar'], (0, 0, 0), font=title_font1)
            I1.text((618,1002), dict2['ar'], (0, 0, 0), font=title_font)
            I1.text((365, 1225), str(dict2['symbol'])+' '+str(dict2['fare']), (0, 0, 0), font=title_font)
            #img1.show()
            img1.save("s1.png")


            image_1 = Image.open('s1.png')
            im_1 = image_1.convert('RGB')
            im_2 = img2.convert('RGB')
#

            image_list = [im_2]
            cur1.execute('''INSERT INTO FlightDataStorage(BookingRefNumber,UserMailID,UserName,DateofSearch,PassengerCount,DepartureLOC,DateOfDeparture,ArrivalLOC,DateOfArrival,CabinClass,Airline,TotalFare,Duration,Currency,ConnectingFlights,StatusR,TimeOfDept,TimeOfArr) 
                                                        Values('{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}',{},'{}','{}',{},'{}','{}','{}')'''.format(
                bookingrefnum,entuser,entuser[:-10], date,1,dict2['dep'], str(dict2['dateoDept']),dict2['ar'],str(dict2['dateofarr']),cabinclass,dict2['airname']+' '+str(fno),dict2['fare'], str(Tdur), convert_currency,0, 'Success', str(dict2['timeofDept']), str(dict2['timeofar'])))
            conn1.commit()
            o=str(originCode)+' , '+str(originAirport)+' , '+str(originCity)+' , '+str(originCountry)
            d=str(destinCode)+' , '+str(destinAirport)+' , '+str(destinCity)+' , '+str(destinCountry)
            emc1='Thank you, {}, for booking with Trouvaille!\n\n\n'.format(entuser[:-10])
            emc2='''Your booking summary: \n\n Departure from:{}\n Arrival at: {}'''.format(' '+o,' '+d)
            emc3=' \nDate of Departure: {}\n Estimated time of Departure: {}\n Date of Arrival: {}\n Estimated time of Arrival {}\nNumber of persons travelling: 1 \n Total Fare: {} \nConnecting Flights: 0\n\n'.format(str(dict2['dateoDept']),dict2['timeofDept'],str(dict2['dateofarr']),dict2['timeofar'],str(convert_currency)+' '+str(dict2['fare']))
            emc4='Your Journey:\n\n {} ---> {} \n Airline: {} \n Cabin Class: {}\n Estimated departure from {}: {}\n Estimated arrival at {}: {}\nDuration of Flight:{} \n\n\nKindly find attatched the e-ticket.\nWishing you a safe journey!\nWith regards,\nTrouvaille Inc.'.format(str(originCode),str(destinCode),dict2['airname']+' '+str(fno), cabinclass,str(originCode),dict2['timeofDept'],str(destinCode),dict2['timeofar'],Tdur)
            emailContent = emc1 + emc2 + emc3 +emc4
            im_1.save('trialscs/ticketpages/'+str(bookingrefnum)+'_eticket.pdf', save_all=True, append_images=image_list)
            yag = yagmail.SMTP('trouvaille.cscproject@gmail.com','urrjdcmqpuynrpmo')
            print(entuser)
            yag.send(to=entuser,subject='Booking Confirmation for '+str(dict2['dep'])+' --> '+str(dict2['ar']),
                     contents=emailContent,
                     attachments=['trialscs/ticketpages/'+str(bookingrefnum)+'_eticket.pdf']
                     )

            fileDel('s1.png')
            fileDel('trialscs/ticketpages/'+str(bookingrefnum)+'_eticket.pdf')

        elif dict2['conf'] == 1:
            fno = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['flight_data']['flight_0']['info']["flight_number"]
            Tdur = data['getAirFlightDepartures']['results']['result']['itinerary_data']['itinerary_' + str(int(fav))]['slice_data']['slice_0']['info']['duration']
            img1 = Image.open('trialscs/ticketpages/1stoppage1.png')
            img2 = Image.open('trialscs/ticketpages/1stoppage2.png')
            img3 = Image.open('trialscs/ticketpages/1stoppage3.png')
            I1 = ImageDraw.Draw(img1)
            I2 = ImageDraw.Draw(img2)
            title_font = ImageFont.truetype('trialscs/Fonts/Antonio/antonio.ttf', 40)
            title_font1 = ImageFont.truetype('trialscs/Fonts/Antonio/antonio.ttf', 30)
            title_font2 = ImageFont.truetype('trialscs/Fonts/Antonio/antonio.ttf', 20)
            # dict1 = {'symbol': symbol, 'airname': airname, 'timeofDept': timeOfDept, 'timeofar': timeOfArr,'Tdur': Tdur, 'dateoDept': dateOfDept, 'dateofarr': dateOfArr, 'fare': fare, 'conf': conf,'aircraft': aircraft, 'id': id,'mid':mid1[:-1]}
            I1.text((231, 184), entuser, (0, 0, 0), font=title_font1)
            I1.text((253, 248), str(date)[:-6], (0, 0, 0), font=title_font1)
            I1.text((351, 310), bookingrefnum, (0, 0, 0), font=title_font1)
            I1.text((81, 867), dict2['airname'] + ' ' + str(fno), (0, 0, 0), font=title_font1)
            I1.text((360, 867), str(dict2['T1'])+' '+str(dict2['t1']), (0, 0, 0), font=title_font1)
            I1.text((78, 966), 'A23', (0, 0, 0), font=title_font)
            I1.text((622, 870), dict2['dep'], (0, 0, 0), font=title_font)
            I1.text((348, 999), str(dict2['T2'])+' '+str(dict2['t2']), (0, 0, 0), font=title_font1)
            I1.text((618, 1002), dict2['mid'], (0, 0, 0), font=title_font)
            I1.text((142, 1117), dict2['mid'], (0, 0, 0), font=title_font)
            I1.text((350,1320), str(dict2['T3'])+' '+str(dict2['t3']), (0, 0, 0), font=title_font1)
            I1.text((93,1433), 'D41', (0, 0, 0), font=title_font)
            I1.text((352,1462), str(dict2['T4'])+' '+str(dict2['t4']), (0, 0, 0), font=title_font1)
            I1.text((621,1460), dict2['arr'], (0, 0, 0), font=title_font)
            I2.text((300,285), str(dict2['symbol'])+' '+str(dict2['fare']), (0, 0, 0), font=title_font)
            I1.text((81,1328), dict2['airname'] + ' ' + str(int(fno)+24), (0, 0, 0), font=title_font1)
            I1.text((621, 1330), dict2['mid'], (0, 0, 0), font=title_font)

            '''Via - 142, 1137
                    Flight2 - 81,1328
                    Dept time - 350,1320
                    Dept place - 621, 1330
                    Seat class -  93,1433
                    Arrival Time 2 - 352,1462
                    Place of Arrival - 621,1460
                    '''
            #d2={'dep':lst1[0],'mid':lst1[1],'arr':lst1[3],'t1':lst2[0],'t2':lst2[1],'t3':lst2[2],'t4':lst2[3],'dur1':lst3[0],'dur2':lst3[1],'T1':lst4[0],'T2':lst4[1],'T3':lst4[2],'T4':lst4[3]}
            #img1.show()
            #img2.show()
            img1.save("s1.png")
            img2.save('s2.png')
            image_1 = Image.open('s1.png')
            im_1 = image_1.convert('RGB')
            im_2 = img2.convert('RGB')
            im_3 = img3.convert('RGB')
            cur1.execute('''INSERT INTO FlightDataStorage(BookingRefNumber,UserMailID,UserName,DateofSearch,PassengerCount,DepartureLOC,DateOfDeparture,ArrivalLOC,DateOfArrival,CabinClass,Airline,TotalFare,Duration,Currency,ConnectingFlights,StatusR,TimeOfDept,TimeOfArr) 
                                                                    Values('{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}',{},'{}','{}',{},'{}','{}','{}')'''.format(
                bookingrefnum, entuser, entuser[:-10], date, 1, dict2['dep'], str(dict2['dateoDept']), dict2['arr'],
                str(dict2['dateofarr']), cabinclass, dict2['airname'] + ' ' + str(fno), dict2['fare'], str(Tdur),
                convert_currency, 1, 'Success', str(dict2['timeofDept']), str(dict2['timeofar'])))
            conn1.commit()
            image_list = [im_2,im_3]
            o = str(originCode) + ' , ' + str(originAirport) + ' , ' + str(originCity) + ' , ' + str(originCountry)
            d = str(destinCode) + ' , ' + str(destinAirport) + ' , ' + str(destinCity) + ' , ' + str(destinCountry)
            emc1 = 'Thank you, {}, for booking with Trouvaille!\n\n\n'.format(entuser[:-10])
            emc2 = '''Your booking summary: \n\n Departure from:{}\n Arrival at: {}'''.format(' ' + o, ' ' + d)
            emc3 = ' \nDate of Departure: {}\n Estimated time of Departure: {}\n Date of Arrival: {}\n Estimated time of Arrival {}\nDuration of flight: {}\nNumber of persons travelling: 1 \n Total Fare: {} \nConnecting Flights: 1 Cabin Class: {}\n\n'.format(str(dict2['T1']), str(dict2['t1']), str(dict2['T4']), str(dict2['t4']),str(Tdur),str(convert_currency) + ' ' + str(dict2['fare']),cabinclass)
            emc4='\n\nYour Journey:\n\n'
            emc5='{} --> {}\nEstimated time of departure from {}: {}\nEstimated time of arrival at {}: {}'.format(str(originCode),str(dict2['mid']),str(originCode),str(dict2['t1']),str(dict2['mid']),str(dict2['t2']))
            emc6='\n\n{} --> {}\nEstimated time of departure from {}: {}\nEstimated time of arrival at {}: {}'.format(str(dict2['mid']),str(destinCode),str(dict2['mid']),str(dict2['t3']),str(destinCode),str(dict2['t4']))
            emc7='\n\n\nKindly find attatched the e-ticket.\nWishing you a safe journey!\nWith regards,\nTrouvaille Inc.'
            emailContent=emc1+emc2+emc3+emc4+emc5+emc6+emc7
            im_1.save('trialscs/ticketpages/' + str(bookingrefnum) + '_eticket.pdf', save_all=True,
                      append_images=image_list)
            yag = yagmail.SMTP('trouvaille.cscproject@gmail.com','urrjdcmqpuynrpmo')
            yag.send(to=entuser, subject='Booking Confirmation for ' + str(dict2['dep']) + ' --> ' + str(dict2['arr']),
                     contents=emailContent,
                     attachments=['trialscs/ticketpages/' + str(bookingrefnum) + '_eticket.pdf']
                     )

            fileDel('s1.png')
            fileDel('s2.png')
            fileDel('trialscs/ticketpages/' + str(bookingrefnum) + '_eticket.pdf')

        return render(request, 'trialscs/flightslast.html', d4)




