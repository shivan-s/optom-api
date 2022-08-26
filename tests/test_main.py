"""Test for project."""

import pytest
from fastapi import status


class TestMain:
    """Testing the root."""

    url = ""

    @pytest.mark.anyio
    def test_root(self, client):
        response = client.get(f"{self.url}/")
        assert response.status_code == status.HTTP_200_OK
