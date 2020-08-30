from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics
from .serializers import NoteSerializer
from .models import Note
# Create your views here.

class UserCreate(APIView):
	""" 
	Creates the user. 
	"""

	def post(self, request, format='json'):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				return Response('account created', status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request):
		username = request.data.get('username', None)
		password = request.data.get('password', None)
		if username and password:
			try:
				user = authenticate(username=username, password=password)
				if user is not None:
					return Response({'status': 'success','userId': user.id}, status=status.HTTP_200_OK)
				else:
					return Response({'status': 'failed', 'message': 'user does not exist'}, status=status.HTTP_200_OK)
			except Exception as e:	
				return Response({'status': 'failed', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'status': 'failed', 'message': 'username and password are required'}, status=status.HTTP_400_BAD_REQUEST)


class UserNotesListView(generics.ListCreateAPIView):
	serializer_class = NoteSerializer

	def get_queryset(self):
		user_id = self.request.GET.get('user',None)
		queryset = []
		if user_id:
			user = User.objects.filter(id=user_id)
			if user:
				queryset = Note.objects.filter(user=user[0]).order_by('-created_at')
		return queryset

	def create(self, request, *args, **kwargs):
		user_id = request.data.get('user', None)
		note = request.data.get('note', "")
		data = {}
		if user_id:
			try:
				user = User.objects.get(id=user_id)
				data['text'] = note
				data['user'] = user_id
				serializer = self.serializer_class(data=data)
				if serializer.is_valid():
				  serializer.save()
				  return Response({'status':'success'}, status=status.HTTP_201_CREATED)
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			except User.DoesNotExist:
				return Response({"status":"failed", "message":"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"status":"failed", "message":"user id required"}, status=status.HTTP_400_BAD_REQUEST)