import pyglet

import pygletreactor
pygletreactor.install()

from twisted.internet import reactor, task
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

window = pyglet.window.Window(1000, 1000)
batch = pyglet.graphics.Batch()

vertex_list = pyglet.graphics.vertex_list(1000000, 'v2i', 'c3B')

@window.event
def on_draw():
    window.clear()
    vertex_list.draw(pyglet.gl.GL_POINTS)

colors = {
    'red': [255, 0, 0],
    'green': [0, 255, 0],
    'blue': [0, 0, 225],
}

class PixelServer(LineReceiver):
    def __init__(self):
        self.pixels = []

    def connectionMade(self):
        print("Connection received...")
        print(self.transport.hostname)

    def lineReceived(self, line):
        print(line)
        decoded_line = line.decode('utf-8')
        x_str, y_str, color_str = str(decoded_line).split()
        x, y, (r, g ,b) = int(x_str), int(y_str), colors[color_str]
        vertex_list.vertices[(x + y * 1000) * 2] = x
        vertex_list.vertices[(x + y * 1000) * 2 + 1] = y
        vertex_list.colors[(x + y * 1000) * 3] = r
        vertex_list.colors[(x + y * 1000) * 3 + 1] = g
        vertex_list.colors[(x + y * 1000) * 3 + 2] = b
        self.sendLine(b'ok')

    def connectionLost(self, reason):
        print("Connection lost...")

factory = Factory()
factory.protocol = PixelServer
reactor.listenTCP(8000, factory)

reactor.run()
