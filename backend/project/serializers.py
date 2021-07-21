from rest_framework import serializers
from project.models import Essay, FeedbackRequest, Comment


class EssaySerializer(serializers.ModelSerializer):
	""" Serialize an Essay. """

	class Meta:
		model = Essay
		fields = (
			'pk',
			'name',
			'uploaded_by',
			'content',
			'revision_of',
		)


class CommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = ('id', 'feedback_request', 'date', 'text')


	def validate(self, data):
		request = self.context['request']
		if data['feedback_request'].picked_up_by != request.user:
			raise serializers.ValidationError("request is not picked by you or might have picked by some other editor")
		return data

class ListFeedbackRequestSerializer(serializers.ModelSerializer):
	""" Serialize a FeedbackRequest. """

	essay = EssaySerializer()

	class Meta:
		model = FeedbackRequest
		fields = ('pk', 'essay', 'edited', 'picked_up_by','deadline')

class PreviousFeedbackRequestSerializer(serializers.ModelSerializer):

	comments = CommentSerializer(many = True)

	class Meta:
		model = FeedbackRequest
		fields = ('pk', 'essay', 'edited', 'picked_up_by','deadline', 'comments')


class DetailFeedbackRequestSerializer(serializers.ModelSerializer):
	""" Serialize a FeedbackRequest. """

	essay = EssaySerializer()
	comments = CommentSerializer(many = True)
	previous_feedback = serializers.SerializerMethodField()

	class Meta:
		model = FeedbackRequest
		fields = ('pk', 'essay', 'edited', 'picked_up_by','deadline', 'comments', 'previous_feedback')

	def get_previous_feedback(self, obj):
		previous_feedbacks = []
		essay = obj.essay
		while essay:
			if hasattr(essay, 'feedback_request'):
				previous_feedbacks.append(essay.feedback_request)
			essay = essay.revision_of
		#order by created, consider upto 0 but not 0th, 0th is itself, we want previous
		return PreviousFeedbackRequestSerializer(previous_feedbacks[:0:-1], many=True).data 

