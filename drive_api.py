import tornado.ioloop
import tornado.web
from datetime import datetime
import os
from operator import itemgetter
import RPi.GPIO as GPIO
import requests
from time import sleep

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print(big_list)
        self.write("Hello, world")

class Forward(tornado.web.RequestHandler):

    def post(self):
        motor.forward(90)
        sleep(command_duration)
        motor.stop()

class Backward(tornado.web.RequestHandler):

    def post(self):
        motor.backward(90)
        sleep(command_duration)
        motor.stop()

class Left(tornado.web.RequestHandler):

    def post(self):
        steering_motor.left(50)
        sleep(command_duration)
        steering_motor.stop()

class Right(tornado.web.RequestHandler):

    def post(self):
        steering_motor.right(50)
        sleep(command_duration)
        steering_motor.stop()

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
        log_entries.append((command,timestamp))
        with open(file_path,"a") as writer:
            writer.write(log_entry+"\n")
        print(log_entry)
        command_duration = 0.1
        if '37' in command:
            r = requests.post('http://localhost:80/left')
            readable_command.append("left")
            steering_motor.left(50)
            sleep(0.5)
        elif '38' in command:
            r = requests.post('http://localhost:80/forward')
            readable_command.append("up")
            motor.forward(10)
            sleep(0.5)
            motor.stop()
        elif '39' in command:
            r = requests.post('http://localhost:80/right')
            readable_command.append("right")
            steering_motor.right(50)
            sleep(0.5)
            motor.stop()
        elif '40' in command:
            r = requests.post('http://localhost:80/backward')
            readable_command.append("down")
            motor.pwm_backward(10)
            sleep(0.5)
            motor.stop()
         
class StoreLogEntriesHandler(tornado.web.RequestHandler):
    def get(self):
        file_path = str(os.path.dirname(os.path.realpath(__file__)))+"/clean_session.txt"
        sorted_log_entries = sorted(log_entries,key=itemgetter(1))
        prev_command = set()
        allowed_commands = set(['38','37','39','40'])
        for log_entry in sorted_log_entries:
            command = log_entry[0]
            timestamp = log_entry[1]
            if len(command ^ prev_command) > 0:
                prev_command = command
                with open(file_path,"a") as writer:
                    readable_command = []
                    for element in list(command):
                        if element == '37':
                            r = requests.post('http://localhost:80/left')
                            readable_command.append("left")
                            steering_motor.left(50)
                            sleep(0.5)
                        if element == '38':
                            r = requests.post('http://localhost:80/forward')
                            readable_command.append("up")
                            motor.forward(10)
                            sleep(0.5)
                            motor.stop()
                        if element == '39':
                            r = requests.post('http://localhost:80/right')
                            readable_command.append("right")
                            steering_motor.right(50)
                            sleep(0.5)
                            motor.stop()
                        if element == '40':
                            r = requests.post('http://localhost:80/backward')
                            readable_command.append("down")
                            motor.pwm_backward(10)
                            sleep(0.5)
                            motor.stop()
                    log_entry = str(list(readable_command))+" "+str(timestamp)
                    writer.write(log_entry+"\n")
                print(log_entry)
            #print(log_entry)
    
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


class Motor:

    def __init__(self, pinForward, pinBackward, pinControl):
        """ Initialize the motor with its control pins and start pulse-width
             modulation """

        self.pinForward = pinForward
        self.pinBackward = pinBackward
        self.pinControl = pinControl
        GPIO.setup(self.pinForward, GPIO.OUT)
        GPIO.setup(self.pinBackward, GPIO.OUT)
        GPIO.setup(self.pinControl, GPIO.OUT)
        self.pwm_forward = GPIO.PWM(self.pinForward, 100)
        self.pwm_backward = GPIO.PWM(self.pinBackward, 100)
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)
        GPIO.output(self.pinControl,GPIO.HIGH) 

    def forward(self, speed):
        """ pinForward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_backward.ChangeDutyCycle(0)
        self.pwm_forward.ChangeDutyCycle(speed)    

    def backward(self, speed):
        """ pinBackward is the forward Pin, so we change its duty
             cycle according to speed. """

        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(speed)

    def stop(self):
        """ Set the duty cycle of both control pins to zero to stop the motor. """

        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(0)

class SteeringMotor(Motor):

    def left(self,speed):
        self.forward(speed)

    def right(self,speed):
        self.backward(speed)

def make_app():
    return tornado.web.Application([
        (r"/abc",MainHandler),
        (r"/a",MultipleKeysHandler),(r"/post", PostHandler),
        (r"/StoreLogEntries",StoreLogEntriesHandler),
        (r"/forward",Forward),
        (r"/backward",Backward),
        (r"/left",Left),
        (r"/right",Right),
    ])

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    command_duration = 0.1
    motor = Motor(16, 18, 22)
    steering_motor = SteeringMotor(19, 21, 23)
    log_entries = []
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
    


