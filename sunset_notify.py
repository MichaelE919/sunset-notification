import os
import sched
import time as tm
from datetime import date, datetime, time, timedelta

import requests

from bs4 import BeautifulSoup
from twilio.rest import Client

loc = '30.578806,-97.853065'
url = f'https://darksky.net/forecast/{loc}/us12/en'

sun_page = requests.get(url)
sun = sun_page.content

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

scheduler = sched.scheduler(tm.time, tm.sleep)
client = Client(account_sid, auth_token)

soup = BeautifulSoup(sun, 'html.parser')

sun_today = soup.find('span', {'class': 'sunset swap'})

now = datetime.now()

year = now.year
month = now.month
day = now.day
hour = int(str(sun_today.contents[3])[-13:-12])
mins = int(str(sun_today.contents[3])[-11:-9])

sunset_time = time(hour=hour+12, minute=mins)

delta = timedelta(hours=5, minutes=55)

msg_time = (datetime.combine(date(year, month, day), sunset_time) + delta).timestamp()

str_time = sunset_time.strftime('%I:%M %p').lstrip('0')

def send_sms(time):
    message = client.messages.create(
        to='+15129836197', from_='+18328955418', body=f'Turn on the lights at {time}'
    )
    return message


scheduler.enterabs(msg_time, 1, send_sms, (str_time,))

scheduler.run()