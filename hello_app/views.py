from django.http import HttpResponse


def hello_view(request):
    cookies_list = ""
    for key, value in request.COOKIES.items():
        cookies_list += f"<li>{key}: {value}</li>"

    if not cookies_list:
        cookies_list = "<li>(немає cookies)</li>"

    author_surname = "Tohqa"

    visit_count = request.session.get("hello_visits", 0)
    visit_count += 1
    request.session["hello_visits"] = visit_count


    html = f"""
    <html>
      <head><title>Hello Page</title></head>
      <body>
        <h1>Hello!</h1>

        <h2>Cookies:</h2>
        <ul>{cookies_list}</ul>

        <h2>Page views (session counter): {visit_count}</h2>

        <p><a href="/">На головну</a></p>
      </body>
    </html>
    """

    response = HttpResponse(html)
    response.set_cookie("author", author_surname)

    return response