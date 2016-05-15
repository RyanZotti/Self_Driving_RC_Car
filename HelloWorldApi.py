import tornado.ioloop
import tornado.web

# import requests
# r = requests.get('http://localhost:80/')
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("HelloWorld")
        self.write("Hello, world")

# import requests
# r = requests.post('http://localhost:80/post',json={'command':'speed'})
class PostHandler(tornado.web.RequestHandler):
    def post(self):
        data_json = tornado.escape.json_decode(self.request.body)
        command = data_json['command']
        print(command)
            

class MultipleKeysHandler(tornado.web.RequestHandler):
    def get(self):
        print("HelloWorld")
        self.write('''
                <!DOCTYPE html>
                <html>
                    <head>
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
                        <script>
                            var keys = {};

                            $(document).keydown(function (e) {
                                keys[e.which] = true;
                                
                                var json_upload = JSON.stringify({command:keys});
                                var xmlhttp = new XMLHttpRequest(); 
                                xmlhttp.open("POST", "/post");
                                xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                                xmlhttp.send(json_upload);

                                printKeys();
                            });

                            $(document).keyup(function (e) {
                                delete keys[e.which];
                                
                                var json_upload = JSON.stringify({command:keys});
                                var xmlhttp = new XMLHttpRequest(); 
                                xmlhttp.open("POST", "/post");
                                xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                                xmlhttp.send(json_upload);

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

def make_app():
    return tornado.web.Application([
        (r"/abc",MainHandler),
        (r"/a",MultipleKeysHandler),(r"/post", PostHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
