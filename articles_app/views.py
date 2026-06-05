from rest_framework import viewsets
from .models import Article
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializers import ArticleSerializer

"""
CRUD complet pour les articles
"""
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('owner', 'owner__profile').all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)