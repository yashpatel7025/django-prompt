import uuid
import json

from typing import Optional
from django.utils import timezone
from faker import Faker

from django.test import TestCase
from django.urls import reverse
from django.contrib import auth

from project.models import Essay, FeedbackRequest, User, Comment

USER_PASSWORD = '12345'
JSON = 'application/json'


def user_factory(is_superuser=False):
	fake = Faker()
	email = fake.email()
	u = User.objects.create(
		first_name=fake.first_name(),
		last_name=fake.last_name(),
		username=email,
		email=email,
		is_superuser=is_superuser,
		is_staff=is_superuser
	)
	u.set_password(USER_PASSWORD)
	u.save()
	return u


def essay_factory(revision_of: Optional[Essay] = None):
	fake = Faker()
	admin_user = User.objects.filter(is_superuser=True).first()
	return Essay.objects.create(
		name=' '.join(fake.words(nb=5)),
		uploaded_by=admin_user,
		content=fake.paragraph(nb_sentences=5),
		revision_of=revision_of,
	)


def feedback_request_factory(essay: Essay, assign=False):
	""" Create a feedback request. """
	feedback_request = FeedbackRequest.objects.create(essay=essay, edited=False, deadline=timezone.now())
	if assign:
		feedback_request.assigned_editors(*User.objects.all())
	return feedback_request


class AuthenticationTestCase(TestCase):
	""" Test user authentication: login and logout. """

	def setUp(self):
		self.user = user_factory()

	def test_login(self):
		""" Check that login is functional. """
		url = reverse('user-login')

		# The user can load the /login/ page
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed('project/login.html')

		# The user cannot login with incorrect credentials
		data = {'username': self.user.username, 'password': 'WRONG'}
		response = self.client.post(url, data=json.dumps(data), content_type=JSON)
		self.assertEqual(response.status_code, 403)

		# The user can login with correct credentials
		data = {'username': self.user.username, 'password': USER_PASSWORD}
		response = self.client.post(url, data=json.dumps(data), content_type=JSON)
		self.assertEqual(response.status_code, 204)
		user = auth.get_user(self.client)
		self.assertTrue(user.is_authenticated)

	def test_logout(self):
		""" Check that logout is functional. """
		url = reverse('user-logout')
		self.client.force_login(self.user)

		# Logging out logs out the user
		response = self.client.post(url)
		self.assertEqual(response.status_code, 204)
		user = auth.get_user(self.client)
		self.assertFalse(user.is_authenticated)


class PlatformTestCase(TestCase):
	""" Verify that the platform is able to be loaded. """

	def setUp(self):
		self.user = user_factory()

	def test_load_platform(self):
		url = reverse('platform')

		# Loading the platform fails if the user is not authenticated
		response = self.client.get(url)
		self.assertEqual(response.status_code, 403)

		# Loading the platform works if the user is not authenticated
		self.client.force_login(self.user)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed('project/platform.html')


