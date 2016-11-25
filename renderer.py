#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import jinja2
import json
import os
import premailer
import re

# Исходный шаблон email-рассылки
template = jinja2.Template(
    open('template.j2.html', 'r').read()
)

# Пути к параметрам рассылок и сайтов, на которые они ведут
campaigns = os.path.join(os.getcwd(), 'options', 'campaigns')
sources   = os.path.join(os.getcwd(), 'options', 'sources')

for opt in os.listdir(campaigns):
    if opt.endswith('.json'):
        # Берутся параметры конкретной рассылки
        cur_campaign = json.load(
            open(os.path.join(campaigns, opt), 'r')
        )

        # Рассылка генерируется, если опция `renderable` для этого включена
        if cur_campaign['renderable']:
            # В зависимости от организации берутся именно её параметры
            for src in os.listdir(sources):
                if src == opt.split('_')[0] + '.json':
                    cur_source = json.load(
                        open(os.path.join(sources, src), 'r')
                    )

            # Слияние словарей с параметрами рассылки и её сайта
            cur_campaign.update(cur_source)
            # print(json.dumps(
            #     cur_campaign, indent=4, ensure_ascii=False, sort_keys=False)
            # )

            # Отрисовка и сохранение шаблона email-рассылки
            cur_template = template.render(cur_campaign)

            # Инлайнинг стилей с помощью premailer
            cur_template = premailer.Premailer(
                cur_template,
                keep_style_tags=False,
                include_star_selectors=True,
                capitalize_float_margin=True,
                strip_important=False,
                align_floating_images=False,
                remove_unset_properties=False
            ).transform()

            # Минификация кода
            cur_template = re.sub(r'^\ +', r'', cur_template, 0, re.MULTILINE)
            cur_template = re.sub(r'\n',   r'', cur_template)

            # Сохранение готовой подписи в HTML-файл
            cur_output = open(
                os.path.join(os.getcwd(), 'templates',
                    opt[:-5] + '.html'
                ), 'w'
            )
            cur_output.write(cur_template)
