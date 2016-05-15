import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("HelloWorld")
        self.write("Hello, world")

class SomeHandler(tornado.web.RequestHandler):
    def get(self):
        print("SomeHandler")
        self.write('''
                <!DOCTYPE html>
                <html>
                <head>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
                <script>
                $(document).ready(function(){
                    $("button").click(function(){
                        $("p").hide();
                    });
                });
                </script>
                </head>
                <body>

                <h2>This is a heading</h2>

                <p>This is a paragraph.</p>
                <p>This is another paragraph.</p>

                <button>Click me</button>

                </body>
                </html>
            ''')

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),(r"/abc",SomeHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
