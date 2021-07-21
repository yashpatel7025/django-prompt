from django.db.models import query
from project.models import FeedbackRequest, User
from rest_framework import status
from rest_framework.response import Response

class FeedbackRequestManager:
	""" Helper methods related to FeedbackRequests. """

	@staticmethod
	def query_for_user(user: User, include_edited: bool = False, only_picked_up: bool = False):
		""" Query all FeedbackRequests available to the current user.

			Includes those that are finished if requested. Otherwise, includes only unfinished.
		"""

		# include_edited = True and only_picked_up=True -> all picked up request by current user(irrespective of edited)
		# include_edited = False and only_picked_up=False -> all non pickedup request --> in our case
		# include_edited = True and only_picked_up=False ->  all non pickedup request
		# include_edited = False and only_picked_up=True -> non edited pickedup request
		
		queryset = FeedbackRequest.objects.filter(assigned_editors=user, picked_up_by= user if only_picked_up else None)
		if not include_edited:
			queryset = queryset.filter(edited=False)
		return queryset
		

def is_valid_pickup_request(feedback_request: FeedbackRequest, request):
	if not feedback_request.assigned_editors.filter(id=request.user.id).exists():
		return (False, Response({'message': 'request can not be picked, you are not assignee of this feedback request'}, status=status.HTTP_400_BAD_REQUEST))
	if feedback_request.picked_up_by:
		return  (False, Response({'message': 'request already picked by other editor'}, status=status.HTTP_400_BAD_REQUEST))
	return (True, None)