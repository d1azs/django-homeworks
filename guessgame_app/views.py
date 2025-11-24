from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import random

SECRET_KEY = "guess_secret_number"
MESSAGE_KEY = "guess_message"


def _get_or_create_secret_number(request):
    """Отримуємо загадане число з сесії або створюємо нове."""
    secret = request.session.get(SECRET_KEY)
    if secret is None:
        secret = random.randint(1, 100)
        request.session[SECRET_KEY] = secret
    return secret


def guess_view(request):
    """
    GET: показує форму + результат останньої спроби (якщо є в сесії).
    Це кінцева точка в PRG (Post-Redirect-Get).
    """
    message = request.session.pop(MESSAGE_KEY, "")

    html = f"""
    <html>
      <head>
        <title>GuessGame</title>
      </head>
      <body>
        <h1>Гра "Вгадай число"</h1>
        <p>Я загадав число від 1 до 100. Спробуй вгадати!</p>

        {"<p><strong>" + message + "</strong></p>" if message else ""}

        <form action="{reverse('guess_submit')}" method="post">
          <label>Введіть число: <input type="number" name="number" required></label>
          <button type="submit">Submit</button>
        </form>
      </body>
    </html>
    """
    return HttpResponse(html)


@csrf_exempt
def guess_submit(request):
    """
    POST: обробляє введене число, порівнює із secret
    і кладе повідомлення в session, потім робить redirect на /guess/ (GET).
    """
    if request.method != "POST":
        return HttpResponseRedirect(reverse("guess"))

    secret = _get_or_create_secret_number(request)

    user_input = request.POST.get("number")

    try:
        guess = int(user_input)
    except (TypeError, ValueError):
        request.session[MESSAGE_KEY] = "Будь ласка, введіть коректне ціле число."
        return HttpResponseRedirect(reverse("guess"))

    if guess == secret:
        request.session[MESSAGE_KEY] = f"🎉 Вітаю! Ви вгадали число {secret}. Нова гра розпочата!"
        request.session[SECRET_KEY] = random.randint(1, 100)
    elif guess < secret:
        request.session[MESSAGE_KEY] = "Не вгадали. Загадане число більше."
    else:
        request.session[MESSAGE_KEY] = "Не вгадали. Загадане число менше."

    # PRG: після POST робимо Redirect на GET (/guess/)
    return HttpResponseRedirect(reverse("guess"))