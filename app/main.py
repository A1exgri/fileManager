from http.server import HTTPServer
import logging
import settings
from app.image_hosting_handler import ImageHostingHandler


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M%S')

logger = logging.getLogger(__name__)


def run(server_address=('', 8001), server_class=HTTPServer, handler_class=ImageHostingHandler):
    logger.info(f'Starting the webserver on {server_address}')
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        httpd.server_close()
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == '__main__':
    run()
