from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, JobPostSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .models import JobPost

# User Registration
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to register
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "User registered successfully",
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login and JWT Token Generation
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to log in
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


# List all job posts of the logged-in user or create a new job post
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access
def job_post_list_create(request):
    if request.method == 'GET':
        # Get all job posts created by the logged-in user
        job_posts = JobPost.objects.filter(user=request.user)
        serializer = JobPostSerializer(job_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Create a new job post for the logged-in user
        serializer = JobPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associate the job post with the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a specific job post based on the logged-in user and post ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access
def job_post_detail(request, pk):
    try:
        # Ensure the job post belongs to the logged-in user
        job_post = JobPost.objects.get(pk=pk, user=request.user)
    except JobPost.DoesNotExist:
        return Response({"error": "Job post not found or you do not have permission to view it."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Return job post details
        serializer = JobPostSerializer(job_post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the job post
        serializer = JobPostSerializer(job_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the job post
        job_post.delete()
        return Response({"message": "Job post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
