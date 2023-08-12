from django.contrib import admin

from .models import Comment, Exhibit, FeedBack, Route


admin.site.register(Comment)
admin.site.register(Exhibit)
admin.site.register(FeedBack)
admin.site.register(Route)
