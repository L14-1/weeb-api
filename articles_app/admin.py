from django.contrib import admin
from .models import Article
 

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'uuid',
        'title',
        'owner',
        'created_at',
        'updated_at',
        'deleted_at',
    )

    readonly_fields = (
        'uuid',
        'created_at',
        'updated_at',
        'deleted_at',
    )

    list_filter = (
        'created_at',
        'updated_at',
        'deleted_at',
    )

    search_fields = (
        'title',
        'content',
        'owner__username',
        'owner__email',
        'owner__first_name',
        'owner__last_name',
    )