import os

import pyglet

import pygletreactor
pygletreactor.install()

from twisted.internet import reactor, task
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

width, height = int(os.environ.get('WIDTH', 1000)), int(os.environ.get('HEIGHT', 1000))
is_fullscreen = os.environ.get('FULLSCREEN') == '1'

window = pyglet.window.Window(width, height, fullscreen=is_fullscreen)

batch = pyglet.graphics.Batch()

vertex_list = pyglet.graphics.vertex_list(width * height, 'v2i', 'c3B')

@window.event
def on_draw():
    window.clear()
    vertex_list.draw(pyglet.gl.GL_POINTS)

colors = {
    'black': [0, 0, 0],
    'blue': [0, 0, 225],
    'green': [0, 255, 0],
    'aqua': [0, 255, 225],
    'red': [255, 0, 0],
    'magenta': [255, 0, 255],
    'yellow': [255, 255, 0],
    'white': [255, 255, 255],
}

def set_color(x, y, color):
    r, g, b = color
    vertex_list.vertices[(x + y * height) * 2] = x
    vertex_list.vertices[(x + y * height) * 2 + 1] = y
    vertex_list.colors[(x + y * height) * 3] = r
    vertex_list.colors[(x + y * height) * 3 + 1] = g
    vertex_list.colors[(x + y * height) * 3 + 2] = b

class PixelServer(LineReceiver):
    def connectionMade(self):
        print("Connection received...")
        print(self.transport.hostname)

    def lineReceived(self, line):
        try:
            decoded_line = line.decode('utf-8')
            x_str, y_str, color_str = str(decoded_line).split()
            set_color(int(x_str), int(y_str), colors[color_str])
            self.sendLine(b'ok')
            print('ok', line)
        except Exception as e:
            self.sendLine(b'error')
            print('error:', e)

    def connectionLost(self, reason):
        print("Connection lost...")

factory = Factory()
factory.protocol = PixelServer
reactor.listenTCP(8000, factory)

reactor.run()
