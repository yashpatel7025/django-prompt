from django.contrib import admin
from .models import *
# Register your models here.

class FeedbackRequestAdmin(admin.ModelAdmin): 
    list_display = ('pk', 'essay', 'edited', 'picked_up_by' ,'deadline')

class EssayAdmin(admin.ModelAdmin): 
    list_display = ('pk', 'name', 'uploaded_by', 'content' ,'revision_of')

admin.site.register(User)
admin.site.register(Essay, EssayAdmin)
admin.site.register(FeedbackRequest, FeedbackRequestAdmin)
admin.site.register(Comment)
