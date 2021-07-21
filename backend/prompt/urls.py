"""prompt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project.views import *

feedback_request_list = FeedbackRequestViewSet.as_view({
    'get': 'get_list'
})
feedback_request_detail = FeedbackRequestViewSet.as_view({
    'get': 'get_detail',
    'patch': 'patch_pick_up_request'
})

urlpatterns = [

	path('admin/', admin.site.urls),
	path('', HomeView.as_view(), name='home'),
	path('login/', LoginView.as_view(), name='user-login'),
	path('logout/', LogoutView.as_view(), name='user-logout'),
	path('platform/', PlatformView.as_view(), name='platform'),

    path('api/feedback-request/',feedback_request_list, name='feedback-request-list'),
    path('api/feedback-request/<int:pk>/',feedback_request_detail, name='feedback-request-detail'),
    path('api/feedback-request/comment/', CommentView.as_view(), name='feedback-request-comment'),

]
