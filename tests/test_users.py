"""Test users routes."""

import pytest
from fastapi import status
from pytest_lazyfixture import lazy_fixture

from app.sql import models


class TestUsers:
    """Test for users."""

    url = "/users"

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        "selected_client,status_code",
        [
            pytest.param(
                lazy_fixture("anon_client"),
                status.HTTP_401_UNAUTHORIZED,
                id="Not logged in",
            ),
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_403_FORBIDDEN,
                id="Normal staff",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_201_CREATED,
                id="Admin staff",
            ),
        ],
    )
    def test_create_user(self, selected_client, status_code, fake_user):
        """Test creation of users. Only admin users can create user."""
        response = selected_client.post(f"{self.url}/", json=fake_user)
        assert response.status_code == status_code
        if status_code == status.HTTP_201_CREATED:
            assert response.json()["full_name"] == fake_user["full_name"]

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        "selected_client,status_code",
        [
            pytest.param(
                lazy_fixture("anon_client"),
                status.HTTP_401_UNAUTHORIZED,
                id="Not logged in",
            ),
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_403_FORBIDDEN,
                id="Normal staff",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_200_OK,
                id="Admin staff",
            ),
        ],
    )
    def test_get_users(self, selected_client, status_code, mock_user):
        """Test the the list view of users.

        Only admin users can access this.
        """
        response = selected_client.get(f"{self.url}/")
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert mock_user.full_name in [i["full_name"] for i in response.json()]

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        "selected_client,status_code",
        [
            pytest.param(
                lazy_fixture("anon_client"),
                status.HTTP_401_UNAUTHORIZED,
                id="Not logged in",
            ),
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_403_FORBIDDEN,
                id="Normal staff",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_200_OK,
                id="Admin staff",
            ),
        ],
    )
    def test_get_user(self, selected_client, status_code, mock_user):
        """Test getting a single users.

        Only admin level staff can do this.
        """
        response = selected_client.get(f"{self.url}/{mock_user.username}/")
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert response.json()["full_name"] == mock_user.full_name

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        "selected_client,status_code",
        [
            pytest.param(
                lazy_fixture("anon_client"),
                status.HTTP_401_UNAUTHORIZED,
                id="Not logged in",
            ),
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_403_FORBIDDEN,
                id="Normal staff",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_200_OK,
                id="Admin staff",
            ),
        ],
    )
    def test_edit_user(self, selected_client, status_code, mock_user, user_update):
        """Test editing a single user.

        Only admin level staff can do this.
        """
        old_mock_user_username = str(mock_user.username)
        old_mock_user_full_name = str(mock_user.full_name)
        response = selected_client.patch(
            f"{self.url}/{mock_user.username}", json=user_update
        )
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert response.json()["username"] == user_update["username"]
            assert response.json()["full_name"] == user_update["full_name"]
        else:
            assert mock_user.username == old_mock_user_username
            assert mock_user.full_name == old_mock_user_full_name

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        "selected_client,status_code",
        [
            pytest.param(
                lazy_fixture("anon_client"),
                status.HTTP_401_UNAUTHORIZED,
                id="Not logged in",
            ),
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_403_FORBIDDEN,
                id="Normal staff",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_204_NO_CONTENT,
                id="Admin staff",
            ),
        ],
    )
    def test_delete_user(self, selected_client, status_code, mock_user, db):
        """Test deleting a single user.

        Only admin level staff can do this.
        """
        response = selected_client.delete(f"{self.url}/{mock_user.username}")
        db_user = (
            db.query(models.User)
            .filter(models.User.username == mock_user.username)
            .one_or_none()
        )
        assert response.status_code == status_code
        if status_code == status.HTTP_204_NO_CONTENT:
            assert db_user is None
        else:
            assert db_user.full_name == mock_user.full_name
