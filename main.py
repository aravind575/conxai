from fastapi import FastAPI
from fastapi.testclient import TestClient
from random import randint
import uvicorn
from datetime import datetime, timedelta


# App setup
app = FastAPI()
client = TestClient(app)


# Storing OTP data persistently between requests
class OtpData():
    __otpdata = ''
    __otpExpiry = datetime.now()

    @classmethod
    def getOtp(self):
        return self.__otpdata

    @classmethod
    def setOtp(self, otp: str):
        self.__otpdata = otp
        self.__otpExpiry = datetime.now() + timedelta(minutes=3)
        return self.__otpdata

    @classmethod
    def verifyOtp(self, otp: str):
        if otp == self.__otpdata:
            if datetime.now() > self.__otpExpiry:
                return 'Otp has expired! Please generate a new otp.'
            else:
                return 'Otp verified successfully!'
        return 'Wrong otp! Please try again!'


# Function to generate otp
def generate():
    otp = ''

    for i in range(6):
        x = str(randint(0, 9))
        otp += x
    
    return otp


# APIs
@app.get('/generate_otp')
async def generateOtp():
    otp = generate()
    return f"Otp is {OtpData.setOtp(otp)}, valid for 3 minutes."


@app.get('/verify_otp/{otp}')
async def verifyOtp(otp: str):
    return OtpData.verifyOtp(otp)


############ MAIN FUNCTION ############ MAIN FUNCTION ###########
if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8009)