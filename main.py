#!/usr/bin/env python

from draw import Draw
from google_calendar import GoogleCalendar

def main():
    google_calendar = GoogleCalendar()
    events = google_calendar.get_events()

    draw = Draw()
    draw.draw_separate_line()
    draw.draw_monthly_calendar()
    draw.draw_schedules(events)
    draw.save_image()


if __name__ == '__main__':
    main()