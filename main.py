import pyglet

window = pyglet.window.Window()

class SocketEventDispatcher(pyglet.event.EventDispatcher):
    def paint_pixel(self, coord, color):
        self.dispatch_event('on_paint_pixel', coord, color)
SocketEventDispatcher.register_event_type('on_paint_pixel')
event_dispatcher = SocketEventDispatcher()

@event_dispatcher.event
def on_paint_pixel(coord, color):
    pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
        ('v2i', coord),
        ('c3B', color)
    )

@window.event
def on_draw():
    window.clear()
    event_dispatcher.paint_pixel((20, 20), (255, 255, 255))

pyglet.app.run()
