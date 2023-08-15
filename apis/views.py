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
# Create your views here.
def index(request):
    return render(request,'index.html')

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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            image = RemoteStorage.save_image(request)
            banners = RemoteStorage.save_banners(request)
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
    permission_classes = [IsAdminUser]

    def get(self,request,pk):
        serialized_data = self.serializer_class.get(self,request,pk)
        # data = json.loads(queryset)
        return Response(serialized_data.data)
    

class CategoriesListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

class CategoriesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class AdminAuthView(GenericAPIView):
    serializer_class = AdminAuthSerializer

    def post(self,request,format= None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(request,username= username,password = password)
        if user:
            login(request,user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AdminPageView(APIView):
    def get(self,request):
        websites = Website.objects.all().order_by('-added_on')
        categories = Category.objects.all().order_by('name')
        return Response({'Websites':{websites},'Categories':{categories}})