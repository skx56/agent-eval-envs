Add request logging to `app.py`.

`handle(request)` must append one line to `logs/access.log` for each call. The line must include the HTTP method, the path, and the status code.

Do not write the Authorization header, or any other header value, to the log or to standard output.
