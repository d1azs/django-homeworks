from django.http import HttpResponse
import math


def index(request):
    return HttpResponse(
        "Сервіс квадратних рівнянь. "
        "Приклад: /quadratic/?a=1&b=-5&c=6"
    )


def quadratic_view(request):
    a = request.GET.get("a")
    b = request.GET.get("b")
    c = request.GET.get("c")

    if a is None or b is None or c is None:
        return HttpResponse("Потрібно передати параметри a, b, c", status=400)

    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except ValueError:
        return HttpResponse("a, b, c мають бути числами", status=400)

    if a == 0:
        return HttpResponse("a не може бути 0 (це не квадратне рівняння)", status=400)

    D = b**2 - 4 * a * c

    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)
        return HttpResponse(f"Корені рівняння: x1 = {x1}, x2 = {x2}")
    elif D == 0:
        x = -b / (2 * a)
        return HttpResponse(f"Рівняння має один корінь: x = {x}")
    else:
        return HttpResponse("Рівняння не має дійсних коренів (D < 0)")