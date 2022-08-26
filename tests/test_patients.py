"""Test patient routes."""

import pytest
from fastapi import status
from pytest_lazyfixture import lazy_fixture


class TestPatients:
    """Testing patient operations."""

    url = "/patients"

    @pytest.mark.anyio
    def test_anon_patient(self, anon_client):
        """Ensure anonymous client cannot access the data.

        And this is present on all methods.
        """
        response = anon_client.get(f"{self.url}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

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
                status.HTTP_201_CREATED,
                id="Normal staff",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_201_CREATED,
                id="Admin staff",
            ),
        ],
    )
    def test_create_patient(self, selected_client, status_code, fake_patient):
        """Creating a patient."""
        response = selected_client.post(f"{self.url}/", json=fake_patient)
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert response.json()["name"] == fake_patient["name"]

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
    def test_read_patients(self, selected_client, status_code, mock_patient):
        """Reading all patients."""
        response = selected_client.get(f"{self.url}/")
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert mock_patient.name in [i["name"] for i in response.json()]

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
    def test_read_patient(self, selected_client, status_code, mock_patient):
        """Reading a single patient."""
        response = selected_client.get(f"{self.url}/{mock_patient.id}")
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert response.json()["name"] == mock_patient.name

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
    def test_update_patient(
        self, selected_client, status_code, mock_patient, patient_update
    ):
        """Updating a single patient."""
        old_mock_patient_name = str(mock_patient.name)
        old_mock_patient_dob = str(mock_patient.dob)
        response = selected_client.patch(
            f"{self.url}/{mock_patient.id}", json=patient_update
        )
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert response.json()["name"] != old_mock_patient_name
            assert response.json()["dob"] != old_mock_patient_dob
            assert response.json()["name"] == patient_update["name"]
            assert response.json()["dob"] == patient_update["dob"]

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
                status.HTTP_204_NO_CONTENT,
                id="Normal staff",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_204_NO_CONTENT,
                id="Admin staff",
            ),
        ],
    )
    def test_delete_patient(self, selected_client, status_code, mock_patient):
        """Deleting a single patient."""
        response = selected_client.delete(f"{self.url}/{mock_patient.id}")
        assert response.status_code == status_code
        if status_code == status.HTTP_204_NO_CONTENT:
            get_response = selected_client.get(f"{self.url}/{mock_patient.id}")
            assert get_response.status_code == status.HTTP_404_NOT_FOUND
