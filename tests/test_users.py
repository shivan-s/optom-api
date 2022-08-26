"""Test users routes."""

import pytest
from fastapi import status
from pytest_lazyfixture import lazy_fixture


class TestUsers:

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
        response = selected_client.get(f"{self.url}/{mock_user.username}/")
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert response.json()["full_name"] == mock_user.full_name
