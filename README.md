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

1. Take business data from different JSON files stored in `options` folder recursively.
This folder has 2 subfolders - `campaigns` and `source` (in terms of UTM codes).
Each campaign's file is prefixed with source name to link them together.
2. Join each campaign info with its source by campaign's prefix.
3. Render each template according to input data.
4. Inline all CSS styles with `premailer`.
5. Minify code by simple regexps.
5. Save each template into separate file in `templates` folder.
