from app.base_handler import BasicHandler


class ImageHostingHandler(BasicHandler):
    def do_GET(self):
        path = self.path
        if self.path == '/':
            self.template_response('index.html')
        elif self.path == '/upload':
            self.template_response('upload.html')
        elif self.path == '/images':
            self.template_response('images.html')
        elif any(self.path.endswith(ext) for ext in ['.css', '.js', '.png']):
            self.send_file(self.path)
        else:
            self.html_response('Not Found', 404)
