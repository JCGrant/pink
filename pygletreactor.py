import queue

import pyglet
from twisted.internet import _threadedselect

class PygletEventLoop(pyglet.app.base.EventLoop):
    def __init__(self, twisted_queue, call_interval=1/10.):
        super().__init__()
        self.register_twisted_queue(twisted_queue, call_interval)        

    def register_twisted_queue(self, twisted_queue, call_interval):
        self._twisted_call_queue = twisted_queue
        self.clock.schedule_interval_soft(self._make_twisted_calls, call_interval)

    def _make_twisted_calls(self, dt):
        try:
            f = self._twisted_call_queue.get(False)
            f()
        except queue.Empty:
            pass

class PygletReactor(_threadedselect.ThreadedSelectReactor):
    def _runInMainThread(self, f):
        self._twistedQueue.put(f)

    def _stopPyglet(self):
        if hasattr(self, "pygletEventLoop"):
            self.pygletEventLoop.exit()

    def run(self, call_interval=1/10.):
        self._twistedQueue = queue.Queue()
        self.pygletEventLoop = PygletEventLoop(self._twistedQueue, call_interval)
        self.interleave(self._runInMainThread, installSignalHandlers=True)
        self.addSystemEventTrigger("after", "shutdown", self._stopPyglet)
        self.pygletEventLoop.run()

    def stop(self):
        _threadedselect.ThreadedSelectReactor.stop(self)

def install():
    reactor = PygletReactor()
    from twisted.internet.main import installReactor
    installReactor(reactor)
    return reactor

__all__ = ['install']
