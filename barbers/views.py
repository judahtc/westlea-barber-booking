from django.shortcuts import render
from rest_framework import response
from django.http import HttpResponse, JsonResponse, request #1
from django.views.decorators.csrf import csrf_exempt #2
from rest_framework.parsers import DataAndFiles, JSONParser #3
from rest_framework.response import Response
from barbers.models import barber
from barbers.serializers import BarberSerializer
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
        
        user=barber.objects.filter(email=email).first()
        
      
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




class BarberView(APIView):

    def get(self,request):
        token=request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("unauthorised")
        
        try:
            payload =jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("session expired")

        user=barber.objects.get(barberId=payload['id'])
        
        serializer=BarberSerializer(user)
        return Response(serializer.data)


        
    def post(self,request):
        serializer=BarberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Saved")

class OneBarberView(APIView):
    def get_object(self,request):
            try:
                token=request.COOKIES.get('jwt')
                
                if not token:
                    raise AuthenticationFailed("unauthorised")
                
                try:
                    payload =jwt.decode(token, 'secret', algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed("session expired")

                user=barber.objects.get(barberId=payload['id'])
                
                return user

            except barber.DoesNotExist:
                return Response("wakadhakwa",status=status.HTTP_204_NO_CONTENT)
     
    
    def get(self,request):
        obj=self.get_object(request)
        serializer=BarberSerializer(obj)
        
        return Response(serializer.data)

    def put(self,request):
        
        obj=self.get_object(request)
        serializer=BarberSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response("corrupted data",status=status.HTTP_204_NO_CONTENT)   

    def delete(self,request):
        all=self.get_object(request)  
        all.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)         