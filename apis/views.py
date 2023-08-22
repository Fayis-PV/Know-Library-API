import json
from .custom_storage import RemoteStorage
from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .serializers import WebsiteSerializer,CategorySerializer,MyTokenObtainPairSerializer
from .models import Website,Category
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from .permissions import IsAdminUserOrReadOnly
from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser,MultiPartParser
from django.core.serializers import serialize
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.sessions.models import Session
from django.utils import timezone
import jwt
from allauth.account.views import LogoutView,LoginView,SignupView,ConfirmEmailView
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.conf import settings
from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.views import View
from django import template
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'index.html')


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


         
class WebsitesListView(ListCreateAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request):
        print(self.request.COOKIES.values())
        queryset = Website.objects.all()
        serialized_data = serialize('json', queryset)
        data = json.loads(serialized_data)
        return Response(data)
    
    def post(self,request):
        categories = request.data.getlist('category')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            remote = RemoteStorage()
            image = remote.save_image(request=request)
            banners = remote.save_banners(request=request)
            website = serializer.save(image = image,banners=banners)
            website.add_categories(categories) 
            website = website.to_json()
            if website:
                return Response(website ,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            

class WebsitesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        serialized_data = self.serializer_class.get_data(request,pk)
        return Response(serialized_data)
    

class CategoriesListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoriesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]



class AdminPageView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        token = self.request.COOKIES.get('refresh_token')
        try:
            # Decode the JWT token's payload
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # Extract the user's unique identifier
            user_id = payload.get('user_id')
            
            # Query the user database to retrieve the user
            user = User.objects.get(id=user_id)
            
            websites = Website.objects.all().order_by('-added_on')
            categories = Category.objects.all().order_by('name')
            return Response({'User':user.username,
                             'Websites':{websites.first().name},
                             'Categories':{categories.first().name} })
        
        except jwt.ExpiredSignatureError:
            # Handle token expiration
            return None
        except jwt.DecodeError:
            # Handle invalid token
            return None
        except User.DoesNotExist:
            # Handle user not found
            return None
        

class CustomSignupView(SignupView):
    def get(self,request):
        return render(request,'account/signup.html')
    
    def form_valid(self, form):
        
        # Do your custom processing here
        # For example, you can create the user account
        
        # Redirect to the login page after signup
        return redirect('account_login') 


class CustomLoginView(LoginView):
    def get(self,request):
        return render(request,'account/login.html')
    
    def form_valid(self, form):
        # Call the parent class's form_valid to complete the login process
        response = super().form_valid(form)
        
        # Generate and set JWT token as a cookie
        user = form.user
        refresh = MyTokenObtainPairSerializer.get_token(user)
        access_token = refresh.access_token
        
        response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax')

        return response

    


class CustomLogoutView(LogoutView):
    def get(self,request):
        return render(request,'account/logout.html')
    
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)

        # Delete the 'refresh_token' and 'user_session_id' cookies
        response.delete_cookie('refresh_token')
        response.delete_cookie('user_session_id')

        return response
    

