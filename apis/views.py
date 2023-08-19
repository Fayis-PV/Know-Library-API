from django.shortcuts import render,redirect,HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,ListCreateAPIView,GenericAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from .serializers import WebsiteSerializer,CategorySerializer,MyTokenObtainPairSerializer
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
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.sessions.models import Session
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'index.html')


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SetTokenView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user

            # Create and set the JWT token
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            session_key = f'user_{user.id}'
            expire_date = timezone.now() + refresh.access_token.lifetime


            # Update or create user session
            try:
                user_session = Session.objects.get(session_key=session_key)
                user_session.expire_date = timezone.now() + refresh.access_token.lifetime

                user_session.save()
            except Session.DoesNotExist:
                user_session = Session.objects.create(session_key=session_key,expire_date=expire_date)
                user_session.save()

            # Set the refresh token as a secure HTTP-only cookie
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True)

            # Set user session ID as a cookie for tracking
            response.set_cookie('user_session_id', user_session.session_key,secure=True,httponly=True)

            return redirect('/')
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

         
class WebsitesListView(ListCreateAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request):
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
    permission_classes = [IsAuthenticated]
    def get(self,request):
        websites = Website.objects.all().order_by('-added_on')
        categories = Category.objects.all().order_by('name')
        return Response({'Websites':{websites},'Categories':{categories}})