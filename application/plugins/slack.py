import sys
import datetime
from slackbot.bot import respond_to, listen_to
sys.path.append('..')
from application.google_calendar import get_upcoming_events
from find_avairable_time import get_available_time

@listen_to('飲みにいける日')
@listen_to('呑みにいける日')
@listen_to('のみにいける日')
@listen_to('ひまな日')
def respond_schedule(message):

    calendar_ids = {'塩ホッケ': 'mchmng0grg5vb1q9pdahc2fui4@group.calendar.google.com',
                    '大西': '9hsr2ngo831lbbq5pk52ujcicc@group.calendar.google.com',
                    '耀太': 'sufgin9an1pmqgr6o24dks5q40@group.calendar.google.com'}
    john_events = get_upcoming_events(calendar_id=calendar_ids['塩ホッケ'], max_results=100)
    mary_events = get_upcoming_events(calendar_id=calendar_ids['大西'], max_results=100)
    mike_events = get_upcoming_events(calendar_id=calendar_ids['耀太'], max_results=100)

    from pprint import pprint
    min_time, max_time = datetime.time(18, 0), datetime.time(21, 0)
    intervals = get_available_time(min_time, max_time, john_events, mary_events, mike_events)
    free_list = []

    for date in sorted(intervals.keys()):
        for pair in intervals[date]:
            start,end = pair
            start_str = start.strftime('%m/%d %H:%M')
            end_str = end.strftime('%m/%d %H:%M')
            text = '\r\n' + start_str + " ～ " + end_str
            free_list.append(text)

    reply_schedule = ' '.join(free_list)
    reply_message = '\r\n' + "3人の都合が合う日はこれです" + reply_schedule
    message.reply(reply_message)

@respond_to('おススメのお店')
@respond_to('お勧めのお店')
@respond_to('おススメの店')
@respond_to('お勧めの店')
def respond_bar(message):
    reply_message2 = "日本酒好きが多いですね" + "\r\n" + "ここがおススメですよ" + "\r\n" + "https://tabelog.com/osaka/A2701/A270101/27080955/"
    message.reply(reply_message2)

@respond_to('他のお店')
@respond_to('他の店')
def respond_bar2(message):
    reply_message3 = "たまにはピザなんてどうですか？" + "\r\n" + "ここもおススメですよ" + "\r\n" + "https://tabelog.com/osaka/A2701/A270101/27092761/"
    message.reply(reply_message3)