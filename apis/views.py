from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,ListCreateAPIView,GenericAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from .permissions import IsAdminUserOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import login,logout,authenticate
from rest_framework import status
from rest_framework.parsers import FormParser,MultiPartParser
from .custom_storage import RemoteStorage
import json
from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from allauth.account.views import LoginView
# Create your views here.
def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'index.html')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        return token
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data['refresh']
            response.set_cookie('refresh_token', refresh_token, httponly=True)
        return response
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyLoginView(GenericAPIView):
    serializer_class = MyTokenObtainPairSerializer

    def get(self, request):
        if request.user.is_authenticated:
            user = self.request.user
            refresh = RefreshToken.for_user(user)  # Generate a new refresh token
            access_token = refresh.access_token
            
            # Set the refresh token as a cookie
            response = redirect('/')
            response.set_cookie('refresh_token', str(refresh), httponly=True)
            
            return response
        else:
            return redirect('/accounts/login')

         
class WebsitesListView(ListCreateAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    # parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        queryset = Website.objects.all()
        serialized_data = serialize('json', queryset)
        data = json.loads(serialized_data)
        return Response(data)
    
    def post(self,request):
        print(request.data)
        categories = request.data.getlist('category')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            remote = RemoteStorage()
            image = remote.save_image(request=request)
            banners = remote.save_banners(request=request)
            website = serializer.save(image = image,banners=banners)
            website.add_categories(categories) 
            website = website.save_data()
            if website:
                return Response(website ,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            

class WebsitesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        serialized_data = self.serializer_class.get_data(request,pk)
        print(serialized_data)
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
    permission_classes = [IsAuthenticated]
    def get(self,request):
        websites = Website.objects.all().order_by('-added_on')
        categories = Category.objects.all().order_by('name')
        return Response({'Websites':{websites},'Categories':{categories}})