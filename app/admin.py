from django.contrib import admin

# Register your models here.
from app.models import Board, WorkIn, PostIt, VoteIn

admin.site.register(Board)
admin.site.register(WorkIn)
admin.site.register(PostIt)
admin.site.register(VoteIn)