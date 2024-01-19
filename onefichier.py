import os
from constants import *
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import csv
from random import randint
import glob
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

title_font_size = 60
title_top_margin = 130
title_font_cut = 30
post_font_size = 40
rectangle_color_1 = '#f6dcd3'
rectangle_color_2 = '#d8e8ce'
rectangle_radius = 30
ellipse_color_1 = '#d8e8ce'
ellipse_color_2 = '#f6dcd3'
bottom_section = True
bottom_text = '🔥 All-in-one Solution In The Link ➡️ 🔥'


def check_csv_delimiter(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()

        if ',' in first_line:
            return ','
        elif ';' in first_line:
            return ';'
        else:
            return ','


def open_data(folder_name):
    file_path = READY / folder_name / 'data.csv'
    delimiter = check_csv_delimiter(file_path)

    with open(file_path, "r", newline="") as data:
        heading = next(data)
        reader = csv.reader(data, delimiter=delimiter)

        for row in reader:
            create_image(row, folder_name)


def get_font(font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)

    return font


def create_image(row, folder_name):
    font_title_path = READY / folder_name / 'assets' / 'fonts' / 'title_font.ttf'
    font_post_path = READY / folder_name / 'assets' / 'fonts' / 'post_font.otf'

    font_title = ImageFont.truetype(str(font_title_path))
    font_post = ImageFont.truetype(str(font_post_path))

    im = Image.new('RGBA', (1000, 1500))
    width, height = im.size

    images_path = READY / folder_name / 'assets' / 'bg' / '*.png'
    images = glob.glob(str(images_path))

    img = images[randint(0, len(images) - 1)]

    img_open = Image.open(img)

    im.paste(img_open, (0, 0))

    board_name = row[0]

    row.remove(row[0])

    if 'black' in img:
        title_color = 'black'
    else:
        title_color = 'white'

    draw = ImageDraw.Draw(im)

    if ':' in row[0]:
        parts = row[0].split(':')

        draw.text((width / 2, title_top_margin - 15), f'{parts[0].upper()}:',
                  anchor="mb", align='center',
                  font=get_font(font_title.path, title_font_size),
                  fill=title_color)

        title_split = parts[1].split()

        new_title = ''
        title_count = 0

        for i in title_split:
            if len(new_title) < title_count:
                new_title += f' {i}'
            else:
                new_title += f'\n{i}'
                title_count += title_font_cut

        new_title = new_title.strip().upper()

        draw.text((width / 2, title_top_margin - 15), new_title,
                  anchor="ma", align='center',
                  font=get_font(font_title.path, title_font_size),
                  fill=title_color)

    else:
        title_split = row[0].split()

        new_title = ''
        title_count = 0

        for i in title_split:
            if len(new_title) < title_count:
                new_title += f' {i}'
            else:
                new_title += f'\n{i}'
                title_count += title_font_cut

        new_title = new_title.strip().upper()

        draw.text((width / 2, title_top_margin), new_title,
                  anchor="mm", align='center',
                  font=get_font(font_title.path, title_font_size),
                  fill=title_color)

    tips_number = 0
    from_top_counter = 370

    for i in row[1:]:
        split = i.split(' ')
        new_string = ''

        count = 0

        for e in split:
            if len(new_string) < count:
                new_string += f' {e}'
            else:
                new_string += f'\n{e}'
                count += 35

        tips = new_string.strip()

        size_multiline = get_font(font_post.path, post_font_size).getsize_multiline(tips)

        offset_w = (width - size_multiline[0]) // 2
        offset_h = (height - size_multiline[1]) // 2
        padding_lr = 30
        padding_tb = 30

        shape = (
            offset_w - padding_lr, (from_top_counter - 35) - padding_tb, offset_w + size_multiline[0] + padding_lr,
            (from_top_counter - 35) + size_multiline[1] + padding_tb)

        if tips_number % 2 == 0:
            rectangle_color = rectangle_color_1
        else:
            rectangle_color = rectangle_color_2

        img1 = ImageDraw.Draw(im)

        img1.rounded_rectangle(shape, fill=rectangle_color, radius=rectangle_radius)

        ellipse_x = offset_w - 100
        ellipse_x_right = shape[2] - 30
        ellipse_y = (from_top_counter - 35) - 70

        if tips_number % 2 == 0:
            img1.ellipse((ellipse_x, ellipse_y, ellipse_x + 100, ellipse_y + 100), fill=ellipse_color_1)
            draw.text((ellipse_x + 50, ellipse_y + 35), str(tips_number + 1),
                      font=get_font(font_post.path, 50), align='center',
                      anchor="mt", fill='black')
        else:
            img1.ellipse((ellipse_x_right, ellipse_y, ellipse_x_right + 100, ellipse_y + 100), fill=ellipse_color_2)
            draw.text((ellipse_x_right + 50, ellipse_y + 35), str(tips_number + 1),
                      font=get_font(font_post.path, 50), align='center',
                      anchor="mt", fill='black')

        draw.multiline_text((width / 2, from_top_counter), tips,
                            font=get_font(font_post.path, post_font_size),
                            align='center', anchor="ms", fill='black')

        from_top_counter += size_multiline[1] + 100
        tips_number += 1

    if bottom_section:
        plane_bottom = Image.new('RGB', (1000, 120), 'black')
        plane_bottom.putalpha(140)

        im.alpha_composite(plane_bottom, (0, height - 120))

        with Pilmoji(im) as pilmoji:
            pilmoji.text((100, height - 100), bottom_text.upper(),
                         font=get_font(font_title.path, 50),
                         fill='white')

    images_dir = READY / folder_name / 'images'
    images_dir.mkdir(exist_ok=True)
    filename = f'{row[0]}[[{board_name}]].png'
    full_path = os.path.join(images_dir, filename)
    im.save(full_path)
    print('Image saved')

if __name__ == '__main__':
    project_folder = 'Keto'
    open_data(project_folder)
