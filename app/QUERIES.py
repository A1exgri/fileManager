from app.settings import IMAGES_LIMIT

CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS images (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    filename TEXT NOT NULL,
    original_name TEXT NOT NULL,
    size INTEGER NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_type TEXT NOT NULL
);'''

ADD_IMAGE = """
INSERT INTO images (filename, original_name, size, file_type)
    VALUES (%(filename)s, %(original_name)s, %(size)s, %(file_type)s)
"""

DELETE_IMAGE_BY_NAME = '''
DELETE FROM images WHERE filename = %s
'''

GET_ALL_IMAGES = '''
SELECT * from images LIMIT {IMAGES_LIMIT} OFFSET %s
'''

GET_IMAGES_NAMES = '''
SELECT filename || '.' || file_type  from images
'''