from django.shortcuts import render
from rest_framework import response
from django.http import HttpResponse, JsonResponse, request #1
from django.views.decorators.csrf import csrf_exempt #2
from rest_framework.parsers import DataAndFiles, JSONParser #3
from rest_framework.response import Response
from barbers.models import barber
from customers.models import customer
from customers.serializers import CustomerSerializer
from appointments.models import appointments
from barbers.serializers import BarberSerializer
from appointments.serializers import AppointmentsSerializer
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
            'id':user.barberId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt',value=token ,httponly=True)
        response.data = {
            'jwt':token
        }
        return response




class AppointmentsView(APIView):

    def get(self,request):
        token=request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("unauthorised")
        
        try:
            payload =jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("session expired")

        appointment=appointments.objects.filter(barberId=payload['id'])     
        serializer=AppointmentsSerializer(appointment,many=True)
        return Response(serializer.data)


        
    def post(self,request):
        
            serializer=AppointmentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Appointment successfully saved")
            else:
                return Response("the barber is currently booked at that timeslot, kindly try a different barber or timeslot")
            
class AllAppointsView(APIView):
    def get(self,request):
        appointment=appointments.objects.all()     
        serializer=AppointmentsSerializer(appointment,many=True)
        return Response(serializer.data)

            


class OneAppointmentView(APIView):
    
    
    def get(self,request,id):
        obj=appointments.objects.get(appointmentId=id)
        serializer=AppointmentsSerializer(obj)
        
        return Response(serializer.data)

    def put(self,request,id):
        
        obj=appointments.objects.get(appointmentId=id)
        serializer=AppointmentsSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("updated")
        return Response("corrupted data",status=status.HTTP_204_NO_CONTENT)   

    def delete(self,request,id):
        try: 
            all=appointments.objects.get(appointmentId=id) 
            all.delete()
            return Response("Appointment successfully cancelled, click close to exit")         
        except: 
            return Response("Appointment already cancelled")
        