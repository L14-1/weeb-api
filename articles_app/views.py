from rest_framework import viewsets
from .models import Article
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializers import ArticleSerializer

"""
CRUD complet pour les articles
"""
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Article.objects.select_related('owner', 'owner__profile').filter(deleted_at__isnull=True)


    def perform_destroy(self, instance):
        instance.soft_delete()
