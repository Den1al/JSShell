from app import app
from gevent.pywsgi import WSGIServer
from gevent import monkey

# need to patch sockets to make requests async
monkey.patch_all()

if __name__ == "__main__":


    # use gevent WSGI server instead of the Flask

    port = app.config.get('PORT')
    host = app.config.get('HOST')

    print("Started JSShell server on {}:{} ...".format(host, port))

    http = WSGIServer((host, port), app.wsgi_app)
    http.serve_forever()
