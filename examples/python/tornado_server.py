#!/usr/bin/python

import tornado.ioloop
import tornado.web
from tornado.gen import coroutine, Return, sleep
import uuid, time
import contextlib2

@contextlib2.contextmanager
def instrument():
    """Core instrumentation logic."""
    start_time = time.time()
    try:
        yield
    except:
        print 'instruemtn exception'
        raise
    else:
        end_time = time.time()
        ms = (end_time - start_time) * 1000
        print 'instrument timing was ' + str(ms)

class MainHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        rid = str(uuid.uuid4())
        print 'start ' + rid
        #t0 = time.time()
        with instrument():
            yield self.foo()
        #t1 = time.time()
        #print 'it took ' + str((t1-t0)*1000)
        print 'done ' + rid
        self.write("hellooooooo")

    @coroutine
    def foo(self):
        yield sleep(10)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    print 'launching'
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
