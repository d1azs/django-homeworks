from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import math
import urllib.parse

FEEDBACKS = []


def index(request):
    html = """
    <html>
      <head><title>Math Project</title></head>
      <body>
        <h1>Лабораторні з Django</h1>
        <ul>
          <li><a href="/quadratic/">Калькулятор квадратних рівнянь (ДЗ 2.2 / 2.3)</a></li>
          <li><a href="/feedback/">Форма зворотного зв'язку (ДЗ 2.3)</a></li>
          <li><a href="/rating/">Статистика рейтингу (ДЗ 2.3)</a></li>
          <li><a href="/guess/">Гра "Вгадай число" (ПР 2.3)</a></li>
        </ul>
      </body>
    </html>
    """
    return HttpResponse(html)


def _solve_quadratic(a: float, b: float, c: float) -> str:
    """
    Обчислює корені квадратного рівняння ax^2 + bx + c = 0
    і повертає текстовий опис результату.
    """
    if a == 0:
        return "a не може бути 0 (це не квадратне рівняння)"

    D = b**2 - 4 * a * c

    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)
        return f"Корені рівняння: x1 = {x1}, x2 = {x2}"
    elif D == 0:
        x = -b / (2 * a)
        return f"Рівняння має один корінь: x = {x}"
    else:
        return "Рівняння не має дійсних коренів (D < 0)"


@csrf_exempt
def quadratic_view(request):
    """
    ДЗ 2.3:
    - GET: показує HTML-форму для введення a, b, c.
      Додатково: якщо в GET є параметри a,b,c, можемо одразу показати результат.
    - POST: приймає дані форми, рахує результат і робить redirect на /result (PRG).
    """

    if request.method == "POST":
        a_str = request.POST.get("a")
        b_str = request.POST.get("b")
        c_str = request.POST.get("c")

        if not a_str or not b_str or not c_str:
            result_text = "Потрібно заповнити всі поля a, b, c."
        else:
            try:
                a = float(a_str)
                b = float(b_str)
                c = float(c_str)
                result_text = _solve_quadratic(a, b, c)
            except ValueError:
                result_text = "a, b, c мають бути числами."

        encoded = urllib.parse.quote(result_text)
        url = f"{reverse('result')}?message={encoded}"
        return redirect(url)

    a_str = request.GET.get("a")
    b_str = request.GET.get("b")
    c_str = request.GET.get("c")
    result_block = ""

    if a_str is not None and b_str is not None and c_str is not None:
        try:
            a = float(a_str)
            b = float(b_str)
            c = float(c_str)
            result_text = _solve_quadratic(a, b, c)
        except ValueError:
            result_text = "a, b, c мають бути числами."
        result_block = f"<p><strong>Результат (GET): {result_text}</strong></p>"

    html = f"""
    <html>
      <head><title>Квадратне рівняння</title></head>
      <body>
        <h1>Калькулятор квадратних рівнянь</h1>
        <p>Рівняння вигляду: ax² + bx + c = 0</p>

        {result_block}

        <form method="post" action="">
          <label>a: <input type="text" name="a" required></label><br>
          <label>b: <input type="text" name="b" required></label><br>
          <label>c: <input type="text" name="c" required></label><br>
          <button type="submit">Обчислити</button>
        </form>

        <p>Після відправки форми відбувається перенаправлення (POST-Redirect-GET) на /result.</p>

        <p><a href="/">На головну</a></p>
      </body>
    </html>
    """
    return HttpResponse(html)


def result_view(request):
    """
    ДЗ 2.3:
    /result — показує результат обчислення, переданий через параметр message.
    """
    message = request.GET.get("message", "Результат відсутній.")
    message = urllib.parse.unquote(message)

    html = f"""
    <html>
      <head><title>Результат</title></head>
      <body>
        <h1>Результат обчислення</h1>
        <p><strong>{message}</strong></p>
        <p><a href="/quadratic/">Назад до форми квадратного рівняння</a></p>
        <p><a href="/">На головну</a></p>
      </body>
    </html>
    """
    return HttpResponse(html)


@csrf_exempt
def feedback_view(request):
    """
    ДЗ 2.3:
    /feedback — форма зворотного зв'язку:
      - name (ім'я)
      - rating (1..5)
    Дані зберігаються у глобальному списку FEEDBACKS.
    Після POST можна зробити redirect на /rating.
    """
    if request.method == "POST":
        name = request.POST.get("name") or "Анонім"
        rating_str = request.POST.get("rating")

        try:
            rating = int(rating_str)
        except (TypeError, ValueError):
            rating = None

        if rating is None or rating < 1 or rating > 5:
            error_html = """
            <p style="color:red;">Оцінка має бути числом від 1 до 5.</p>
            """
        else:
            FEEDBACKS.append({"name": name, "rating": rating})
            return redirect(reverse("rating"))
    else:
        error_html = ""

    html = f"""
    <html>
      <head><title>Feedback</title></head>
      <body>
        <h1>Форма зворотного зв'язку</h1>

        {error_html if request.method == "POST" else ""}

        <form method="post" action="">
          <label>Ім'я: <input type="text" name="name" placeholder="Ваше ім'я"></label><br>
          <label>Оцінка (1-5): <input type="number" name="rating" min="1" max="5" required></label><br>
          <button type="submit">Надіслати</button>
        </form>

        <p><a href="/rating/">Переглянути рейтинг</a></p>
        <p><a href="/">На головну</a></p>
      </body>
    </html>
    """
    return HttpResponse(html)


def rating_view(request):
    """
    ДЗ 2.3:
    /rating — показує:
      - кількість оцінок для кожного значення 1..5
      - середню оцінку
      - загальну кількість відгуків
    Дані беруться з глобального списку FEEDBACKS.
    """
    total = len(FEEDBACKS)
    counts = {i: 0 for i in range(1, 6)}
    sum_ratings = 0

    for fb in FEEDBACKS:
        r = fb["rating"]
        if r in counts:
            counts[r] += 1
            sum_ratings += r

    avg = sum_ratings / total if total > 0 else 0

    rows = ""
    for r in range(1, 6):
        rows += f"<tr><td>{r}</td><td>{counts[r]}</td></tr>"

    html = f"""
    <html>
      <head><title>Рейтинг</title></head>
      <body>
        <h1>Статистика рейтингу</h1>

        <table border="1" cellpadding="5" cellspacing="0">
          <tr><th>Оцінка</th><th>Кількість</th></tr>
          {rows}
        </table>

        <p>Загальна кількість відгуків: <strong>{total}</strong></p>
        <p>Середня оцінка: <strong>{avg:.2f}</strong></p>

        <p><a href="/feedback/">Залишити ще один відгук</a></p>
        <p><a href="/">На головну</a></p>
      </body>
    </html>
    """
    return HttpResponse(html)