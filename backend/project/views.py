from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout

from rest_framework import views
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from project.models import FeedbackRequest

from project.serializers import EssaySerializer, ListFeedbackRequestSerializer, DetailFeedbackRequestSerializer, CommentSerializer
from project.utilities import FeedbackRequestManager, is_valid_pickup_request


class FeedbackRequestViewSet(viewsets.GenericViewSet):
	""" Viewset for views pertaining to feedback requests. """

	permission_classes = (IsAuthenticated,)

	def get_list(self, request,):
		 feedback_requests = FeedbackRequestManager.query_for_user(self.request.user, include_edited=False, only_picked_up=False).select_related('essay').order_by("deadline")
		 serialized = ListFeedbackRequestSerializer(feedback_requests, many=True).data
		 return Response(serialized, status=status.HTTP_200_OK)

	def get_detail(self, request, pk=None):
		serialized = DetailFeedbackRequestSerializer(FeedbackRequest.objects.get(id=pk)).data
		return Response(serialized, status=status.HTTP_200_OK)

	def patch_pick_up_request(self, request, pk, *args, **kwargs):
		feedback_request = FeedbackRequest.objects.get(id=pk)
		is_valid, response  = is_valid_pickup_request(feedback_request, request)
		if not is_valid:
			return response
		feedback_request.picked_up_by = request.user
		feedback_request.save()
		return  Response({'message':'feedback request picked up successfully'}, status=status.HTTP_200_OK)


class CommentView(views.APIView):

	permission_classes = (IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		serializer = CommentSerializer(data=request.data,  context={'request':request})
		if serializer.is_valid():
			comment = serializer.save()
			comment.feedback_request.edited = True
			comment.feedback_request.save()
			return Response({'message':'feedback submitted'}, status=status.HTTP_200_OK)
		else:
			return Response({'errors': dict(serializer.errors.items())}, status=status.HTTP_400_BAD_REQUEST)


class HomeView(views.APIView):
	""" View that takes users who navigate to `/` to the correct page, depending on login status. """

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/platform/')
		return redirect('/login/')


class PlatformView(views.APIView):
	""" View that renders the essay review platform. """

	permission_classes = (IsAuthenticated,)

	def get(self, *args, **kwargs):
		return render(self.request, 'project/platform.html', {})


class LoginView(views.APIView):
	""" View for user login. """

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/platform/')
		return render(self.request, 'project/login.html', {})

	def post(self, request, *args, **kwargs):
		user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
		if user is None:
			# Auth failure
			return Response({'detail': 'Incorrect email or password.'}, status=status.HTTP_403_FORBIDDEN)
		auth_login(request, user)
		return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(views.APIView):
	""" View for user logout. """

	def post(self, request, *args, **kwargs):
		auth_logout(request)
		return Response(status=status.HTTP_204_NO_CONTENT)
