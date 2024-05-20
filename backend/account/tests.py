from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='old_password')

    def test_send_password_reset_email(self):
        response = self.client.post(reverse('account:password_reset'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)  # Перенаправление после отправки формы
        self.assertEqual(len(mail.outbox), 1)  # Проверка, что письмо было отправлено
        self.assertIn('password_reset_confirm', mail.outbox[0].body)  # Проверяем, что в письме есть ссылка сброса
    

    def test_password_reset_confirm(self):
    # Получаем токен и uid
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        # Проверяем, что страница сброса пароля доступна
        response = self.client.get(reverse('account:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 200)

        # Отправляем новый пароль
        response = self.client.post(reverse('account:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}), {
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после установки нового пароля


    def test_reset_password_complete(self):
    # Процесс входа после сброса
        self.client.login(username='testuser', password='new_password')
        response = self.client.get(reverse('account:dashboard'))
        self.assertEqual(response.status_code, 200)  # Доступ к защищенной странице