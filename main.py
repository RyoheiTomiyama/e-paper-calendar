#!/usr/bin/env python

from google_calendar import GoogleCalendar

def main():
    google_calendar = GoogleCalendar()
    google_calendar.get_events()

if __name__ == '__main__':
    main()