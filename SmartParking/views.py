
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Q
from SmartParking.models import *
import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time


# Create your views here.

def home(request):
    return render(request,'SmartParking/home.html')

model=YOLO('yolov8s.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)

def parking_lot_state(request):
    cap=cv2.VideoCapture('video_2023-06-09_12-16-22.mp4')
    my_file = open("coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")

    area1=[(270,111),(284,119),(349,103),(331,97)]
    area2=[(285,121),(301,132),(368,111),(354,106)]
    count = 0
    while True:    
        ret,frame = cap.read()
        count += 1
        if count % 15 != 0:
            continue
        if not ret:
            break
        frame=cv2.resize(frame,(1020,500))

        results=model.predict(frame)
        a=results[0].boxes.data
        px=pd.DataFrame(a).astype("float")
        list1=[]
        list2=[]

        for index,row in px.iterrows():
            x1=int(row[0])
            y1=int(row[1])
            x2=int(row[2])
            y2=int(row[3])
            d=int(row[5])
            c=class_list[d]
            if 'car' in c:
                cx=int(x1+x2)//2
                cy=int(y1+y2)//2
                results1=cv2.pointPolygonTest(np.array(area1,np.int32),((cx,cy)),False)
                if results1>=0:
                   cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
                   list1.append(c)
                   cv2.putText(frame,str(c),(x1,y1),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                results2=cv2.pointPolygonTest(np.array(area2,np.int32),((cx,cy)),False)
                if results2>=0:
                   cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
                   list2.append(c)
        a1=(len(list1))
        a2=(len(list2)) 
        o=(a1+a2)
        space=(10-o)
        if a1==1:
            cv2.putText(frame,str('1'),(265,115),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
        else:
            cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,255,0),2)
            cv2.putText(frame,str('1'),(265,115),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
        if a2==1:
            cv2.putText(frame,str('2'),(280,129),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
        else:
            cv2.polylines(frame,[np.array(area2,np.int32)],True,(0,255,0),2)
            cv2.putText(frame,str('2'),(280,129),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)

        text = 'FREE: ' + str(space) + '/10'
        cv2.putText(frame,text,(23,30),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)

        # Return the number of free spaces as a plain text response
        response = HttpResponse(str(space), content_type='text/plain')
        return response
    print(response)

    cap.release()
    cv2.destroyAllWindows()



model = YOLO('yolov8s.pt')

def detail(request):
    cap = cv2.VideoCapture('video_2023-06-09_12-16-22.mp4')
    my_file = open("coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")
    area1 = [(270, 111), (284, 119), (349, 103), (331, 97)]
    area2 = [(285, 121), (301, 132), (368, 111), (354, 106)]
    count = 0
    spaces = []
    # print(spaces)

    while True:
        ret, frame = cap.read()
        count += 1
        if count % 15 != 0:
            continue
        if not ret:
            break
        frame = cv2.resize(frame, (1020, 500))

        results = model.predict(frame)
        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")
        list1 = []
        list2 = []

        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            c = class_list[d]
            if 'car' in c:
                cx = int(x1 + x2) // 2
                cy = int(y1 + y2) // 2
                results1 = cv2.pointPolygonTest(np.array(area1, np.int32), ((cx, cy)), False)
                if results1 >= 0:
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
                    list1.append(c)
                    cv2.putText(frame, str(c), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                results2 = cv2.pointPolygonTest(np.array(area2, np.int32), ((cx, cy)), False)
                if results2 >= 0:
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
                    list2.append(c)
        a1 = len(list1)
        a2 = len(list2)
        o = (a1 + a2)
        space = (10 - o)
        spaces.append(space)
        if a1 == 1:
            cv2.putText(frame, str('1'), (265, 115), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
        else:
            cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 255, 0), 2)
            cv2.putText(frame, str('1'), (265, 115), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        if a2 == 1:
            cv2.putText(frame, str('2'), (280, 129), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
        else:
            cv2.polylines(frame, [np.array(area2, np.int32)], True, (0, 255, 0), 2)
            cv2.putText(frame, str('2'), (280, 129), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

        text = 'FREE: ' + str(space) + '/10'
        cv2.putText(frame, text, (23, 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        cv2.imshow("RGB", frame)

        if cv2.waitKey(100) & 0xFF == ord('d'):
            break

    cap.release()
    cv2.destroyAllWindows()

    context = {
        'spaces': spaces
    }
    return render(request, 'SmartParking/detail.html', context)


# def detail(request):
#     return render(request,'SmartParking/detail.html')
# def signup(request):
#     if request.method == 'POST':
#         # first_name = request.POST['first_name']
#         # last_name = request.POST['last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']

#         if password == password2:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email Already Used') 
#                 return redirect('')
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request,'Username Already taken')
#                 return redirect('')
#             else:
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 user.save()

#                 # log user in and direct to settings page later 
#                 user_login = auth.authenticate(username=username, password=password)
#                 auth.login(request,user_login)

#                 # New profile for new User 
#                 user_model = User.objects.get(username=username)
#                 # new_profile = UserProfile.objects.create(user=user_model)
#                 # new_profile.save()
#                 # return redirect('Post:settings')
#         else:
#             messages.info(request,'Password Not Matching')
#             return redirect('Users:signup')
   
#     else:
#         return render(request, 'Users/signup.html')
#     context = {}
#     return render(request,'Users/signup.html',context)
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('SmartParking:home')
        else:
            messages.info(request,'User does not exist!')
            return redirect('SmartParking:signin')
    else:
        return render(request,'SmartParking/signin.html')

# @login_required
# def signout(request):
#     logout(request)
#     return redirect('Users:signin')
