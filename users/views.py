from rest_framework import status, viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from users.serializers import UserRegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger('django')


# custom permission
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'message': 'User registered successfully',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username
                    }
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(
                f"Failed to register user:  {str(e)}"
            )
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({
                    'error': 'Please provide both email and password'
                }, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(email=email, password=password)

            if not user:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'User login successfully',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
            })
        except Exception as e:
            logger.error(
                f"Failed to login user:  {str(e)}"
            )
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {
                "message": "User retrieve successfully!", 
                 "data": serializer.data
                 },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error in UserViewSet retrieve method: {str(e)}")
            return Response(
                {
                    "error": "Failed to retrieve user.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "User updated successfully!", 
                    "data": serializer.data
                },
                status=status.HTTP_200_OK,
            )
        
        except Exception as e:
            logger.error(
                f"Error updating userId {self.get_object().id}: {str(e)}"
            )
            return Response(
                {
                    "error": "Failed to update user.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            if user.id != instance.id:
                return Response(
                    {
                        "error": "You do not have permission to delete this user."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            instance.delete()
            return Response(
                {
                    "message": "User deleted successfully!"
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(
                f"Error deleting userId {self.get_object().id}: {str(e)}"
            )
            return Response(
                {
                    "error": "Failed to delete user.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )   