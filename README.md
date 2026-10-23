# Experiment 8: Cookies and HTTP Sessions

## Aim

Explore how cookies and HTTP sessions maintain user-specific state across
requests to a web application.

## Overview

HTTP requests are independent by default: a server does not automatically
remember information from one request when the next request arrives. Session
tracking provides a way to associate information with a user's browser across
requests.

This Flask application demonstrates two approaches:

| Mechanism | Where the data is stored | Example in this application |
| --- | --- | --- |
| Cookie | In the browser, sent with subsequent requests | The user's language preference |
| HTTP session | On the server, associated with the browser by a session ID | The user's visit count |

The language cookie and visit-count session are independent. Selecting a
language does not reset the visit count, and resetting the visit count does not
remove the language preference.

## Cookie demonstration

The application stores the selected language in a `user_language` cookie. Use
the English or Spanish link on the home page to set the preference. The
`/set_language/<language>` route accepts `en` and `es`, sets the cookie, and
shows a confirmation page. The home page reads the cookie on a later request
and displays the saved value.

The cookie is configured to last for one year and uses the `HttpOnly` and
`SameSite=Lax` attributes. It demonstrates storing a small preference in the
browser; the application displays the selected language code but does not
translate the page.

## HTTP session demonstration

Flask-Session is configured with its filesystem backend. Session data is stored
on the server under `instance/sessions`, while the browser receives a session
identifier that Flask uses to associate later requests with that data.

When the home page is requested, the application increments
`session["visit_count"]`. A new session starts at visit 1, and later requests
from the same browser session show an increasing count. The **Reset visit
count** link clears that value; its redirect returns to the home page, which
then starts the count again at 1.

## Routes

| Route | Purpose |
| --- | --- |
| `/` | Displays the saved language preference and increments/displays the session visit count |
| `/set_language/en` | Saves English as the language preference |
| `/set_language/es` | Saves Spanish as the language preference |
| `/reset_session` | Clears the visit count and redirects to the home page |

Any other language code returns a 404 response.

## Requirements

- Python 3
- Flask
- Flask-Session

Install the dependencies and start the application in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_SECRET_KEY = "use-a-random-secret-value"
py app.py
```

Then open <http://127.0.0.1:5000> in a browser. The default secret key in the
code is only a development fallback; configure a private, random
`FLASK_SECRET_KEY` before using the application outside a local demonstration.
Debug mode is enabled for this experiment and should also be disabled before
deployment.

## Expected result

On the first visit, the page indicates that the language preference is not set
and shows visit number 1. After choosing a language, the home page displays the
saved preference. Refreshing or revisiting the page in the same browser session
increases the visit count. Resetting the count starts it over.

## Conclusion

Cookies are useful for small pieces of client-side state such as preferences.
HTTP sessions let an application keep per-user state on the server, with a
session ID linking the browser's requests to that data. The appropriate choice
depends on the data and the application's security and storage requirements.
