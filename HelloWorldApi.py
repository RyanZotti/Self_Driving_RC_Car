import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("HelloWorld")
        self.write("Hello, world")

class MultipleKeysHandler(tornado.web.RequestHandler):
    def get(self):
        print("HelloWorld")
        self.write('''
                <!DOCTYPE html>
                <html>
                <head>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
                <script>
                $(document).ready(function(){
                    $("button").click(function(){
                        $.get("/", function(data, status){
                            alert("Data: " + data + "\nStatus: " + status);
                        });
                    });
                });
                </script>
                <script>

var keys = {};

$(document).keydown(function (e) {
    keys[e.which] = true;
    
    printKeys();
});

$(document).keyup(function (e) {
    delete keys[e.which];
    
    printKeys();
});

function printKeys() {
    var html = '';
    for (var i in keys) {
        if (!keys.hasOwnProperty(i)) continue;
        html += '<p>' + i + '</p>';
    }
    $('#out').html(html);
}

                </script>
                </head>
                <body>
                Click in this frame, then try holding down some keys
                <div id="out"></div>
                </body>
                </html>
            ''')

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
                        $.get("/", function(data, status){
                            alert("Data: " + data + "\nStatus: " + status);
                        });
                    });
                });
                </script>
                </head>
                <body>

                <button>Send an HTTP GET request to a page and get the result back</button>

                </body>
                </html>
            ''')

def make_app():
    return tornado.web.Application([
        (r"/",SomeHandler ),(r"/abc",MainHandler),
        (r"/a",MultipleKeysHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
