import json
import logging
import os
import pytest

from unifiapipy import Unifi


UNIFI_API_BASE_URL = os.getenv("UNIFI_API_BASE_URL")
UNIFI_API_USER = os.getenv("UNIFI_API_USERNAME")
UNIFI_API_PASSWORD = os.getenv("UNIFI_API_PASSWORD")
BOTO3_ENDPOINT_URL = os.getenv("BOTO3_ENDPOINT_URL")
BOTO3_ACCESS_KEY = os.getenv("BOTO3_ACCESS_KEY")
BOTO3_SECRET_KEY = os.getenv("BOTO3_SECRET_KEY")
BOTO3_BUCKET = os.getenv("BOTO3_BUCKET")


@pytest.fixture
def unifi_instance():
    u = Unifi(
        UNIFI_API_BASE_URL,
        UNIFI_API_USER,
        UNIFI_API_PASSWORD,
        BOTO3_ENDPOINT_URL,
        BOTO3_ACCESS_KEY,
        BOTO3_SECRET_KEY,
        BOTO3_BUCKET,
    )
    return u


@pytest.fixture
def MockResponse(mocker):
    resp = mocker.MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"data": {"a": 1}}
    return resp


# ============================
# ===== Functional tests =====
def test_login(unifi_instance):
    unifi_instance.login()
    # TODO actually test that it worked?


def test_collection_stat_hourly_site(unifi_instance):
    unifi_instance.login()
    devices = unifi_instance.fetch_collection("stat_hourly_site")
    # Uncomment below to dump response.
    # with open("get_devices.json", "w") as f:
    #     json.dump(devices, f)
    assert isinstance(devices, list)
    assert isinstance(devices[0], dict)
    assert "wlan_bytes" in devices[0]
    assert "num_sta" in devices[0]
    assert "oid" in devices[0]
    assert "o" in devices[0]


def test_fetch_and_upload_collection(unifi_instance):
    unifi_instance.login()
    unifi_instance.fetch_and_upload_collection("list_clients")
    # import pdb; pdb.set_trace()


# ============================
# ===== Unit tests ===========
def test_unit_login_unifi(unifi_instance, mocker, MockResponse):

    m = mocker.patch("requests.Session.post", return_value=MockResponse)
    loginresp = unifi_instance.login_unifi_api("a", "b")
    m.assert_any_call(
        unifi_instance.BASE_URL + unifi_instance.URL_PATHS["login"],
        json={"username": "a", "password": "b"},
    )
    m.assert_any_call(
        unifi_instance.BASE_URL + "/ajax/update_controller.php",
        data={"new_controller_idx": 1},
    )


def test_unit_fetch_and_upload_collection(unifi_instance, mocker, MockResponse):
    mock_boto = mocker.patch("unifiapipy.Unifi.login_boto3")
    mock_post = mocker.patch("requests.Session.post", return_value=MockResponse)

    unifi_instance.login()
    unifi_instance.fetch_and_upload_collection("count_alarms")

    assert len(mock_boto.mock_calls[-1].args) == 3
    assert mock_boto.mock_calls[-1].args[1] == unifi_instance.BOTO3_BUCKET
