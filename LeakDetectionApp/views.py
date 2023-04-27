from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from LeakDetectionApp.forms import LoginForm, UserForm, WorkerForm, ScheduleForm, ComplaintForm
from LeakDetectionApp.models import Consumer, Worker, Schedule, Appointment, Complaint,Login


def welcome(request):
    return render(request, 'hello.html')


def Home(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('AdminHome')
            elif user.is_worker:
                return redirect('WorkerHome')
            elif user.is_consumer:
                return redirect('UserHome')
        else:
            messages.info(request, 'Invalid username or password')
    return render(request, 'login.html')


def Admin_Home(request):
    return render(request, 'AdminHome.html')


def User_Home(request):
    return render(request, 'UserHome.html')


def Worker_Home(request):
    return render(request, 'WorkerHome.html')


def registerUser(request):
    login_form = LoginForm()
    user_form = UserForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        user_form = UserForm(request.POST)
        if login_form.is_valid() and user_form.is_valid():
            user = login_form.save(commit=False)
            user.is_consumer = True
            user.save()
            consumer = user_form.save(commit=False)
            consumer.user = user
            consumer.save()
            messages.info(request, "registered successfully")
            return redirect('login')
    return render(request, 'UserRegister.html', {'login_form': login_form, 'user_form': user_form})


def View_consumer(request):
    consumer = Consumer.objects.all()
    return render(request, 'ViewConsumer.html', {'consumer': consumer})


def ManageAppointment(request):
    appointment = Appointment.objects.all()
    return render(request, 'ManageAppointment.html', {'appointment': appointment})

def approve_appointment(request,id):
    n = Appointment.objects.get(id=id)
    n.status = 1
    n.save()
    messages.info(request,'Appointment Confirmed')
    return redirect('ManageAppointment')

def reject_appointment(request,id):
    n = Appointment.objects.get(id=id)
    n.status = 2
    n.save()
    messages.info(request, 'Appointment Rejected')
    return redirect('ManageAppointment')

def registerWorker(request):
    login_form = LoginForm()
    user_form = WorkerForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        user_form = WorkerForm(request.POST,request.FILES)
        if login_form.is_valid() and user_form.is_valid():
            user = login_form.save(commit=False)
            user.is_worker = True
            user.save()
            worker = user_form.save(commit=False)
            worker.user = user
            worker.save()
            messages.info(request, "registered successfully")
            return redirect('AdminHome')
    return render(request, 'WorkerRegister.html', {'login_form': login_form, 'user_form': user_form})

def worker_update(request,id):
    w = Worker.objects.get(id=id)
    l = Login.objects.get(worker=w)
    if request.method == 'POST':
        form = WorkerForm(request.POST or None,instance = w)
        user_form = LoginForm(request.POST or None,instance=l)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.info(request,'workers updated Successful')
            return redirect('ManageWorker')
    else:
        form = WorkerForm(instance = w)
        user_form = LoginForm(instance = l)
    return render(request,'worker_update.html',{'form':form,'user_form':user_form})

def worker_delete(request,id):
    data1 = Worker.objects.get(id=id)
    data = Login.objects.get(worker=data1)
    if request.method == 'POST':
        data.delete()
        return redirect('ManageWorker')
    else:
        return redirect('ManageWorker')



def ManageWorker(request):
    worker = Worker.objects.all()
    return render(request, 'ManageWorker.html', {'worker': worker})


def AssignWork(request):
    consumer = Consumer.objects.all()
    return render(request, 'ManageAppointment.html', {'consumer': consumer})


def ConsumerProfile(request):
    consumer = Consumer.objects.get(user=request.user)
    return render(request, 'ConsumerProfile.html', {'consumer': consumer})

def edit_consumerprofile(request,id):
    c = Consumer.objects.get(id=id)
    l = Login.objects.get(consumer=c)
    if request.method == 'POST':
        form = UserForm(request.POST or None, instance=c)
        user_form = LoginForm(request.POST or None, instance=l)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.info(request, 'consumer updated Successful')
            return redirect('UserHome')
    else:
        form = UserForm(instance=c)
        user_form = LoginForm(instance=l)
    return render(request,'edit_consumerprofile.html',{'form':form,'user_form':user_form})


def WorkerProfile(request):
    worker = Worker.objects.get(user=request.user)
    return render(request, 'WorkerProfile.html', {'worker': worker})


# def ScheduleWork(request):
#     form = ScheduleForm()
#     if request.method == 'POST':
#         form = ScheduleForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.info(request,'Scheduled successfully')
#             return redirect('WorkerHome')
#     else:
#         form = ScheduleForm()
#     return render(request,'Schedule.html',{'form':form})
def ScheduleWork(request):
    form = ScheduleForm()
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.worker = Worker.objects.get(user=request.user)
            form.save()
            messages.info(request, 'Schedule added Successful')
            return redirect('view_schedule')
    return render(request, 'Schedule.html', {'form': form})

def view_schedule(request):
    u= Worker.objects.get(user=request.user)
    s= Schedule.objects.filter(worker=u)
    return render(request,'view_schedule.html',{'s':s})

def edit_schedule(request,id):
    s = Schedule.objects.get(id=id)
    if request.method == 'POST':
        form = ScheduleForm(request.POST or None,instance=s)
        if form.is_valid():
            form.save()
            messages.info(request,'schdeule updated')
            return redirect('view_schedule')
    else:
        form = ScheduleForm(instance=s)
    return render(request,'edit_schedule.html',{'form':form})

def remove_schedule(request,id):
    s = Schedule.objects.filter(id=id)
    if request.method == 'POST':
        s.delete()
        return redirect('view_schedule')
    else:
        return redirect('view_schedule')

def ViewSchedule(request):
    u = Worker.objects.get(user=request.user)
    s = Schedule.objects.filter(worker=u)
    context = {
        'schedule': s
    }
    return render(request, 'ViewSchedule.html', context)


def ViewScheduleUser(request):
    schedule = Schedule.objects.all()
    return render(request, 'ViewScheduleUser.html', {'schedule': schedule})

def appointments_consumer(request):
    u = Consumer.objects.get(user=request.user)
    a = Appointment.objects.filter(user=u)
    return render(request,'appointments_consumer.html',{'a':a})


def AdminAppointmentView(request):
    a = Appointment.objects.all()
    context = {
        'Appointment': a,
    }
    return render(request, 'ManageAppointment.html', context)


def take_appointment(request, id):
    s = Schedule.objects.get(id=id)
    c = Consumer.objects.get(user=request.user)
    appointment = Appointment.objects.filter(user=c, schedule=s)
    if appointment.exists():
        messages.info(request, 'You Have Already Requested Appointment for this Schedule')
        return redirect('ViewScheduleUser')
    else:
        if request.method == 'POST':
            obj = Appointment()
            obj.user = c
            obj.schedule = s
            obj.save()
            messages.info(request, 'Appointment Booked Successfully')
            return redirect('appointment_view')
    return render(request, 'take_appointment.html', {'schedule': s})


def appointment_view(request):
    c = Consumer.objects.get(user=request.user)
    a = Appointment.objects.filter(user=c)
    return render(request, 'appointment_view.html', {'appointment': a})


def Complaint_add_user(request):
    form = ComplaintForm()
    u = request.user
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('Complaint_view_user')
    return render(request, 'complaint_add.html', {'form': form})


def Complaint_view_user(request):
    f = Complaint.objects.filter(user=request.user)
    return render(request, 'complaint_view.html', {'feedback': f})

def Complaint_admin(request):
    f = Complaint.objects.all()
    return render(request, 'complaint_view_a.html', {'feedback': f})

def reply_Feedback(request, id):
    f = Feedback.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        f.reply = r
        f.save()
        messages.info(request, 'Reply send for complaint')
        return redirect('Feedback_admin')
    return render(request, 'reply_complaint.html', {'feedback': f})


#############iot section#############
from urllib.request import urlopen

import json
import time

READ_API_KEY = 'IIU0S59YV41Q0XP7'
CHANNEL_ID = '1771038'

def iotvalues(request):

  while True:
    TS = urlopen(
        "https://api.thingspeak.com/channels/1771038/feeds.json?api_key=IIU0S59YV41Q0XP7&results=2".format(CHANNEL_ID,
                                                                                                           READ_API_KEY))

    response = TS.read()

    data = json.loads(response.decode('utf-8'))

    print(data)

    # print (data["feeds"][1]["field1"])

    a = data["feeds"][1]["field1"]
    b = data['channel']['latitude']
    c = data['channel']['longitude']
    print(a)
    print(b)
    print(c)
    return render(request,'iot_value.html',{'a':a,'b':b,'c':c})

def schedule_admin(request):
    w = Schedule.objects.all()
    return render(request,'View_schedule_admin.html',{'w':w})

def user_view_iot(request):
    return render(request,'iot_user.html')

def worker_view_iot(request):
    return render(request,'iot_worker.html')