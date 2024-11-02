from django.contrib import admin
from qurilish_app.models import Posts, Likes


# Register your models here.

class LikesInline(admin.TabularInline):
    model = Likes
    extra = 1


class CommentsInline(admin.TabularInline):
    model = Posts.comments.through
    extra = 1


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    inlines = [LikesInline, CommentsInline]
    list_display_links = ('title',)
    list_display = ('title', 'author', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'author')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
            obj.save()
        else:
            obj.save()
