import sqlite3
import os
import imghdr  
import mimetypes
'''
def save_images(db_path, table_name, blob_column, genus_column, id_column, output_dir):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f"SELECT {genus_column}, {id_column}, {blob_column} FROM {table_name}"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for genus, id, blob_data in rows:
            if blob_data is not None:
                file_extension = get_file_extension(blob_data)

                filename = f"{genus}_{id}.{file_extension}"
                file_path = os.path.join(output_dir, filename)
                
                with open(file_path, 'wb') as file:
                    file.write(blob_data)
            else:
                print(f"Skipping: {genus}_{id} (No data)")
    finally:
        cursor.close()
        conn.close()


def get_file_extension(blob_data):
    image_type = imghdr.what(None, blob_data)
    if image_type:
        return image_type 

    mime_type = mimetypes.guess_type("dummy")[0] 
    if mime_type:
        return mime_type.split('/')[-1]  

    return None 

save_images('db.sqlite3', 'content_plant', 'photo', 'genus_id', 'plant_id', 'images/plants') '''

def save_image_paths(db_path, table_name, genus_column, id_column, output_dir):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    files = os.listdir(output_dir)
    file_names = [os.path.splitext(file)[0] for file in os.listdir(output_dir)]

    query = f'SELECT {genus_column}, {id_column} FROM {table_name}'

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for genus, id in rows:
            filename = f"{genus}_{id}"
            if filename in file_names:
                cursor.execute("UPDATE content_plant SET photo = ? WHERE plant_id = ?", (files[file_names.index(filename)], id))
                conn.commit() 
    finally:
        cursor.close()
        conn.close()


save_image_paths('db.sqlite3', 'content_plant', 'genus_id', 'plant_id', 'images/plants')