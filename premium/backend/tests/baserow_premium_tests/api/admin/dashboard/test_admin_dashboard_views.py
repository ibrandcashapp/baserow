from django.shortcuts import reverse
from django.test.utils import override_settings

import pytest
from freezegun import freeze_time
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_402_PAYMENT_REQUIRED,
    HTTP_403_FORBIDDEN,
)

from baserow.core.models import UserLogEntry


@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_admin_dashboard(api_client, premium_data_fixture):
    with freeze_time("2020-01-01 00:01"):
        normal_user = premium_data_fixture.create_user(
            is_staff=False, has_active_premium_license=True
        )
        admin_user = premium_data_fixture.create_user(
            is_staff=True, has_active_premium_license=True
        )

    with freeze_time("2020-01-01 00:01"):
        normal_token = premium_data_fixture.generate_token(user=normal_user)
        admin_token = premium_data_fixture.generate_token(user=admin_user)

        premium_data_fixture.create_database_application(user=normal_user)
        UserLogEntry.objects.create(actor=admin_user, action="SIGNED_IN")

        response = api_client.get(
            reverse("api:premium:admin:dashboard:dashboard"),
            format="json",
            HTTP_AUTHORIZATION=f"JWT {normal_token}",
        )
        assert response.status_code == HTTP_403_FORBIDDEN

        response = api_client.get(
            reverse("api:premium:admin:dashboard:dashboard"),
            format="json",
            HTTP_AUTHORIZATION=f"JWT {admin_token}",
        )
        assert response.status_code == HTTP_200_OK
        assert response.json() == {
            "total_users": 2,
            "total_workspaces": 1,
            "total_applications": 1,
            "new_users_last_24_hours": 2,
            "new_users_last_7_days": 2,
            "new_users_last_30_days": 2,
            "previous_new_users_last_24_hours": 0,
            "previous_new_users_last_7_days": 0,
            "previous_new_users_last_30_days": 0,
            "active_users_last_24_hours": 1,
            "active_users_last_7_days": 1,
            "active_users_last_30_days": 1,
            "previous_active_users_last_24_hours": 0,
            "previous_active_users_last_7_days": 0,
            "previous_active_users_last_30_days": 0,
            "new_users_per_day": [{"date": "2020-01-01", "count": 2}],
            "active_users_per_day": [{"date": "2020-01-01", "count": 1}],
        }

        url = reverse("api:premium:admin:dashboard:dashboard")
        response = api_client.get(
            f"{url}?timezone=Etc/GMT%2B1",
            format="json",
            HTTP_AUTHORIZATION=f"JWT {admin_token}",
        )
        assert response.status_code == HTTP_200_OK
        assert response.json() == {
            "total_users": 2,
            "total_workspaces": 1,
            "total_applications": 1,
            "new_users_last_24_hours": 2,
            "new_users_last_7_days": 2,
            "new_users_last_30_days": 2,
            "previous_new_users_last_24_hours": 0,
            "previous_new_users_last_7_days": 0,
            "previous_new_users_last_30_days": 0,
            "active_users_last_24_hours": 1,
            "active_users_last_7_days": 1,
            "active_users_last_30_days": 1,
            "previous_active_users_last_24_hours": 0,
            "previous_active_users_last_7_days": 0,
            "previous_active_users_last_30_days": 0,
            "new_users_per_day": [{"date": "2019-12-31", "count": 2}],
            "active_users_per_day": [{"date": "2019-12-31", "count": 1}],
        }

        premium_data_fixture.remove_all_active_premium_licenses(admin_user)
        url = reverse("api:premium:admin:dashboard:dashboard")
        response = api_client.get(
            url,
            format="json",
            HTTP_AUTHORIZATION=f"JWT {admin_token}",
        )
        assert response.status_code == HTTP_402_PAYMENT_REQUIRED
        assert response.json()["error"] == "ERROR_FEATURE_NOT_AVAILABLE"
