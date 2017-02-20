import sys
import datetime
from slackbot.bot import respond_to
sys.path.append('..')
from find_avairable_time import get_available_time
from application.google_calendar import get_upcoming_events

@respond_to('今後の予定を教えて')
def respond_schedule(message):

    calendar_ids = {'塩ホッケ': 'mchmng0grg5vb1q9pdahc2fui4@group.calendar.google.com',
                    '大西': '9hsr2ngo831lbbq5pk52ujcicc@group.calendar.google.com',
                    '耀太': 'sufgin9an1pmqgr6o24dks5q40@group.calendar.google.com'}
    john_events = get_upcoming_events(calendar_id=calendar_ids['塩ホッケ'], max_results=100)
    mary_events = get_upcoming_events(calendar_id=calendar_ids['大西'], max_results=100)
    mike_events = get_upcoming_events(calendar_id=calendar_ids['耀太'], max_results=100)

    from pprint import pprint
    min_time, max_time = datetime.time(9, 0), datetime.time(18, 0)  # search free time between 9 and 18 o'clock.
    pprint(get_available_time(min_time, max_time, john_events, mary_events, mike_events))

    reply_message = str(get_available_time(min_time, max_time, john_events, mary_events, mike_events))
    message.reply(reply_message)