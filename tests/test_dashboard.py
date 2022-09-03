"""Test dashboard endpoints."""

import pytest
from fastapi import status
from pytest_lazyfixture import lazy_fixture


class TestDashboard:
    """Testing the dashboard."""

    url = "/dashboard/"

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
                status.HTTP_200_OK,
                id="Normal staff",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_200_OK,
                id="Admin staff",
            ),
        ],
    )
    def test_access_self(self, selected_client, status_code):
        """Able to access self if user.

        Anonymous users are not able to access self.
        """
        response = selected_client.get(f"{self.url}")
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            # TODO: try and access the user.
            assert isinstance(response.json()["full_name"], str)

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
                status.HTTP_200_OK,
                id="Normal staff",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_200_OK,
                id="Admin staff",
            ),
        ],
    )
    def test_edit_self(self, selected_client, status_code, user_update):
        """Able to access self if user.

        Anonymous users are not able to access self.
        """
        selected_user = selected_client.get(f"{self.url}").json()
        old_username = selected_user.get("username")
        old_full_name = selected_user.get("full_name")
        response = selected_client.patch(f"{self.url}", json=user_update)
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert response.json()["username"] == user_update["username"]
            assert response.json()["full_name"] == user_update["full_name"]
        else:
            assert selected_user.get("username") == old_username
            assert selected_user.get("full_name") == old_full_name
