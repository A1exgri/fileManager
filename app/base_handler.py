from http.server import BaseHTTPRequestHandler
from app.settings import STATIC_PATH, STATIC_DIR


class BasicHandler(BaseHTTPRequestHandler):
    server_version = '0.1'
    server_name = 'Image Hosting Server'

    def response(self, data: str | bytes, content_type: str = 'text/html', status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(data if isinstance(data, bytes) else data.encode('utf-8'))

    def html_response(self, data: str | bytes, content_type: str = 'text/html', status_code=200) -> None:

        self.response(data, content_type, status_code)

    @staticmethod
    def load_static(filename: str) -> bytes:
        try:
            print( f'{STATIC_PATH}/{filename}')
            with open(f'{STATIC_PATH}/{filename}', 'rb') as file:
                return file.read()
        except FileNotFoundError:
                return b'Not Found'

    def template_response(self, template_filename: str) -> None:
        print('template_filename', template_filename)
        self.html_response(self.load_static(template_filename))

    def send_file(self, filename) -> None:
        if filename.endswith('.png'):
            content_type = 'image/png'
        elif filename.endswith('.css'):
            content_type = "text/css"
        elif filename.endswith('.js'):
            content_type = "application/javascript"
        else:
            content_type = 'application/octet-stream'
        self.html_response(self.load_static(filename), content_type)

