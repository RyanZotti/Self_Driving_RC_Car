import tornado.ioloop
import tornado.web
from datetime import datetime
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print(big_list)
        self.write("Hello, world")


class PostHandler(tornado.web.RequestHandler):

    def post(self):
        timestamp = datetime.now()
        data_json = tornado.escape.json_decode(self.request.body)
        allowed_commands = set(['38','37','39','40'])
        command = data_json['command']
        command = list(command.keys())
        command = set(command)
        command = allowed_commands & command
        file_path = str(os.path.dirname(os.path.realpath(__file__)))+"/session.txt"
        log_entry = str(command)+" "+str(timestamp)
        with open(file_path,"a") as writer:
            writer.write(log_entry+"\n")
        print(log_entry)
         

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
