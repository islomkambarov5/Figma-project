from django.contrib.auth import authenticate, update_session_auth_hash, login, logout
from django.shortcuts import render

# Create your views here.
from django.utils.timezone import now
from rest_framework import permissions, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from qurilish_app.models import Posts, Comments
from qurilish_app.serializers import LogInSerializer, RegisterSerializer, PasswordChangeSerializer, PostSerializer, \
    CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     # Allow authenticated users to create new instances via POST
    #     if request.method == "POST" and request.user.is_authenticated:
    #         return True
    #     return True

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj.author == request.user
        )
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # return obj.author == request.user


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
        try:
            logout(self.request)
            return Response({'message': 'Log outed successfully.'})
        except:
            return Response({'status': 400, 'message': 'Something went wrong, please try again'})


@permission_classes([permissions.IsAuthenticated])
class PasswordChangeApiView(GenericAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PasswordChangeSerializer(data=data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([permissions.AllowAny])
class PostAPIView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


@permission_classes([IsOwnerOrReadOnly])
class PostDetailAPIView(RetrieveDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Posts.objects.all()
    lookup_field = "slug"

    def get(self, *args, **kwargs):
        post = Posts.objects.get(slug=self.kwargs['slug'])
        comments = Comments.objects.filter(post=post)
        serialized_comments = CommentSerializer(comments, many=True)
        return Response({
            'id': post.id,
            'title': post.title,
            'context': post.context,
            'comments': serialized_comments.data
        })

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Только зарегистрированные пользователи могут оставлять комментарии.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        serializer = CommentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            post = Posts.objects.get(slug=self.kwargs["slug"])
            serializer.save(post=post)
            return Response({'status': status.HTTP_201_CREATED})
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND})


@permission_classes([IsOwnerOrReadOnly])
class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
