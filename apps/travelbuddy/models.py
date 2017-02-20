from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

######################## defining the USER MANAGER#########################
class UserManager(models.Manager):
    def validateReg(self, request):
        errors = self.validate_inputs(request)

        if len(errors) > 0:
            return (False, errors)

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        user = self.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], pw_hash=pw_hash)

        return (True, user)

    def validateLogin(self, request):
        try:
            user = User.objects.get(email=request.POST['email'])
            # The email matched a record in the database, now test passwords
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()) == user.pw_hash.encode():
                return (True, user)

        except ObjectDoesNotExist:
            pass

        return (False, ["Email/password don't match."])

    def validate_inputs(self, request):
        errors = []
        if len(request.POST['first_name']) < 2 or len(request.POST['last_name']) < 2:
            errors.append("Please include a first and/or last name longer than two characters.")
        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append("Please include a valid email.")
        if len(request.POST['password']) < 8 or request.POST['password'] != request.POST['confirm_pw']:
            errors.append("Passwords must match and be at least 8 characters.")

        return errors


######################## defining the table#########################
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()
######################## defining the trip manager#########################

class TripManager(models.Manager):
    def checkErrors(self, request):
        errors=[]
        if len(request.POST['destination']) < 2:
            errors.append("Destination name must be longer than two characters")

        if len(request.POST['description']) < 2:
            errors.append("Description must be longer than two characters")
        startdate=datetime.strptime(request.POST['travel_from'], '%Y-%m-%d')
        enddate=datetime.strptime(request.POST['travel_to'], '%Y-%m-%d')
        if len(request.POST['travel_from'])<2:
            errors.append("start date missing")
        if len(request.POST['travel_to'])<2:
            errors.append("end date missing")
        if startdate < datetime.now():
            errors.append("start day must be in future")
        if startdate>enddate:
            errors.append("start date must be before end date")
        return errors
    def validateTrip(self, request):
        errors = self.checkErrors(request)
        if len(errors)>0:
            return (False, errors)
        user = User.objects.get(id=request.session['user']['id'])
        trip = self.create(travel_from = request.POST['travel_from'], travel_to = request.POST['travel_to'], description = request.POST['description'], destination = request.POST['destination'], created_by = user)
        return (True, trip)
    def joinTrip(self, trip_id, user_id):
        self.get(id=trip_id).joined_by.add(User.objects.get(id=user_id))
    def getUsersOnTrip(self, trip_id):
        trip = self.get(id = trip_id)
        return trip.joined_by.all()


######################## defining the table#########################

class Trip(models.Model):
    travel_from = models.DateField()
    travel_to = models.DateField()
    description = models.CharField(max_length=250)
    destination = models.CharField(max_length=45)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User)
    joined_by = models.ManyToManyField(User, related_name="joined_trips")

    objects = TripManager()
