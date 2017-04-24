from app import app, config
from gevent.pywsgi import WSGIServer
from gevent import monkey

# need to patch sockets to make requests async
monkey.patch_all()

if __name__ == "__main__":


    # use gevent WSGI server instead of the Flask

    conf = config.DevelopmentConfig

    port = conf.PORT
    host = conf.HOST

    print("Started JSShell server ...")
    print("Host:",host)
    print("Port:",port)

    http = WSGIServer((host, port), app.wsgi_app)
    http.serve_forever()
