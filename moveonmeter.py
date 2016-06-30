from sys import argv
import asyncio
from aiohttp import web

class Handler:
    def __init__(self, n):
        self._max = n
        self._count = 0
        self._wsl = []

    @asyncio.coroutine
    def _increment(self):
        if self._count == self._max:
            for ws in self._wsl:
                ws.send_str('Shut up')
                yield from ws.drain()
            return False
        self._count += 1
        return True

    @asyncio.coroutine
    def handle_vote(self, request):
        if (yield from self._increment()):
            text = '<html>Vote #{}</html>'.format(self._count)
            return web.Response(body=text.encode('utf-8'))
        else:
            return web.Response(body='<html>Vote over</html>'.encode('utf-8'), status=410)

    @asyncio.coroutine
    def handle_interrupt(self, request):
        ws = web.WebSocketResponse()
        yield from ws.prepare(request)
        if self._count < self._max:
            ws.send_str('Continue')
        else:
            ws.send_str("Don't start")
        yield from ws.drain()
        self._wsl.append(ws)
        f = asyncio.Future()
        yield from f
        return ws


htmlump = '''<html>
<script>
window.onload = function() {
    var elem = document.createTextNode('Loading...')
    document.body.appendChild(elem)

    var ws = new WebSocket('ws' + window.location.href.slice(4) + '_ws')
    ws.onmessage = function(event) {
        elem.textContent = event.data;
    }
}
</script>
<body>
</body>
</html>'''.encode('utf-8')


@asyncio.coroutine
def send_interruptor(request):
    return web.Response(body=htmlump)


handler = Handler(int(argv[1]))
app = web.Application()
app.router.add_route('GET', '/vote', handler.handle_vote)
app.router.add_route('GET', '/interruptor', send_interruptor)
app.router.add_route('GET', '/interruptor_ws', handler.handle_interrupt)

web.run_app(app)
