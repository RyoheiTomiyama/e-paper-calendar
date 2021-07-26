import pytz
import calendar as cal
from datetime import date, datetime
from dateutil.parser import parse
from typing import List, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont

Width, Height = int, int

# image size
SIZE = (800, 480)
MAIN_WIDTH = 560

FONTS = dict(
    en='./Fonts/Marcellus-Regular.ttf',
    ja='./Fonts/NotoSansJP-Bold.otf',
    num='./Fonts/Cardo-Regular.ttf',
    title='./Fonts/PinyonScript-Regular.ttf',
    number='./Fonts/Krungthep.ttf',
)

# color scale
COLORS = dict(
    black=(0, 0, 0),
    red=(255, 0, 0),
    white=(255, 255, 255)
)

LOCALE = 'Asia/Tokyo'

WEEKDAY = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

def get_calendar(year: int, month: int):
    month_dates = cal.Calendar(cal.SUNDAY).monthdatescalendar(year, month)
    return month_dates

class Draw:
    # EPDで描画するときに、黒と赤を別画像から描画するので、2色の画像を用意する
    # def display(self, imageblack, imagered):
    img_black: Image.Image
    img_red: Image.Image
    draw_black: ImageDraw.ImageDraw
    draw_red: ImageDraw.ImageDraw
    today: date

    def __init__(self):
        # create a new image
        self.img_black = Image.new('RGB', SIZE, COLORS['white'])
        self.img_red = Image.new('RGB', SIZE, COLORS['white'])
        self.draw_black = ImageDraw.Draw(self.img_black)
        self.draw_red = ImageDraw.Draw(self.img_red)
        self.today = date.today()

    def get_font(self, name: str, size: int):
        return ImageFont.truetype(FONTS[name], size)

    def get_rect(self, text: str, font_name: str, font_size: int) -> Tuple[Width, Height]:
        bbox = self.draw_black.multiline_textbbox(
            (0, 0), text,  
            font = self.get_font(font_name, font_size)
        )
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
    # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.textsize
    def get_textsize(self, text: str, font_name: str, font_size: int) -> Tuple[Width, Height]:
        textsize = self.draw_black.multiline_textsize(
            text,
            font = self.get_font(font_name, font_size)
        )
        width = textsize[0]
        height = textsize[1]
        return width, height

    def padding_width(self, width: int, text: str, font_name: str, font_size: int):
        rect = self.get_rect(text, font_name, font_size)
        return (width - rect[0]) // 2

    def padding_height(self, height: int, text: str, font_name: str, font_size: int):
        rect = self.get_rect(text, font_name, font_size)
        textsize = self.get_textsize(text, font_name, font_size)
        return (height - rect[1] + textsize[1]) // 2

    def save_image(self, file_name: str = 'text'):
        saved_image = Image.new('RGB', SIZE, COLORS['white'])
        for x in range(SIZE[0]):
            for y in range(SIZE[1]):
                pixel_black = self.img_black.getpixel((x, y))
                pixel_red = self.img_red.getpixel((x, y))
                if pixel_black[0] != 255 or pixel_black[1] != 255 or pixel_black[2] != 255:
                    saved_image.putpixel((x, y), pixel_black)
                if pixel_red[0] != 255 or pixel_red[1] != 255 or pixel_red[2] != 255:
                    saved_image.putpixel((x, y), pixel_red)
        file_path = f'./{file_name}.bmp'
        saved_image.save(file_path, 'bmp')
    
    def convert_multiline_text(self, text: str, font_name: str, font_size: int, width):
        lines: List[str] = []
        line_text = ''
        for i, t in enumerate(text):
            rect = self.get_rect(
                line_text + t,
                font_name,
                font_size
            )
            if rect[0] > width:
                lines.append(line_text)
                line_text = t
            else:
                line_text = line_text + t
            if len(text) == i + 1:
                lines.append(line_text)
        return lines

    def draw_monthly_calendar(self):
        if not self.draw_black or not self.draw_red:
            return
        calendar = get_calendar(self.today.year, self.today.month)
        # calendar = get_calendar(2018, 12)

        month_size = 12
        month_padding = self.padding_width(SIZE[0] - MAIN_WIDTH, self.today.strftime("%B"), 'number', month_size)
        self.draw_black.multiline_text(
            (MAIN_WIDTH + month_padding, 32 + 30 * 7),
            self.today.strftime("%B"),
            fill = COLORS['black'],
            font = self.get_font('number', month_size),
        )
        month_size = 20
        month_padding = self.padding_width(SIZE[0] - MAIN_WIDTH, str(self.today.month), 'number', month_size)
        self.draw_black.multiline_text(
            (MAIN_WIDTH + month_padding, 12 + 30 * 7),
            str(self.today.month),
            fill = COLORS['black'],
            font = self.get_font('number', month_size),
        )

        w_day = (SIZE[0] - MAIN_WIDTH) // 7
        x_start: np.ndarray = np.arange(7) * w_day + MAIN_WIDTH
        weekday_s = ['S', 'M', 'T', 'W', 'T', 'F', 'S']

        for i, text in enumerate(weekday_s):
            w_pad = self.padding_width(w_day, text, 'number', 12)
            color = COLORS['red'] if i == 0 else COLORS['black']
            draw = self.draw_red if i == 0 else self.draw_black
            draw.multiline_text(
                (x_start[i] + w_pad, 270),
                text,
                font = self.get_font('number', 12),
                fill = color,
            )

        # show the dates
        for h, row in enumerate(calendar):
            for i, d in enumerate(row):
                text = d.day
                if text == 0:
                    continue
                w_pad = self.padding_width(w_day, str(text), 'number', 16)
                color = COLORS['black']
                draw = self.draw_black
                if i == 0:
                    color = COLORS['red']
                    draw = self.draw_red
                if d.month is not self.today.month:
                    color = (160, 160, 160) 
                    draw = self.draw_black
                # color = COLOR['red'] if i == 0 or text in holidays else COLOR['black']
                draw.multiline_text(
                    (x_start[i] + w_pad, 300 + 30 * h),
                    str(text),
                    font = self.get_font('number', 16),
                    fill = color
                )

    def draw_schedules(self, schedules):
        h_schedule = (SIZE[1] - 20) // 10
        font_size = 15
        for i, schedule in enumerate(schedules):
            s_name: str = schedule['name']
            s_datetime: datetime = schedule['datetime']
            s_datetime = s_datetime.astimezone(pytz.timezone(LOCALE))
            if s_name is None or s_datetime is None:
                continue
            
            # draw date
            # if i > 0:
            prev_schedule_datetime: datetime = schedules[i - 1]['datetime']
            is_same_date = s_datetime.strftime('%m/%d') == prev_schedule_datetime.astimezone(pytz.timezone(LOCALE)).strftime('%m/%d')
            if not is_same_date:
                s_date = s_datetime.strftime('%m/%d')
                h_pad = self.padding_height(h_schedule, s_date, 'number', font_size)
                self.draw_black.multiline_text(
                    (10, 10 + h_pad + (h_schedule * i) + 1),
                    s_date,
                    font = self.get_font('number', font_size),
                    anchor = 'lm',
                    fill = COLORS['black']
                )

            # draw time
            s_time = s_datetime.strftime('%H:%M')
            h_pad = self.padding_height(h_schedule, s_time, 'number', font_size)
            rect = self.get_rect(s_time, 'number', font_size)
            self.draw_black.multiline_text(
                (70, 10 + h_pad + (h_schedule * i)),
                s_time,
                font = self.get_font('number', font_size),
                anchor = 'lm',
                fill = COLORS['black'],
            )

            # draw line for date
            line_start = 10 + (h_pad // 2) + (h_schedule * i)
            line_end = line_start + rect[1] + (h_pad // 2)
            if is_same_date:
                line_start = line_start - (h_schedule // 2)
            self.draw_black.line(
                ((126, line_start), (126, line_end)),
                fill = COLORS['black'],
                width = 1,
            )

            # draw schedule title
            lines = self.convert_multiline_text(s_name, 'ja', font_size, MAIN_WIDTH - 120)
            text = str('\n'.join(lines[:3]))
            h_pad = self.padding_height(h_schedule, text, 'ja', font_size)
            self.draw_black.multiline_text(
                (140, 10 + h_pad + (h_schedule * i)),
                text,
                font = self.get_font('ja', font_size),
                anchor = 'lm',
                fill = COLORS['black']
            )

    def draw_separate_line(self):
        self.draw_black.line(
            ((MAIN_WIDTH, 0), (MAIN_WIDTH, SIZE[1])),
            fill = COLORS['black'],
            width = 1,
        )
        self.draw_black.line(
            ((MAIN_WIDTH + 2, 0), (MAIN_WIDTH + 2, SIZE[1])),
            fill = COLORS['black'],
            width = 1,
        )
        self.draw_black.line(
            ((MAIN_WIDTH, 6 + 30 * 7), (SIZE[0], 6 + 30 * 7)),
            fill = COLORS['black'],
            width = 1,
        )
        self.draw_black.line(
            ((MAIN_WIDTH, 8 + 30 * 7), (SIZE[0], 8 + 30 * 7)),
            fill = COLORS['black'],
            width = 1,
        )
