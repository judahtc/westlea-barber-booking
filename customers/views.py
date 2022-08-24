from pyclbr import Class
from django.shortcuts import render
from rest_framework import response
from django.http import HttpResponse, JsonResponse, request #1
from django.views.decorators.csrf import csrf_exempt #2
from rest_framework.parsers import DataAndFiles, JSONParser #3
from rest_framework.response import Response
from appointments import serializers
from barbers.models import Barber
from customers.models import customer
from customers.serializers import CustomerSerializer
from appointments.serializers import AppointmentsSerializer
from django.db import connection, transaction
from appointments.serializers1 import BarberSerializer1

from barbers.serializers import BarberSerializer
from appointments.models import appointments
import jwt,datetime
from rest_framework.exceptions import AuthenticationFailed



# Create your views here.
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.




class LoginView(APIView):
    
    def post(self,request):
        email =request.data['email']
        password =request.data['password']
        
        user=customer.objects.filter(email=email).first()
        
      
        if user is None:
            raise AuthenticationFailed('User not found!')

        if user.password!=password :
            raise AuthenticationFailed("incorrect password")

        

        payload = {
            'id':user.custId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt',value=token ,httponly=True)
        response.data = {
            'jwt':token
        }
        print(email)
        return response




class CustomerView(APIView):

    def get(self,request):
        token=request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("unauthorised")
        
        try:
            payload =jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("session expired")

        user=customer.objects.get(custId=payload['id'])
        
        serializer=CustomerSerializer(user)
        return Response(serializer.data)


        
    def post(self,request):
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Saved")


class OneCustomerView(APIView):
    def get_object(self,request):
            try:
                token=request.COOKIES.get('jwt')
                
                if not token:
                    raise AuthenticationFailed("unauthorised")
                
                try:
                    payload =jwt.decode(token, 'secret', algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed("session expired")

                user=customer.objects.get(custId=payload['id'])
                
                return user

            except customer.DoesNotExist:
                return Response("wakadhakwa",status=status.HTTP_204_NO_CONTENT)
     
    
    def get(self,request):
        obj=self.get_object(request)
        serializer=CustomerSerializer(obj)
        
        return Response(serializer.data)

    def put(self,request):
        
        obj=self.get_object(request)
        serializer=CustomerSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response("corrupted data",status=status.HTTP_204_NO_CONTENT)   

    def delete(self,request):
        
        all=self.get_object(request)  
        all.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)         

        #------------CUSTOMER APPOINTMENTS---------------#

class AppointmentsView(APIView):

    def get(self,request):
        token=request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("unauthorised")
        
        try:
            payload =jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("session expired")

        appointment=appointments.objects.filter(custId=payload['id'])     
        serializer=AppointmentsSerializer(appointment,many=True)
        return Response(serializer.data)

    def post(self,request):

        token=request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("unauthorised")
        
        try:
            payload =jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("session expired")

        serializer=AppointmentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Saved")
        else:
            return Response("Timeslot or Barber booked")    

class barberCheckView(APIView):

    def get(self,request,date,time):
        token=request.COOKIES.get('jwt')
        print(date,time)
        if not token:
            raise AuthenticationFailed("unauthorised")
        
        try:
            payload =jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("session expired")

        freebarber=Barber.objects.raw('Select Distinct(a."barberId"),a."username" from Barber a join appointments b on a."barberId"=b."barberId_id" where b."appointDate" =%s AND b."appointTime" =%s',[date,time])
        serializer=BarberSerializer1(freebarber,many=True)
        return Response(serializer.data)

class BarbersView(APIView):
    def get(self,request):
        barbers=Barber.objects.all()
        serializer=BarberSerializer(barbers,many=True)
        return Response(serializer.data)