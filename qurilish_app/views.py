from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from qurilish_app.serializers import LogInSerializer, RegisterSerializer


@permission_classes([permissions.AllowAny])
class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": LogInSerializer(user, context=self.get_serializer_context()).data
        })


@permission_classes([permissions.AllowAny])
class LoginApiView(GenericAPIView):
    serializer_class = LogInSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = LogInSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                user = authenticate(username=email, password=password)
                if user is None:
                    return Response({
                        'status': 400,
                        'message': 'Invalid password',
                        'data': {}
                    })
                else:
                    refresh = RefreshToken.for_user(user)

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
        except Exception as e:
            print(e)

