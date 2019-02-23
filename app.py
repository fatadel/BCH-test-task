import requests
import sys
import constants

from time import sleep
from datetime import datetime

# Check proper usage
if len(sys.argv) != 2:
    print(constants.errors['usage_error'])
    sys.exit(1)

# Get the timestamp
# Covert it from UNIX timestamp to UTC datetime object
try:
    timestamp = datetime.utcfromtimestamp(int(sys.argv[1]))
except ValueError:
    print(constants.errors['usage_error'])
    sys.exit(1)

while True:
    # Get the most recent MTP-11
    try:
        response = requests.get('https://api.blockchair.com/bitcoin-cash/blocks?limit=1&s=median_time(desc)')
    except requests.exceptions.ConnectionError:
        print(constants.errors['service_error'])
        sleep(constants.SLEEP_TIME)
        continue

    # Decode response
    response_data = response.json()

    if response.status_code == requests.codes.ok:
        # Convert string-formatted datetime to UTC datetime object
        median_time = datetime.strptime(response_data.get('data')[0].get('median_time'), '%Y-%m-%d %H:%M:%S')

        if median_time >= timestamp:
            print('HardFork happened!')
            sys.exit(0)
        else:
            # Calculate time to HardFork
            dt = timestamp - median_time
            days = '{} day(s) '.format(dt.days) if dt.days > 0 else ''
            hours = dt.seconds // constants.SECONDS_IN_HOUR
            hours = '{} hour(s) '.format(hours) if hours > 0 else ''
            minutes = dt.seconds % constants.SECONDS_IN_HOUR // constants.SECONDS_IN_MINUTE
            minutes = '{} minute(s) '.format(minutes) if minutes > 0 else ''
            seconds = dt.seconds % constants.SECONDS_IN_HOUR % constants.SECONDS_IN_MINUTE
            seconds = '{} second(s)'.format(seconds) if seconds > 0 else ''

            print('HardFork will happen in {}{}{}{}'.format(days, hours, minutes, seconds))
    else:
        error = response_data.get('context').get('error')
        if error:
            print(error)
        else:
            print(constants.errors['service_error'])

    # Sleep SLEEP_TIME seconds until next try
    sleep(constants.SLEEP_TIME)
