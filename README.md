# E-mail template Jinja2 renderer

Python Jinja2 templater to create multiple HTML files for email templates.

# Requirements

```python
cssselect==0.9.2
cssutils==1.0.1
Jinja2==2.8
lxml==3.6.0
MarkupSafe==0.23
premailer==3.0.0
requests==2.10.0
```

# Usage

You should create a new virtual environment with Python 3 and install everything from `requirements.txt`.

Then prepare the source data and simply run `renderer.py`. It does the following:

1. Takes business data from different JSON files stored in `options` folder recursively.
This folder has 2 subfolders - `campaigns` and `sources` (in terms of UTM codes).

Each HTTP link in email template should contain special standartized GET-parameters called UTM codes.
They help to clearly identify clicks on each link and further commercial conversion from each email that have been send.

* `utm_source`   - web site prefix or subdomain that email template belongs to
* `utm_medium`   - always "email"
* `utm_campaign` - campaign's name
* `utm_content`  - event's name within each campaign

`campaigns` JSON file format:

```js
{
    // Boolean attribute to render new template from the current source info file
    // or to skip rendering if it has been already rendered properly
    "renderable": true,
    // Campaign's name and `utm_campaign` value
    "campaign": "afisha-2016-10",
    // <title> text that should be the same as email subject
    "title": "Афиша Воронеж. Открыты продажи на осень 2016 г.",
    // Subtitle (invisible text that some email programs show below the email subject) - not more than 120-140 symbols
    "subtitle": "Не пропустите лучшие концерты и спектакли грядущего сезона",
    // Email header (may be an empty list)
    "header":
    [
        // HTML text information (each element of this list is wrapped into a paragraph)
        "Не пропусти!",
        "Уже в продаже лучшие билеты нового концертного сезона!"
    ],
    // A list of rows that contain text description or some clikable events' posters
    "events_list_top":
    [
        // Every child dictionary is one row in a table holding one or many posters of events
        {
            // Overall number of cells to be rendered within one row
            "cells_number": 2,
            // A list of dictionaries with information about each event
            "events":
            [
                {
                    // Type of information within the cell
                    // "text"   - text information
                    // "image"  - poster (with optional button)
                    "type": "text",
                    // Text information (only for "type": "text")
                    "text":
                    [
                        // HTML text information (each element of this list is divided by <br>)
                        "<strong>Ёлка. Большое сольное выступление!</strong>",
                        "Возрастное ограничение 12+",
                    ]
                },
                {
                    "type": "image",
                    // Name of event and `utm_content` value (only for "type": "image")
                    "content": "nargiz",
                    // Link to event (only for "type": "image")
                    // int - ID of event
                    // str - external link
                    "event_id": 1206,
                    // Link to image (only for "type": "image")
                    // int - small vertical event's poster
                    // str - big vertical campaign's poster
                    "img": "2016-10-28_nargiz.jpg",
                    // `alt` attribute of poster's image (only for "type": "image")
                    "alt": "2016-10-28 Наргиз Закирова «Танцы на битых стеклах» Воронежский Концертный Зал",
                    // Date of event as str (only for "type": "image")
                    "date": "28/10",
                    // Type of button (only for "type": "image")
                    // "buy"           - to buy a ticket
                    // "registration"  - to register on some external site
                    "button": "buy",
                    // Button position
                    // "top"    - above the poster
                    // "bottom" - beyond the poster
                    "button_position": "bottom"
                }
            ]
        },
        {
            "cells_number": 2,
            "events":
            [
                {
                    // If cell's width should be multiplied by a given number
                    "colspan": 2,
                    "content": "staraya-deva",
                    "event_id": 1168,
                    "img": "2016-11-28_staraya-deva.jpg",
                    "alt": "2016-11-28 «Старая дева» Воронежский Концертный Зал",
                    "date": "28/11",
                    "button": "buy"
                }
            ]
        }
    ],
    // Email body (may be an empty list)
    "body" [],
    // Same as `events_list_top`
    "events_list_bottom": [],
    // Email footer (may be an empty list)
    "footer":
    [
        // Each element of this list is wrapped into a paragraph
        "С полной информацией о всех мероприятиях Вы можете ознакомиться на нашем сайте..."
    ],
    // Custom links to social networks (may be an empty list)
    // If not empty, it will override the default links from the main template
    "social":
    {
        // "vkontakte" - VKontakte
        // "facebook"  - Facebook
        // "twitter"   - Twitter
        // "instagram" - Instagram
        "vkontakte": "https://vk.com/event127410472"
    }
}
```

`sources` JSON file format:

```js
{
    // Web site ID that email belongs to and `utm_source` value
    "source": "vrn",
    // Web site title
    "source_title": "Афиша Воронежа",
    // Web site main page link
    "source_link": "bezantrakta.ru",
    // Full kink to the main logo at the top
    "source_logo": "http://bezantrakta.ru/emailing/images/bzlogo-telephone.jpg",
    // `alt` attribute of the main logo
    "source_logo_alt": "bezantrakta.ru - билеты на концерты и спектакли в Воронеже",
    // Text in social icons' block at the bottom
    "source_social_text": "Присоединяйтесь к нашим официальным группам в социальных сетях!<br>\nБудьте в курсе последних событий!<br>\n"
}
```

Each campaign's file is prefixed with source name to link them together.

2. Joins each campaign info with its source by campaign's prefix.

3. Renders each template according to input data.

4. Inlines all CSS styles with `premailer`.
Each style within the `<style>` tag goes into `style` attribute of each corresponding HTML tag.

5. Minifies code by simple regexps.

6. Saves each template into separate file in `templates` folder.
