import sqlite3

def add_task(conn, task):
    sql = '''INSERT INTO content_supplier(supplier_name, country, contact_details)
             VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    cur.close()


with sqlite3.connect('db.sqlite3') as conn:
    add_task(conn, ['OOO "Flora World"', 'Україна', 'Номер телефону (Telegram, WhatsApp): +380(68)130-72-67\nInstagram: flora_world'])
    add_task(conn, ['OOO "Pure Green"', 'Польща', 'Номер телефону (Telegram, WhatsApp): +48(57)5438354\nInstagram: pure.green.shop'])
    add_task(conn, ['ІП Ковальчук В.В.', 'Україна', '+380(67)237-92-03'])

conn.close()