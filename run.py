from Flask_server import app, config
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if __name__ == "__main__":
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(config["port"])
    IOLoop.instance().start()
