from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from .serializers import UserSerializer, UserLoginSerializer

from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

from django.core.exceptions import ObjectDoesNotExist

from .models import User

from recruitmentapi.utils.custom_exceptions import BadRequest


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response_obj = super(UserRegisterView, self).create(request, args, kwargs)
        user = User.objects.get(id=response_obj.data.get('id'))
        token, _ = Token.objects.get_or_create(user=user)
        response = {"status_code": status.HTTP_201_CREATED,
                    "message": "User successfully registered",
                    "result": response_obj.data,
                    "token": token.key}
        return Response(response)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            user_serializer = UserSerializer(user)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                response = {"status_code": status.HTTP_200_OK,
                            "message": "User successfully logged in",
                            "result": user_serializer.data,
                            "token": token.key}
                login(request, user)
                return Response(response)
            else:
                raise BadRequest({'message': "Incorrect Username or password"},
                                 code=status.HTTP_400_BAD_REQUEST)

        else:
            raise BadRequest({'message': "Invalid Username or password"},
                             code=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            Token.objects.get(user=request.user).delete()
            user_serializer = UserSerializer(request.user)
            response = {"status_code": status.HTTP_200_OK,
                        "message": "User successfully logged out",
                        "result": user_serializer.data}
            logout(request)
            return Response(response)
        except ObjectDoesNotExist:
            raise BadRequest({'message': "Invalid token. User not logged in"},
                             code=status.HTTP_400_BAD_REQUEST)
