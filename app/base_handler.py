import json
from http.server import BaseHTTPRequestHandler
from app.settings import STATIC_PATH, MEDIA_DIR, IMAGE_EXTENSIONS, MAX_FILE_SIZE, MEDIA_PATH
from multipart import MultipartPart, MultipartParser, parse_options_header
import logging

logger = logging.getLogger(__name__)


class BasicHandler(BaseHTTPRequestHandler):
    server_version = '0.1'
    server_name = 'Image Hosting Server'

    def response(self, data: str | bytes, content_type: str = 'text/html', status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(data if isinstance(data, bytes) else data.encode('utf-8'))

    def html_response(self, data: str | bytes, status_code=200) -> None:
        self.response(data, 'text/html', status_code)

    def json_response(self, data: dict | list | str | bytes, status_code=200) -> None:
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        self.response(data, 'application/json', status_code)

    @staticmethod
    def load_file(filename: str, directory=STATIC_PATH) -> bytes:
        try:
            with open(f'{directory}/{filename}', 'rb') as file:
                return file.read()
        except FileNotFoundError:
            return b'Not Found'
        except ValueError:
            return b'Not Found'

    def template_response(self, template_filename: str) -> None:
        self.html_response(self.load_file(template_filename))

    def send_static_file(self, filename: str) -> None:
        if filename.endswith('.png'):
            content_type = 'image/png'
        elif filename.endswith('.css'):
            content_type = "text/css"
        elif filename.endswith('.js'):
            content_type = "application/javascript"
        else:
            content_type = 'application/octet-stream'
        self.response(self.load_file(filename), content_type)

    def send_media_file(self, filename: str) -> None:
        self.response(self.load_file(filename, MEDIA_PATH), 'image/png')

    def validate_file(self, file: MultipartPart) -> bool:
        name, ext = file.filename.split('.')
        if ext.lower() not in IMAGE_EXTENSIONS:
            self.response(f'Invalid file type. Allowed types {IMAGE_EXTENSIONS}', status_code=400)
            return False
        if file.size > MAX_FILE_SIZE:
            self.response('The size of the uploaded files is too large', status_code=400)
            return False
        return True

    def parse_multipart(self, content_type: str, options: dict, content_length: int, filename: str = None) -> str | None:
        if content_type == "multipart/form-data" and "boundary" in options:
            parser = MultipartParser(
                self.rfile,
                boundary=options["boundary"],
                content_length=content_length
            )

            for part in parser:
                if self.validate_file(part):
                    logger.info(f'{part.name}: File upload ({part.size}) bytes')
                    ext = part.filename.split('.')[-1] if '.' in part.filename else ''
                    file = f"{filename}.{ext}" if filename else part.filename
                    part.save_as(f'{MEDIA_DIR}/{file}')
                    return file
                else:
                    logger.info(f'Invalid file type image {part.name}')
                    return

            for part in parser.parts():
                part.close()

    def upload_file(self, filename: str = None) -> str | None:
        content_type, options = parse_options_header(
            self.headers['Content-Type']
        )
        content_length = int(self.headers['Content-Length'])
        return self.parse_multipart(content_type, options, content_length, filename)
        