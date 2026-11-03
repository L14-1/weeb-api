from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Article


User = get_user_model()

class ArticleTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='test1234!'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='test1234!'
        )

        self.article = Article.objects.create(
            title='Article test',
            content='Contenu test',
            owner=self.user1
        )


    def test_get_all_articles(self):
        url = reverse('article-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_article_with_auth_user(self):
        url = reverse('article-list')

        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Titre de larticle de test',
            'content': 'Contenu de l article'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
        self.assertEqual(Article.objects.last().owner, self.user1)


    def test_create_article_unauth_user(self):
        url = reverse('article-list')

        data = {
            'title': 'Article interdit unauth',
            'content': 'Contenu interdit'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_owner_can_update_article(self):
        url = reverse('article-detail', kwargs={'uuid': self.article.uuid})
        self.client.force_authenticate(user=self.user1)

        data = {
            'title': 'Titre modifié',
            'content': 'Contenu modifié'
        }
 
        response = self.client.put(url, data)
        self.article.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.title, 'Titre modifié')


    def test_others_users_cannot_update_article(self):
        url = reverse('article-detail', kwargs={'uuid': self.article.uuid})

        self.client.force_authenticate(user=self.user2)
        data = {
            'title': 'Test modif interdite',
            'content': 'Test modif interdite'
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_owner_soft_delete_article(self):
        url = reverse('article-detail', kwargs={'uuid': self.article.uuid})

        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(url)

        self.article.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNotNone(self.article.deleted_at)
        self.assertEqual(Article.objects.count(), 1) # article soft-deleted toujours présent 


    def test_soft_deleted_article_filtered(self):
        self.article.soft_delete()

        url = reverse('article-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0) # get articles filtre bien les articles soft-deleted