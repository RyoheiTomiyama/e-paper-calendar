#!/usr/bin/env python

from weather import Weather
from draw import Draw
from google_calendar import GoogleCalendar

# 開発中に画像を書き出してテストしたいときは、コメントアウトを外す
# IS_LOCAL = True

def main():
    google_calendar = GoogleCalendar()
    events = google_calendar.get_events()

    weather = Weather()
    weather.get_weather()

    draw = Draw()
    draw.draw_separate_line()
    draw.draw_monthly_calendar()
    draw.draw_schedules(events)
    draw.draw_today()
    draw.draw_weather(weather)

    if 'IS_LOCAL' in globals():
        draw.save_image()
    else:
        from waveshare import output_epaper
        output_epaper(draw.img_black, draw.img_red)


if __name__ == '__main__':
    main()
