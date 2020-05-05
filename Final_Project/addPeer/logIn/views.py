from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import datetime
import sqlite3
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json




def home(request):
    return render(request, 'logIn.html') 

def logIn(request):
    conn  = sqlite3.connect('addPeers.db')
    user = request.POST['userID']
    pawd = request.POST['password']
    cur = conn.cursor() 
    query = "SELECT Pass FROM user where Id='"+user+"'"
    cur.execute(query)    
    db_pass = cur.fetchone()

    if db_pass != None:
        db_pass = db_pass[0]
    
    conn.close()
    
    if db_pass == pawd:
        request.session['userId'] = user
        request.session['logInTime'] = str(datetime.datetime.now())

        return render(request, 'activities.html',{'data':  request.session['userId']  })
    else:
        return render(request, 'logIn.html',{'data':'Incorrect password'})
   

def message(request):
    return render(request, 'message.html') 

def backToInsert(request):
    return render(request, 'activities.html') 

def addPeer(request):
    fName = request.POST['firstName']
    lName = request.POST['lastName']
    dob = request.POST['dob']
    compName = request.POST['comName']
    conn  = sqlite3.connect('addPeers.db')
    cur = conn.cursor()    
    query = "INSERT INTO peerDetails (fName,lName,dob,compName,Userid) VALUES ('"+fName+"','"+lName+"',"+"'"+dob+"','"+compName+"','"+request.session['userId']+"')"
    cur.execute(query) 
    conn.commit()
    conn.close()
    return render(request, 'message.html',{'message':'Peer Added'}) 

def logOut(request):
    conn  = sqlite3.connect('addPeers.db')
    cur = conn.cursor()  
    query = "INSERT INTO activityDetails (userID,logInTime,logOutTime) VALUES ('"+request.session['userId']+"','"+request.session['logInTime']+"','"+str(datetime.datetime.now())+"')"
    cur.execute(query) 
    conn.commit()
    conn.close()
    return render(request, 'login.html')

   
@api_view(["POST"])
def returnActivityData(data):
    conn  = sqlite3.connect('addPeers.db')
    cur = conn.cursor() 
    query = "SELECT distinct id from user"
    cur.execute(query) 
    user= cur.fetchall()   
    timeList =""
    ust=""
    finlaList = []
    mebersListRet = "{'ok':'#ok', 'members':'#members'}"
    for arr1 in user:        
        for i in arr1:
            memList = "{'id':'#id', 'real_name':'#real_name', 'tz':'#tz', 'activity_periods':'#activity_periods'}"
            res_time_list = []
            query = "select logInTIme, logOutTime from activityDetails where userID='"+str(i)+"'"
            cur.execute(query)
            timeList = cur.fetchall() 
            query = "select name, Location from user where id='"+str(i)+"'"
            cur.execute(query)
            allVal = cur.fetchall()
            name = allVal[0][0]
            location = allVal[0][1]

            for j in timeList:
                time_json = "{'start_time':'#start_time', 'start_time':'#end_time'}"
                for idx,k in enumerate(j):
                    if idx ==0:
                        time_json = time_json.replace('#start_time',k)
                    else:
                        time_json = time_json.replace('#end_time',k)
                res_time_list.append(time_json)
            memList = memList.replace("#id", str(i)).replace("#activity_periods", str(res_time_list)).replace('#real_name', str(name)).replace('#tz',location)
        finlaList.append(memList)
    mebersListRet = mebersListRet.replace("#members",str(finlaList)).replace("#ok","True")
    res = json.loads(json.dumps(mebersListRet))

    return JsonResponse(res, safe=False)
    #return Response(res)

    



