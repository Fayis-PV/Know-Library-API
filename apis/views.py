from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,ListCreateAPIView,GenericAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from .serializers import *
from .models import *
from rest_framework.permissions import IsAdminUser,AllowAny
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
from rest_framework.authtoken.models import Token

# Create your views here.
def index(request):
    return render(request,'index.html')

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        response.data['token'] = token.key
        return response

def home(request):
    return redirect('/api/auth/admin')


class WebsitesListView(ListCreateAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get(self,request):
        queryset = Website.objects.all()
        serialized_data = serialize('json', queryset)
        data = json.loads(serialized_data)
        return Response(data)
    
    def post(self,request):
        categories = request.data.getlist('category')
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            remote = RemoteStorage()
            image = remote.save_image(request=request)
            banners = remote.save_banners(request=request)
            print(banners)
            website = serializer.save(image = image,banners=banners)
            website.add_categories(categories) 
            website = website.save_data()
            if website:
                return Response(website ,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            

class WebsitesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self,request,pk):
        serialized_data = self.serializer_class.get_data(request,pk)
        print(serialized_data)
        return Response(serialized_data)
    

class CategoriesListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

class CategoriesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginSerializer
# class AdminAuthView(GenericAPIView):
#     serializer_class = AdminAuthSerializer

#     def post(self,request,format= None):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
        
#         user = authenticate(request,username= username,password = password)
#         if user:
#             login(request,user)
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

class AdminPageView(APIView):
    def get(self,request):
        websites = Website.objects.all().order_by('-added_on')
        categories = Category.objects.all().order_by('name')
        return Response({'Websites':{websites},'Categories':{categories}})