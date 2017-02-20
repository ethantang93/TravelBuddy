from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib import messages
from models import User,Trip
def index(request):
    return redirect('/main')

def main(request):
    return render(request, 'travelbuddy/main.html')

def travels(request):
    joined_trips = User.objects.get(id=request.session['user']['id']).joined_trips.all()
    my_trips = Trip.objects.filter(created_by=request.session['user']['id']) | joined_trips
    other_trips = Trip.objects.exclude(created_by=request.session['user']['id']).exclude(id__in=joined_trips.values_list("id", flat=True))
    context = {'my_trips':my_trips, 'other_trips':other_trips}
    return render(request, 'travelbuddy/travels.html',context)


def login(request):
    result = User.objects.validateLogin(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect('/main')
    return log_user_in(request, result[1])


def register(request):
    result = User.objects.validateReg(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect('/main')
    return log_user_in(request, result[1])

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.INFO, message)

def log_user_in(request, user):
    request.session['user'] = {
        'id' : user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    return redirect('/travels')

def logout(request):
    request.session.pop('user')
    return redirect('/main')

def addTrip(request):
    return render(request, 'travelbuddy/add.html')

def tripProcess(request):
    result = Trip.objects.validateTrip(request)
    if result[0] == False:
        print_messages(request, result[1])
        print ("something is wrong")
        return redirect('/travels/add')
    print ("seems fine")
    return redirect('/travels')

def tripDetail(request, id):
    trip_detail = Trip.objects.filter(id=id)
    others = Trip.objects.getUsersOnTrip(id)
    context = {'trip_detail':trip_detail, 'others':others}

    return render(request, 'travelbuddy/detail.html', context)

def tripJoin(request, trip_id, user_id):
    print trip_id
    print user_id
    trip = Trip.objects.joinTrip(trip_id,user_id)
    return redirect('/travels')
