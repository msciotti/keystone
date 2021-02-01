from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from routes.keystone import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()