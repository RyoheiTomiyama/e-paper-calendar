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
    ja='./Fonts/NotoSansJP-Regular.otf',
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

def get_calendar(year: int, month: int):
    month_dates = cal.Calendar(cal.SUNDAY).monthdatescalendar(year, month)
    return month_dates
    # calendar_eu = cal.monthcalendar(year, month)
    # print(calendar_eu)
    # # print(cal.prmonth(year, month))
    # formatted = [0]+list(itertools.chain.from_iterable(calendar_eu))[:-1]
    # print(np.array(formatted).reshape(-1, 7).tolist())
    # return np.array(formatted).reshape(-1, 7).tolist()

class Draw:
    img: Image.Image
    draw: ImageDraw.ImageDraw
    today: date

    def __init__(self):
        # create a new image
        self.img = Image.new('RGB', SIZE, COLORS['white'])
        self.draw = ImageDraw.Draw(self.img)
        self.today = date.today()

    def get_font(self, name: str, size: int):
        self.img
        return ImageFont.truetype(FONTS[name], size)

    def get_rect(self, text: str, font_name: str, font_size: int) -> Tuple[Width, Height]:
        bbox = self.draw.multiline_textbbox(
            (0, 0), text,  
            font = self.get_font(font_name, font_size)
        )
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return (width, height)

    def padding_width(self, width: int, text: str, font_name: str, font_size: int):
        rect = self.get_rect(text, font_name, font_size)
        return (width - rect[0]) // 2

    def padding_height(self, height: int, text: str, font_name: str, font_size: int):
        rect = self.get_rect(text, font_name, font_size)
        return (height - rect[1]) // 2

    def save_image(self, file_name: str = 'text'):
        file_path = f'./{file_name}.bmp'
        self.img.save(file_path, 'bmp')
    
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
        if not self.draw:
            return
        calendar = get_calendar(self.today.year, self.today.month)
        # calendar = get_calendar(2018, 12)

        month_size = 12
        month_padding = self.padding_width(SIZE[0] - MAIN_WIDTH, self.today.strftime("%B"), 'number', month_size)
        self.draw.multiline_text(
            (MAIN_WIDTH + month_padding, 32 + 30 * 7),
            self.today.strftime("%B"),
            fill = COLORS['black'],
            font = self.get_font('number', month_size),
        )
        month_size = 20
        month_padding = self.padding_width(SIZE[0] - MAIN_WIDTH, str(self.today.month), 'number', month_size)
        self.draw.multiline_text(
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
            self.draw.multiline_text(
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
                if i == 0:
                    color = COLORS['red']
                if d.month is not self.today.month:
                    color = (160, 160, 160) 
                # color = COLOR['red'] if i == 0 or text in holidays else COLOR['black']
                self.draw.multiline_text(
                    (x_start[i] + w_pad, 300 + 30 * h),
                    str(text),
                    font = self.get_font('number', 16),
                    fill = color
                )

    def draw_schedules(self, schedules):
        h_schedule = (SIZE[1] - 20) // 10
        print(h_schedule)
        for i, schedule in enumerate(schedules):
            s_name: str = schedule['summary']
            s_datetime: datetime = parse(schedule['start'].get('dateTime', schedule['start'].get('date')))
            if s_name is None or s_datetime is None:
                continue
            s_date = s_datetime.strftime('%m/%d')
            h_pad = self.padding_height(h_schedule, s_date, 'number', 16)
            self.draw.multiline_text(
                (10, 10 + h_pad + (h_schedule * i) + 1),
                s_date,
                font = self.get_font('number', 16),
                fill = COLORS['black']
            )
            s_time = s_datetime.strftime('%H:%M')
            h_pad = self.padding_height(h_schedule, s_time, 'number', 16)
            self.draw.multiline_text(
                (70, 10 + h_pad + (h_schedule * i)),
                s_time,
                font = self.get_font('number', 16),
                fill = COLORS['black']
            )
            lines = self.convert_multiline_text(s_name, 'ja', 16, MAIN_WIDTH - 120)
            text = str('\n'.join(lines[:3]))
            h_pad = self.padding_height(h_schedule, text, 'ja', 16)
            self.draw.multiline_text(
                (130, 10 + h_pad + (h_schedule * i)),
                text,
                font = self.get_font('ja', 16),
                fill = COLORS['black']
            )
            
        


    def draw_separate_line(self):
        self.draw.line(
            ((MAIN_WIDTH, 0), (MAIN_WIDTH, SIZE[1])),
            fill = COLORS['black'],
            width = 1,
        )
        self.draw.line(
            ((MAIN_WIDTH + 2, 0), (MAIN_WIDTH + 2, SIZE[1])),
            fill = COLORS['black'],
            width = 1,
        )
        self.draw.line(
            ((MAIN_WIDTH, 6 + 30 * 7), (SIZE[0], 6 + 30 * 7)),
            fill = COLORS['black'],
            width = 1,
        )
        self.draw.line(
            ((MAIN_WIDTH, 8 + 30 * 7), (SIZE[0], 8 + 30 * 7)),
            fill = COLORS['black'],
            width = 1,
        )
