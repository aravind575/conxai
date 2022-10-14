from fastapi.testclient import TestClient

from main import app
from main import OtpData

client = TestClient(app)


############ TESTS ############ TESTS ###########
def test_otp_generator():
    response = client.get("/generate_otp")
    assert response.status_code == 200
    assert response.json() == f'Otp is {OtpData.getOtp()}, valid for 3 minutes.'


def test_otp_verify():
    otp = OtpData.getOtp()
    response = client.get(f"/verify_otp/{otp}")
    assert response.status_code == 200
    assert response.json() == f'Otp verified successfully!'


def test_wrong_otp_verify():
    otp = OtpData.getOtp()
    otp = otp[:-2]
    response = client.get(f"/verify_otp/{otp}")
    assert response.status_code == 200
    assert response.json() == f'Wrong otp! Please try again!'