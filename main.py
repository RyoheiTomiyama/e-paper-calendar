#!/usr/bin/env python

from waveshare import output_epaper
from draw import Draw
from google_calendar import GoogleCalendar

def main():
    google_calendar = GoogleCalendar()
    events = google_calendar.get_events()

    draw = Draw()
    draw.draw_separate_line()
    draw.draw_monthly_calendar()
    draw.draw_schedules(events)
    draw.draw_today()
    draw.draw_weather()
    # draw.save_image()
    output_epaper(draw.img, draw.img_red)


if __name__ == '__main__':
    main()