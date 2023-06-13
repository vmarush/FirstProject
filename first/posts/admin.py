from django.contrib import admin

from .models import Post, PostTag, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "get_tags", "category", "description","date_create")

    def get_tags(self, obj):
        tags = obj.tags.all()
        return "\n".join([t.title for t in tags])


admin.site.register(PostTag)
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
