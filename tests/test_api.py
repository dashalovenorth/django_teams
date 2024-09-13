from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from datetime import date

from app.models import Project, Team


def create_api_test(model_class, url, creation_attrs):
    class ApiTest(TestCase):
        def setUp(self):
            self.client = APIClient()
            # users
            self.user = User(username="user", password="user")
            self.superuser = User(
                username="admin", password="admin", is_superuser=True
            )
            # tokens for users
            self.user_token = Token(user=self.user)
            self.superuser_token = Token(user=self.superuser)

        def api_methods(
            self,
            user: User,
            token: Token,
            post_exp: int,
            put_exp: int,
            delete_exp: int,
        ):
            self.client.force_authenticate(user=user, token=token)

            # create model object
            self.created_id = model_class.objects.create(**creation_attrs).id
            instance_url = f"{url}{self.created_id}/"

            # GET all
            self.assertEqual(
                self.client.options(url).status_code, status.HTTP_200_OK
            )

            # HEAD all
            self.assertEqual(
                self.client.head(url).status_code, status.HTTP_200_OK
            )

            # OPTIONS all
            self.assertEqual(
                self.client.get(url).status_code, status.HTTP_200_OK
            )

            # GET instance
            self.assertEqual(
                self.client.get(instance_url).status_code, status.HTTP_200_OK
            )

            # OPTIONS instance
            self.assertEqual(
                self.client.get(instance_url).status_code, status.HTTP_200_OK
            )

            # POST
            self.assertEqual(
                self.client.post(url, creation_attrs).status_code, post_exp
            )

            # PUT
            self.assertEqual(
                self.client.put(instance_url, creation_attrs).status_code,
                put_exp,
            )

            # DELETE
            self.assertEqual(
                self.client.delete(instance_url).status_code, delete_exp
            )

        def test_superuser(self):
            self.api_methods(
                self.superuser,
                self.superuser_token,
                status.HTTP_201_CREATED,
                status.HTTP_200_OK,
                status.HTTP_204_NO_CONTENT,
            )

        def test_user(self):
            self.api_methods(
                self.user,
                self.user_token,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_403_FORBIDDEN,
            )

    return ApiTest


ProjectApiTest = create_api_test(
    Project,
    "/api/project/",
    {"name": "A", "date_start": date.today(), "status": "готов"},
)
TeamApiTest = create_api_test(
    Team,
    "/api/team/",
    {"name": "Q"}
)
