# PythonPractice

Write a simple web application that exposes a single API which displays the weather (low and high) for each day of the current
week. Leverage tornado (python) or gin (golang) frameworks to serve the request. Use the Dark Sky API for weather data. No CSS
is necessary. The web application should serve the data in JSON format (in essence, it's a wrapper for the Dark Sky API that
provides a higher level abstraction).

Example Request: GET http://localhost:xxxx/api/v1/weather

Example Response:
200
application/json
[
    "sunday": {
        "low": 20.0,
        "high": 53.3
    },
    ...
    "saturday": {
        "low": 30.1,
        "high": 61.4
    }
]

The days of the week returned should start with the current day (server time).

Extra Credit:
- Use a cache to ensure that the Dark Sky API is only accessed at most once per 5 minutes. Explain the implications in comments.
- Add a sub-url so that a single day can be requested, e.g. http://localhost:xxxx/api/v1/weather/monday

Resources:
- Dark Sky: https://darksky.net/dev
- Gin: https://github.com/gin-gonic/gin
- Tornado: https://github.com/tornadoweb/tornado
