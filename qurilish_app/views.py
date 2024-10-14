from django.contrib.auth import authenticate, update_session_auth_hash, login, logout
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from qurilish_app.serializers import LogInSerializer, RegisterSerializer, PasswordChangeSerializer


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

    def post(self, *args, **kwargs):
        try:
            data = self.request.data
            serializer = LogInSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                user = authenticate(self.request, username=email, password=password)
                login(request=self.request, user=user)

                if user is None:
                    return Response({
                        'status': str(404),
                        'message': str('Invalid password')
                    })
                else:
                    refresh = RefreshToken.for_user(user)

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
        except Exception as e:
            print(e)


@permission_classes([permissions.IsAuthenticated])
class UserLogoutApiView(RetrieveAPIView):
    def get(self, *args, **kwargs):
        logout(self.request)
        return Response({'message': 'Log outed successfully.'})


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def change_password(request):
#     if request.method == 'POST':
#         serializer = PasswordChangeSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             if user.check_password(serializer.data.get('old_password')):
#                 user.set_password(serializer.data.get('new_password'))
#                 user.save()
#                 update_session_auth_hash(request, user)  # To update session after password change
#                 return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
#             return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([permissions.IsAuthenticated])
class PasswordChangeApiView(GenericAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PasswordChangeSerializer(data=data)
        if serializer.is_valid():
            user = request.user
            print(user.check_password(serializer.data.get('old_password')))
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
