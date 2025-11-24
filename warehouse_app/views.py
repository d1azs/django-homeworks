from django.http import HttpResponse
from django.urls import reverse
from .models import Product
from decimal import Decimal
import random


ITEM_NAMES = [
    "Pen", "Pencil", "Notebook", "Marker", "Highlighter",
    "Stapler", "Eraser", "Folder", "Sticky Notes", "Binder"
]

BRANDS = [
    "Pilot", "Stabilo", "Faber-Castell", "Bic", "Maped",
    "Parker", "Lamy", "Brauberg", "Koh-I-Noor"
]

CATEGORIES = [
    "Writing", "Paper", "Office", "Drawing", "Accessories"
]


def products_view(request):
    """
    /products — показує всі товари у вигляді HTML-таблиці.
    """
    products = Product.objects.all().order_by("id")

    rows = ""
    for p in products:
        rows += f"""
        <tr>
          <td>{p.id}</td>
          <td>{p.item_name}</td>
          <td>{p.brand}</td>
          <td>{p.category}</td>
          <td>{p.quantity_in_pack}</td>
          <td>{p.price}</td>
        </tr>
        """

    if not rows:
        rows = '<tr><td colspan="6">Немає товарів у базі.</td></tr>'

    html = f"""
    <html>
      <head>
        <title>Products</title>
      </head>
      <body>
        <h1>Склад (канцелярія)</h1>
        <p><a href="/">На головну</a></p>
        <p><a href="{reverse('replenish', kwargs={{'count': 5}})}">Додати 5 випадкових товарів</a></p>

        <table border="1" cellpadding="5" cellspacing="0">
          <tr>
            <th>ID</th>
            <th>Item name</th>
            <th>Brand</th>
            <th>Category</th>
            <th>Quantity in pack</th>
            <th>Price</th>
          </tr>
          {rows}
        </table>
      </body>
    </html>
    """
    return HttpResponse(html)


def replenish_view(request, count: int):
    """
    /replenish/<int:count> — створює count нових випадкових Product.
    """
    created = 0
    for _ in range(count):
        item_name = random.choice(ITEM_NAMES)
        brand = random.choice(BRANDS)
        category = random.choice(CATEGORIES)
        quantity_in_pack = random.randint(1, 50)  

        price_float = round(random.uniform(10.0, 200.0), 2)
        price = Decimal(str(price_float))

        Product.objects.create(
            item_name=item_name,
            brand=brand,
            category=category,
            quantity_in_pack=quantity_in_pack,
            price=price,
        )
        created += 1

    html = f"""
    <html>
      <head><title>Replenish</title></head>
      <body>
        <h1>Додано {created} нових записів.</h1>
        <p><a href="{reverse('products')}">Перейти до списку товарів</a></p>
        <p><a href="/">На головну</a></p>
      </body>
    </html>
    """
    return HttpResponse(html)