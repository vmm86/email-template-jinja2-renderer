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
    // Campaign's name and `utm_campaign` value
    "campaign": "afisha-2016-10",
    // <title> text that should be the same as email subject
    "title": "Афиша Воронеж. Открыты продажи на осень 2016 г.",
    // Subtitle (invisible text that some email programs show below the email subject) - not more than 120-140 symbols
    "subtitle": "Не пропустите лучшие концерты и спектакли грядущего сезона",
    // Email header (may be an empty list)
    "header":
    [
        // Each element of this list is wrapped into a paragraph
        "Не пропусти!",
        "Уже в продаже лучшие билеты нового концертного сезона!"
    ],
    // A list of rows of some clikable events' posters
    "events_list":
    [
        // Every child dictionary is one row in a table, that holds one or many posters of events
        {
            // Additional buttons may be renderer above or beyond posters:
            // "top"
            // "bottom"
            "buttons": "bottom",
            // A list of dictionaries with attributes of each event
            "events":
            [
                {
                    // Name of event and `utm_content` value
                    "content": "nargiz",
                    // int - ID of event
                    // str - external link
                    "event_id": 1206,
                    // int - link to small vertical event's poster
                    // str - link to big vertical campaign's poster
                    "img": "2016-10-28_nargiz.jpg",
                    // `alt` attribute of poster's image
                    "alt": "2016-10-28 Наргиз Закирова «Танцы на битых стеклах» Воронежский Концертный Зал",
                    // Type of button
                    // "buy"           - to buy a ticket
                    // "registration"  - to register on some external site
                    "button": "buy"
                },
                {
                    "content": "shtraus-orkestr",
                    "event_id": 1200,
                    "img": "2016-11-02_shtraus-orkestr.jpg",
                    "alt": "2016-11-02 Венский Филармонический Штраус Оркестр Театр Оперы и Балета",
                    "button": "buy"
                }
            ]
        },
        {
            "buttons": "bottom",
            "events":
            [
                {
                    "content": "staraya-deva",
                    "event_id": 1168,
                    "img": "2016-11-28_staraya-deva.jpg",
                    "alt": "2016-11-26 «Старая дева» Воронежский Концертный Зал",
                    "button": "buy"
                },
                {
                    "content": "devyatova",
                    "event_id": 1201,
                    "img": "2016-12-03_devyatova.jpg",
                    "alt": "2016-12-03 Марина Девятова Воронежский Концертный Зал",
                    "button": "buy"
                }
            ]
        }
    ],
    // Email footer (may be an empty list)
    "footer":
    [
        // Each element of this list is wrapped into a paragraph
        "С полной информацией о всех мероприятиях Вы можете ознакомиться на нашем сайте..."
    ]
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
    "source_logo_alt": "Афиша Воронежа - билеты на концерты и спектакли в Воронеже",
    // Text in social icons' block at the bottom
    "source_social_text": "Заходите в наши группы в социальных сетях..."
}
```

Each campaign's file is prefixed with source name to link them together.

2. Joins each campaign info with its source by campaign's prefix.

3. Renders each template according to input data.

4. Inlines all CSS styles with `premailer`.
Each style within the `<style>` tag goes into `style` attribute of each corresponding HTML tag.

5. Minifies code by simple regexps.

6. Saves each template into separate file in `templates` folder.
