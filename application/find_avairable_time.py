import datetime
from collections import defaultdict

import dateutil.parser
from application.google_calendar import get_upcoming_events


def extract_intervals(events_list):
    intervals = defaultdict(list)
    for events in events_list:
        for event in events:
            # Extract start and end time
            start_datetime_str = event['start'].get('dateTime', event['start'].get('date'))
            end_datetime_str = event['end'].get('dateTime', event['end'].get('date'))

            # Convert datetime str to datetime
            s_datetime = dateutil.parser.parse(start_datetime_str)
            e_datetime = dateutil.parser.parse(end_datetime_str)
            interval = (s_datetime, e_datetime)

            date = datetime.date(s_datetime.year, s_datetime.month, s_datetime.day)
            intervals[date].append(interval)

    return intervals


def add_sentinels(intervals, min_time, max_time):
    for date in intervals.keys():
        tzinfo = intervals[date][0][0].tzinfo
        s_datetime = datetime.datetime.combine(date, datetime.time.min.replace(tzinfo=tzinfo))
        e_datetime = datetime.datetime.combine(date, min_time.replace(tzinfo=tzinfo))
        intervals[date].append((s_datetime, e_datetime))
        s_datetime = datetime.datetime.combine(date, max_time.replace(tzinfo=tzinfo))
        e_datetime = datetime.datetime.combine(date, datetime.time.max.replace(tzinfo=tzinfo))
        intervals[date].append((s_datetime, e_datetime))
    return intervals


def sort_intervals(intervals):
    for date in intervals.keys():
        intervals[date].sort()
    return intervals


def find_free_intervals(intervals):
    free_intervals = defaultdict(list)
    for date, ivals in intervals.items():
        max_time = ivals[0][1]
        for i in range(len(ivals) - 1):
            first, second = ivals[i], ivals[i+1]
            max_time = max(max_time, first[1])
            if max_time >= second[0]:
                continue
            free_interval = (max_time, second[0])
            free_intervals[date].append(free_interval)
    return free_intervals


def get_available_time(min_time, max_time, *events_list):
    intervals = extract_intervals(events_list)
    intervals = add_sentinels(intervals, min_time, max_time)
    intervals = sort_intervals(intervals)
    intervals = find_free_intervals(intervals)
    return intervals


if __name__ == '__main__':
    calendar_ids = {'塩ホッケ': 'mchmng0grg5vb1q9pdahc2fui4@group.calendar.google.com',
                    '大西': '9hsr2ngo831lbbq5pk52ujcicc@group.calendar.google.com',
                    '耀太': 'sufgin9an1pmqgr6o24dks5q40@group.calendar.google.com'}
    john_events = get_upcoming_events(calendar_id=calendar_ids['塩ホッケ'], max_results=100)
    mary_events = get_upcoming_events(calendar_id=calendar_ids['大西'], max_results=100)
    mike_events = get_upcoming_events(calendar_id=calendar_ids['耀太'], max_results=100)

    from pprint import pprint
    min_time, max_time = datetime.time(9, 0), datetime.time(18, 0)  # search free time between 9 and 18 o'clock.
    pprint(get_available_time(min_time, max_time, john_events, mary_events, mike_events))


    intervals = get_available_time(min_time, max_time, john_events, mary_events, mike_events)
    free_list = []
    pprint(intervals[datetime.date(2017, 3, 1)])
    #d.strftime(%m/%d/%H:%M)
    for date in sorted(intervals.keys()):
        for pair in intervals[date]:
            start,end = pair
            start_str = start.strftime('%m/%d %H:%M')
            end_str = end.strftime('%m/%d %H:%M')
            text = start_str + " ～ " + end_str
            free_list.append(text)

    pprint('\r\n'.join(free_list))

