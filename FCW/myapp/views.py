
from django.shortcuts import render
from django.http import JsonResponse 
from myapp.models import Events 
import smtplib
from email.mime.text import MIMEText

def send_meeting_reminder(date, trainer_name, event, user_name, recipient_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  
    sender_email = "" 
    sender_password = ""  # Put app password like they had taught in AE Lab, 2 fact authentication should be enabled
    
    room_name = trainer_name.replace(" ","") + user_name.replace(" ","") + date.replace(" ","")
    subject = "Meeting Reminder"
    body = f"Dear {user_name},\n\nThis is a reminder for the event '{event}' scheduled for {date}.\n\nThe room name is: {room_name}\n\nPlease make sure to attend on time."

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        print("Email reminder sent successfully!")
        server.quit()
    except Exception as e:
        print("Error occured")
        
# Create your views here.
def index(request):  
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'myapp/index.html',context)
 
def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 
 
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    send_meeting_reminder(str(start), "trainer_name", str(title), "user_name", "rishabh.vishwamithra@gmail.com")
    return JsonResponse(data)
 
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    send_meeting_reminder(str(start), "trainer_name", str(title), "user_name", "rishabh.vishwamithra@gmail.com")
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)