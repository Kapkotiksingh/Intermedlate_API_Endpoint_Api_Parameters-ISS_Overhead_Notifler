import time

import requests
from datetime import datetime
import smtplib

MY_EMAIL = "Your Email"
PASSWORD = "Your Password"


MY_LAT = 51.507351 # Your Latitude
MY_LONG = -0.127758 # Your Longitude

def is_iss_overhead():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    # # if response.status_code != 200:
    # #     raise Exception("Bed response from ISS API ")
    # #
    # # if response.status_code == 400:
    # #     raise Exception("That resource does not exist")
    # #
    # # elif response.status_code == 401:
    # #     raise Exception("You are not authorised to access this data")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG-5:
        return True


# is_position = (longitude, latitude)
# print(is_position)

def is_night():
    parameter = {
        "lat" : MY_LAT,
        "lng" : MY_LONG,
        "formatted" : 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", parans = parameter)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["result"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True :
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:look Up\n\nThe ISS is above you in the sky"
        )