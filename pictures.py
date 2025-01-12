import sqlite3
from PIL import Image
import requests
from io import BytesIO
from googleapiclient.discovery import build
import matplotlib.pyplot as plt

def add_task(conn, task):
    sql = '''INSERT INTO content_plant(photo)
             VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

# Ключі API для Google Custom Search
api_key = 'AIzaSyAn7rFcmnlkLmESNcmzBfJR0AurgjdI8js'
cse_id = 'f376712d180704480'

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, searchType='image', num=10, **kwargs).execute()
    
    image_links = []
    if 'items' in res:
        for item in res['items']:
            image_links.append(item['link'])

    return image_links

def get_img_bytes(query):
    for url in google_search(query, api_key, cse_id):
        response = requests.get(url)
        content_type = response.headers.get('Content-Type')
        if 'image' in content_type:
            return response.content
        else:
            print(f'Запит {query} повернув HTML')
    return None

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

names = con.execute("SELECT plant_name FROM content_plant").fetchall()

for name in names:
    if cur.execute("SELECT photo FROM content_plant WHERE plant_name = ?", name).fetchone()[0] == None:
        try:
            cur.execute("UPDATE content_plant SET photo = ? WHERE plant_name = ?", (get_img_bytes(f'{name[0]} рослина фото без водяного знаку'), name[0]))
            print(name[0])
        except KeyError:
            print(name[0], '(зображення завантажити не вдалося)')
        except requests.exceptions.ConnectionError:
            print(name[0], '(зображення завантажити не вдалося)')
        except requests.exceptions.InvalidSchema:
            print(name[0], '(зображення завантажити не вдалося)')
        finally:
            con.commit()

cur.close()
con.close()