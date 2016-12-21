#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from jinja2 import Environment, FileSystemLoader
import json
import os
import premailer
import re

# Basic email campaign's template
this_dir = os.path.dirname(os.path.abspath(__file__))
template = Environment(
    loader=FileSystemLoader(this_dir),
    trim_blocks=True
).get_template('template.j2.html')

# Paths to email campaign and source options (parameters)
campaigns = os.path.join(os.getcwd(), 'options', 'campaigns')
sources   = os.path.join(os.getcwd(), 'options', 'sources')

for opt in os.listdir(campaigns):
    if opt.endswith('.json'):
        # Get current template options
        cur_campaign = json.load(
            open(os.path.join(campaigns, opt), 'r')
        )

        # Tempate to be rendered only if `renderable` option is true
        if cur_campaign['renderable']:
            # Get source options for corresponding campaign options
            for src in os.listdir(sources):
                if src == opt.split('_')[0] + '.json':
                    cur_source = json.load(
                        open(os.path.join(sources, src), 'r')
                    )

            # Join campaign and source options into one dictionary
            cur_campaign.update(cur_source)
            # print(json.dumps(
            #     cur_campaign, indent=4, ensure_ascii=False, sort_keys=False)
            # )

            # Render email template with options needed
            cur_template = template.render(cur_campaign)

            # Inline CSS styles
            cur_template = premailer.Premailer(
                cur_template,
                keep_style_tags=False,
                include_star_selectors=True,
                capitalize_float_margin=True,
                strip_important=False,
                align_floating_images=False,
                remove_unset_properties=False
            ).transform()

            # Minify source code
            cur_template = re.sub(r'^\ +', r'', cur_template, 0, re.MULTILINE)
            cur_template = re.sub(r'\n',   r'', cur_template)

            # Save prepared template to an HTML file
            cur_output = open(
                os.path.join(os.getcwd(), 'templates',
                    opt[:-5] + '.html'
                ), 'w'
            )
            cur_output.write(cur_template)
