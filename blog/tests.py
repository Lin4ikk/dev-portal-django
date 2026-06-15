from django.test import TestCase
from django.urls import reverse
from django.db.models.signals import post_save
from accounts.models import CustomUser, Profile
from blog.models import Post, Category

class BlogTests(TestCase):

    def setUp(self):
        post_save.disconnect(sender=CustomUser, dispatch_uid="create_user_profile")
        post_save.disconnect(sender=CustomUser, dispatch_uid="save_user_profile")

        self.user = CustomUser.objects.create_user(
            username='testuser', 
            password='password123',
            role=CustomUser.ROLE_AUTHOR
        )
        
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        
        self.category = Category.objects.create(
            title='Тест Категория', 
            slug='test-cat'
        )
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Текст тестового поста для проверки поиска.',
            author=self.user,
            category=self.category,
            is_published=True
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Тестовый пост')
        self.assertEqual(self.post.author.username, 'testuser')

    def test_custom_method_comments_count(self):
        self.assertEqual(self.post.get_comments_count(), 0)

    def test_custom_method_read_time(self):
        self.assertEqual(self.post.get_read_time(), 1)

    def test_custom_method_absolute_url(self):
        expected_url = reverse('blog:post_detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_home_page_status_code(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_post_detail_page_status_code(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_search_functional(self):
        response = self.client.get(reverse('blog:home'), {'q': 'проверки'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый пост')

    def test_search_no_results(self):
        response = self.client.get(reverse('blog:home'), {'q': 'несуществующееслово'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Тестовый пост')