class FeedbackRequestViewTestCase(TestCase):
	""" Test feedback request views. """

	def setUp(self):
		self.user = user_factory()
		self.admin = user_factory(is_superuser=True)
		self.old_essay = essay_factory()
		self.essay = essay_factory(revision_of=self.old_essay)

		# The user sees requests matched with them, not requests matched with others
		self.fr_not_matched_with_editor = feedback_request_factory(self.old_essay)
		self.fr_not_matched_with_editor.assigned_editors.add(self.admin)
		self.fr_matched_with_editor = feedback_request_factory(self.essay)
		self.fr_matched_with_editor.assigned_editors.add(self.user)

	def test_get_list_without_login(self):
		url = reverse('feedback-request-list')

		# Must be authenticated to access feedback requests
		response = self.client.get(url)
		self.assertEqual(response.status_code, 403)


	def test_get_list_already_picked_up(self):

		self.client.force_login(self.user)
		url = reverse('feedback-request-list')
		# don't show feedback req. that are already picked up
		self.fr_matched_with_editor.picked_up_by = self.user
		self.fr_matched_with_editor.save()
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content)
		self.assertEqual(len(data), 0)

	def test_get_list_already_edited(self):

		self.client.force_login(self.user)
		url = reverse('feedback-request-list')
		# The user does not see requests that are edited
		self.fr_matched_with_editor.edited = True
		self.fr_matched_with_editor.save()
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content)
		self.assertEqual(len(data), 0)

	def test_get_list_matched_feedback_requests(self):
		""" Test listing feedback requests matched with the a user. """

		self.client.force_login(self.user)
		url = reverse('feedback-request-list')

		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content)
		
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0].get('pk'), self.fr_matched_with_editor.pk)
		self.assertIsInstance(data[0].get('essay'), dict)

	def test_get_detail_without_login(self):
		url = reverse('feedback-request-detail', kwargs={'pk':1}) 
		# Must be authenticated to access feedback requests
		response = self.client.get(url)
		self.assertEqual(response.status_code, 403)

	def test_get_detail(self):
	
		essay3 = essay_factory(revision_of=self.essay)
		essay4 = essay_factory(revision_of=essay3)
		essay5 = essay_factory(revision_of=essay4)
		# no feedback for 3rd essay
		# fr_for_e3= feedback_request_factory(essay3)
		# fr_for_e3.assigned_editors.add(self.user)
		fr_for_e4= feedback_request_factory(essay4)
		fr_for_e4.assigned_editors.add(self.user)
		fr_for_e5= feedback_request_factory(essay5)
		fr_for_e5.assigned_editors.add(self.user)

		url = reverse('feedback-request-detail', kwargs={'pk':fr_for_e4.id}) 
		self.client.force_login(self.user)

		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content)

		self.assertEqual(data.get('pk'), fr_for_e4.id)
		#current essay content visible
		self.assertIsInstance(data.get('essay'), dict) 
		previous_feedbacks = data.get('previous_feedback')
		self.assertEqual(len(previous_feedbacks), 2)
		l = list(map(lambda feedback:feedback.get('pk'), previous_feedbacks))
		#2nd and 1st feedback are previous feedbacks, 3rd feedback not exist
		self.assertEqual(l, [self.fr_not_matched_with_editor.id, self.fr_matched_with_editor.id])
		#previous essay content not visible, just pk is returned
		self.assertIsInstance(previous_feedbacks[0].get('essay'), int) 


	def test_patch_pick_up_request_without_login(self):
		url = reverse('feedback-request-detail', kwargs={'pk':1}) 
		# Must be authenticated to access feedback requests
		response = self.client.patch(url)
		self.assertEqual(response.status_code, 403)

	def test_patch_pick_up_request_validations(self):
		
		self.client.force_login(self.user)

		# user not in assigned_editor list
		url = reverse('feedback-request-detail', kwargs={'pk':self.fr_not_matched_with_editor.id}) 
		response = self.client.patch(url)
		self.assertEqual(response.status_code, 400)


		# if request is already picked by someone else
		url = reverse('feedback-request-detail', kwargs={'pk':self.fr_matched_with_editor.id}) 
		self.fr_matched_with_editor.picked_up_by = self.admin
		self.fr_matched_with_editor.save()
		response = self.client.patch(url)
		self.assertEqual(response.status_code, 400)

	def test_patch_pick_up_request(self):

		self.client.force_login(self.user)

		url = reverse('feedback-request-detail', kwargs={'pk':self.fr_matched_with_editor.id}) 
		
		self.assertEqual(self.fr_matched_with_editor.picked_up_by, None)
		response = self.client.patch(url)
		self.assertEqual(response.status_code, 200)
		self.fr_matched_with_editor.refresh_from_db()
		self.assertEqual(self.fr_matched_with_editor.picked_up_by, self.user)


class CommentTestCase(TestCase):
	""" Test feedback request views. """

	def setUp(self):
		self.user = user_factory()
		self.admin = user_factory(is_superuser=True)
		self.old_essay = essay_factory()
		self.essay = essay_factory(revision_of=self.old_essay)

		# The user sees requests matched with them, not requests matched with others
		self.fr_not_matched_with_editor = feedback_request_factory(self.old_essay)
		self.fr_not_matched_with_editor.assigned_editors.add(self.admin)
		self.fr_matched_with_editor = feedback_request_factory(self.essay)
		self.fr_matched_with_editor.assigned_editors.add(self.user)

	def test_post_comment_without_login(self):
		url = reverse('feedback-request-comment') 
		# Must be authenticated to post comment
		response = self.client.post(url)
		self.assertEqual(response.status_code, 403)

	def test_post_comment_validations(self):
		fake = Faker()
		self.client.force_login(self.user)
		#comment on non picked up request
		url = reverse('feedback-request-comment') 
		data = {'feedback_request': self.fr_matched_with_editor.id, 'text': fake.paragraph(nb_sentences=5)}
		response = self.client.post(url, data=json.dumps(data), content_type=JSON)
		self.assertEqual(response.status_code, 400)
		data = json.loads(response.content)

	def test_post_comment(self):
		fake = Faker()
		self.client.force_login(self.user)
		#comment on non picked up request
		url = reverse('feedback-request-comment') 
		self.fr_matched_with_editor.picked_up_by = self.user
		self.fr_matched_with_editor.save()
		data = {'feedback_request': self.fr_matched_with_editor.id, 'text': fake.paragraph(nb_sentences=5)}
		self.assertEqual(self.fr_matched_with_editor.edited, False)
		response = self.client.post(url, data=json.dumps(data), content_type=JSON)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Comment.objects.all().count(), 1)
		self.fr_matched_with_editor.refresh_from_db()
		self.assertEqual(self.fr_matched_with_editor.edited, True)





		













		



















