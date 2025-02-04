from orders.models import Order
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import FileResponse
import io
from django.contrib.staticfiles import finders
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

DejaVuSans = finders.find('fonts/DejaVuSans.ttf')
DejaVuSans_bold = finders.find('fonts/DejaVuSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('DejaVuSans', DejaVuSans))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', DejaVuSans_bold))

def generate_pdf_receipt(order):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    pdf.setTitle(f"Чек замовлення #{order.order_id}")

    pdf.setFont("DejaVuSans-Bold", 18)
    pdf.drawString(130, height - 50, "ІНТЕРНЕТ-МАГАЗИН РОСЛИН")
    pdf.setFont("DejaVuSans", 12)
    pdf.drawString(150, height - 70, "Ваш надійний магазин для саду та квітів")
    pdf.line(50, height - 80, width - 50, height - 80)

    pdf.setFont("DejaVuSans-Bold", 12)
    pdf.drawString(50, height - 100, f"КАСОВИЙ ЧЕК                            #{order.order_id}")
    pdf.setFont("DejaVuSans", 10)
    pdf.drawString(50, height - 120, f"ДАТА ТА ЧАС: {order.order_date.strftime('%d.%m.%Y %H:%M')}")
    pdf.drawString(50, height - 160, f"ЗАМОВНИК: {order.user.email}")
    pdf.drawString(50, height - 180, f"АДРЕСА ЗАМОВЛЕННЯ: {order.order_street}, {order.order_house}/{order.order_flat}, {order.order_city}, Україна")

    pdf.line(50, height - 200, width - 50, height - 200)

    pdf.setFont("DejaVuSans-Bold", 10)
    pdf.drawString(50, height - 220, "ПРИДБАНІ ТОВАРИ:")
    y = height - 240

    pdf.setFont("DejaVuSans", 10)
    items = list(order.items.all())
    for index, item in enumerate(items):
        line = f"{item.plant.plant_name} ({item.quantity} шт)        {item.quantity} x {item.price} грн = {item.quantity * item.price} грн"
        pdf.drawString(50, y, line)
        if index < len(items) - 1:
            y -= 20
    y -= 5

    pdf.line(50, y - 10, width - 50, y - 10)
    y -= 50

    pdf.setFont("DejaVuSans-Bold", 12)
    pdf.drawString(50, y, f"ЗАГАЛЬНА ВАРТІСТЬ: {order.total_price} грн")

    if order.discount:
        y -= 20
        if order.promocode and order.promocode != '':
            pdf.drawString(50, y, f"ЗНИЖКА (за промокодом {order.promocode}): {order.discount}%")
        else:
            pdf.drawString(50, y, f"ЗНИЖКА: {order.discount}%")
        y -= 20
        pdf.drawString(50, y, f"ЗАГАЛЬНА ВАРТІСТЬ ІЗ ЗНИЖКОЮ: {order.discounted_total_price} грн")
    y -= 20
    pdf.drawString(50, y, f"СПОСІБ ОПЛАТИ: {order.payment_method}")

    y -= 40
    pdf.line(50, y, width - 50, y)
    y -= 20
    pdf.setFont("DejaVuSans", 10)
    pdf.drawString(50, y, "ДЯКУЄМО ЗА ВАШЕ ЗАМОВЛЕННЯ!")
    pdf.drawString(50, y - 20, "З питань просимо Вас звертатися за телефоном +380 (68) 130-72-67.")

    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"receipt_{order.order_id}.pdf")
