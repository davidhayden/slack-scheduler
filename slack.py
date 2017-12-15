"""
A Python 3.6 script that sends a message to a Slack
Channel using Incoming WebHooks. The script uses
APScheduler to schedule the message and requests
to post the message to the Slack Channel.

The script uses 1 environment variable that holds the
Incoming Webhooks URL:

    slackIncomingWebhookUrl

Specify the channel and text for the message in the
send_message() function. The channel is optional if
you wish to use the default channel specfied when
creating the Incoming Webhook.

    message = {
        "channel": "#general",
        "text": "A message."
    }

Choose the interval or date and time you wish to
send the message.

    @sched.scheduled_job('interval', minutes=1)

APScheduler is quite flexible so you may want to
read its documentation to understand the various
ways to schedule a job.abs

    http://apscheduler.readthedocs.io/en/latest/
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import datetime, os, requests


slack_url = os.getenv('slackIncomingWebhookUrl')
sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def send_message():
    message = {
        "channel": "#general",
        "text": "A message."
    }

    results = requests.post(slack_url, json = message)

    response = {
        'date': str(datetime.datetime.now()),
        'message': message,
        'statusCode': results.status_code
    }

    return response


def event_listener(event):
    print(event.retval)


print("Running...")
sched.add_listener(event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
sched.start()
