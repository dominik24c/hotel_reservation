from account.models import Customer
from account.models import HotelOwner
from base.test import BaseApiTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from .factory import create_hotels, create_comments
from ..models import Comment, Hotel


class BaseCommentTestCase(BaseApiTestCase):
    hotel_id = None
    AMOUNT_OF_COMMENTS = 5

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        users = list(User.objects.all())
        hotels = create_hotels(list(HotelOwner.objects.all()))
        cls.hotel_id = hotels[0].id
        create_comments(users, hotels, cls.AMOUNT_OF_COMMENTS)

    def setUp(self) -> None:
        self.user = Customer.objects.first()
        self.client.force_authenticate(self.user)


class CommentApiViewTest(BaseCommentTestCase):
    def test_list_comment_view(self) -> None:
        response = self.client.get(reverse('hotel:hotel-comments-list', kwargs={'hotel_pk': str(self.hotel_id)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertEqual(len(data), self.AMOUNT_OF_COMMENTS)

    def test_get_comment_view(self) -> None:
        comment = Comment.objects.filter(hotel__id=self.hotel_id).first()
        response = self.client.get(reverse('hotel:hotel-comments-detail',
                                           kwargs={'hotel_pk': str(self.hotel_id), 'pk': comment.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(str(comment.id), data['id'])
        self.assertEqual(comment.user.username, data['username'])
        self.assertEqual(comment.rating, data['rating'])
        self.assertEqual(comment.content, data['content'])
        self.assertEqual(comment.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), data['date'])


class CommentCRUApiView(BaseCommentTestCase):
    def test_create_comment_view(self) -> None:
        hotel = Hotel.objects.prefetch_related('comments').first()
        amount_of_comments = hotel.comments.count()

        body = {
            'hotel_id': hotel.id,
            'content': 'Hello there!',
            'rating': 4
        }
        response = self.client.post(reverse('hotel:hotel-comments-list', kwargs={'hotel_pk': hotel.id}), body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        hotel.refresh_from_db()

        self.assertEqual(amount_of_comments + 1, hotel.comments.count())

    def test_update_comment_view(self) -> None:
        comment = Comment.objects.filter(user__id=self.user.id).first()
        body = {
            'content': 'Hello there!',
            'rating': 4
        }
        response = self.client.put(
            reverse('hotel:hotel-comments-detail', kwargs={'hotel_pk': comment.hotel.id, 'pk': comment.id}), body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()

        self.assertEqual(comment.content, body['content'])
        self.assertEqual(comment.rating, body['rating'])

    def test_delete_comment_view(self) -> None:
        comment = Comment.objects.filter(user__id=self.user.id).first()
        response = self.client.delete(
            reverse('hotel:hotel-comments-detail', kwargs={'hotel_pk': comment.hotel.id, 'pk': comment.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Comment.DoesNotExist):
            comment.refresh_from_db()
