from app import app
from gevent.pywsgi import WSGIServer
from gevent import monkey

# need to patch sockets to make requests async
monkey.patch_all()


if __name__ == "__main__":

    print("Started gevent WSGI server")
    # use gevent WSGI server instead of the Flask

    http = WSGIServer(('', 5000), app.wsgi_app)
    # TODO gracefully handle shutdown
    http.serve_forever()
