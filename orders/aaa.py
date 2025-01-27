import os
import sys
import django

# Add the project's root directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)).rsplit('orders', 1)[0])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from orders.models import Order
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.http import FileResponse
import io
from datetime import datetime

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path))
order = Order.objects.first()

def generate_pdf_receipt(order):
    # Create a BytesIO buffer to store the PDF
    buffer = io.BytesIO()
    output_dir = os.path.abspath(os.getcwd())  # Root directory
    output_file = os.path.join(output_dir, f"receipt_{order.order_id}.pdf")
    pdf = canvas.Canvas(output_file, pagesize=A4)

    # Define coordinates and styles
    width, height = A4
    pdf.setTitle(f"Чек замовлення #{order.order_id}")

    # Add header
    pdf.setFont("DejaVuSans-Bold", 18)
    pdf.drawString(100, height - 50, "🌱 ІНТЕРНЕТ-МАГАЗИН РОСЛИН 🌱")
    pdf.setFont("DejaVuSans", 12)
    pdf.drawString(100, height - 70, "Ваш надійний магазин для саду та квітів")
    pdf.line(50, height - 80, width - 50, height - 80)

    # Order details
    pdf.setFont("DejaVuSans-Bold", 12)
    pdf.drawString(50, height - 100, f"КАСОВИЙ ЧЕК                                    #{order.order_id}")
    pdf.setFont("DejaVuSans", 10)
    pdf.drawString(50, height - 120, f"ДАТА ТА ЧАС: {order.order_date.strftime('%d %B %Y, %H:%M')}")
    pdf.drawString(50, height - 140, f"КЛІЄНТ: {order.user.first_name} {order.user.last_name}")
    pdf.drawString(50, height - 160, f"КОНТАКТ: {order.user.email}")
    pdf.drawString(50, height - 180, f"АДРЕСА: {order.order_street}, {order.order_house}/{order.order_flat}, {order.order_city}, Україна")

    pdf.line(50, height - 200, width - 50, height - 200)

    # Purchased items
    pdf.setFont("DejaVuSans-Bold", 10)
    pdf.drawString(50, height - 220, "ПРИДБАНІ ТОВАРИ:")
    y = height - 240

    pdf.setFont("DejaVuSans", 10)
    for item in order.items.all():
        line = f"{item.plant.plant_name} ({item.quantity} шт)        {item.quantity} x {item.price} грн = {item.quantity * item.price} грн"
        pdf.drawString(50, y, line)
        y -= 20

    pdf.line(50, y - 10, width - 50, y - 10)
    y -= 30

    # Summary
    pdf.setFont("DejaVuSans-Bold", 12)
    pdf.drawString(50, y, f"ЗАГАЛЬНА ВАРТІСТЬ: {order.total_price} грн")
    if order.discount:
        y -= 20
        pdf.drawString(50, y, f"ЗНИЖКА ({order.promocode}): -{order.discount} грн")
    y -= 20
    pdf.drawString(50, y, f"СПОСІБ ОПЛАТИ: {order.payment_method}")

    # Footer
    y -= 40
    pdf.line(50, y, width - 50, y)
    y -= 20
    pdf.setFont("DejaVuSans", 10)
    pdf.drawString(50, y, "ДЯКУЄМО ЗА ВАШЕ ЗАМОВЛЕННЯ!")
    pdf.drawString(50, y - 20, "🌸 Завітайте до нас знову: www.onlinegardenshop.com 🌸")

    # Save the PDF
    pdf.save()

    # Return the PDF file as a response
    #buffer.seek(0)
    #return FileResponse(buffer, as_attachment=True, filename=f"receipt_{order.order_id}.pdf")

generate_pdf_receipt(order)
