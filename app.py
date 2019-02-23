import requests
import sys

from time import sleep
from datetime import datetime

HTTP_SUCCESS = 200
SLEEP_TIME = 5
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60

# Check proper usage
if len(sys.argv) != 2:
    print('Usage: python app.py N, where N is a UNIX timestamp value for HardFork time')
    sys.exit(1)

# Get the timestamp
try:
    timestamp = datetime.utcfromtimestamp(int(sys.argv[1]))
except ValueError:
    print('Usage: python app.py N, where N is a UNIX timestamp value for HardFork time')
    sys.exit(1)

while True:
    try:
        response = requests.get('https://api.blockchair.com/bitcoin-cash/blocks?limit=1&s=median_time(desc)')
    except requests.exceptions.ConnectionError:
        print('Service not available')
        sleep(SLEEP_TIME)
        continue
    response_data = response.json()
    if response.status_code == HTTP_SUCCESS:
        median_time = datetime.strptime(response_data.get('data')[0].get('median_time'), '%Y-%m-%d %H:%M:%S')
        if median_time >= timestamp:
            print('HardFork happened!')
            sys.exit(0)
        else:
            dt = timestamp - median_time
            days = '{} day(s) '.format(dt.days) if dt.days > 0 else ''
            hours = '{} hour(s) '.format(dt.seconds // SECONDS_IN_HOUR) if dt.seconds // SECONDS_IN_HOUR > 0 else ''
            minutes = '{} minute(s) '.format(dt.seconds % SECONDS_IN_HOUR // SECONDS_IN_MINUTE) \
                if dt.seconds % SECONDS_IN_HOUR // SECONDS_IN_MINUTE > 0 else ''
            seconds = '{} second(s)'.format(dt.seconds % SECONDS_IN_HOUR % SECONDS_IN_MINUTE) \
                if dt.seconds % SECONDS_IN_HOUR % SECONDS_IN_MINUTE > 0 else ''
            print('HardFork will happen in {}{}{}{}'.format(days, hours, minutes, seconds))
    else:
        error = response_data.get('context').get('error')
        if error:
            print(error)
        else:
            print('Service not available')
    sleep(SLEEP_TIME)
