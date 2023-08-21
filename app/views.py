from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import AppUser, GlobalUserdata, ContactList, SpamReport
from .serializer import SearchByNameSerializer, SpamReportSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class UserSignUp(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')

        if not phone_number or not password or not username or not name :
            return Response({'error': 'Username, Password, name and PhoneNumber are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if AppUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = AppUser.objects.create_user(username=username,phone_number=phone_number,email=email,password=password, name=name)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User registration failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSignIn(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
      
class userSearch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):       
        
        if 'name' in request.GET and 'number' in request.GET:
            return Response({'error': 'Pass either Name or Number'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif 'name' in request.GET:
            name = request.GET['name']
            queryset = GlobalUserdata.objects.filter(name__icontains=name)
            ordered_queryset = sorted(queryset, key=lambda x: x.name.startswith(name), reverse=True)
            serializer = SearchByNameSerializer(ordered_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif 'number' in request.GET:
            number = request.GET['number']

            if number:
                registered_user = AppUser.objects.filter(phone_number=number).first()

                if registered_user:
                    queryset = GlobalUserdata.objects.filter(name=registered_user.name).first()
                    serializer = SearchByNameSerializer(queryset)

                    presentInContact = ContactList.objects.filter(user=registered_user, phone_number=request.user.phone_number).first()

                    if presentInContact:
                        addEmailField = {**serializer.data, **{"email": registered_user.email}}

                        return Response(addEmailField, status=status.HTTP_200_OK)
                    
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    queryset = GlobalUserdata.objects.filter(phone_number=number)
                    serializer = SearchByNameSerializer(queryset, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Phone Number is missing'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'No prameter is passed'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class spam(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if 'number' in request.GET:
            number = request.GET['number']
            try:
                spam_report = SpamReport.objects.create(phone_number=number, reporter=request.user)
                serializer = SpamReportSerializer(spam_report)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Already Added"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({'error': 'Number prameter is required'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

class addEmail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_valid_email(email):
            user = AppUser.objects.get(username=request.user)
            user.email = email
            user.save()
            return Response({'success': 'Email updated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)



class NotFoundView(APIView):
    def get(self, request):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)