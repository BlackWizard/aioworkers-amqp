from aioworkers.amqp import AmqpQueue


class MockedAsynqp:
    class Message:
        def __init__(self, *args):
            self.a, = args

    def __getattr__(self, item):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __await__(self):
        async def coro():
            return self
        return coro().__await__()


async def test_queue(loop, mocker):
    mocker.patch('aioworkers.amqp.asynqp', MockedAsynqp())
    config = mocker.Mock(format='json')
    config.connection.auth = {}
    config.connection.host = 'localhost'
    config.connection.port = 5672
    context = mocker.Mock()
    q = AmqpQueue(config, context=context, loop=loop)
    await q.init()
    async with q:
        await q.put('3')
        await q.get()
