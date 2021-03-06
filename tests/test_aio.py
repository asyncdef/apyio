"""Test suites for the async io object wrappers."""

import asyncio
import functools
import io

import pytest

import apyio


def async_test(loop=None):
    """Wrap an async test in a run_until_complete for the event loop."""
    loop = loop or asyncio.get_event_loop()

    def _outer_async_wrapper(func):
        """Closure for capturing the configurable loop."""
        @functools.wraps(func)
        def _inner_async_wrapper(*args, **kwargs):

            return loop.run_until_complete(func(*args, **kwargs))

        return _inner_async_wrapper

    return _outer_async_wrapper


def test_string_io_produces_string_io():
    """Check that the return value is an implementation of the interface."""
    stream = apyio.StringIO()
    assert isinstance(stream, apyio.AsyncStringIOWrapper)
    assert isinstance(stream._stream, io.StringIO)


def test_bytes_io_produces_bytes_io():
    """Check that the return value is an implementation of the interface."""
    stream = apyio.BytesIO()
    assert isinstance(stream, apyio.AsyncBytesIOWrapper)
    assert isinstance(stream._stream, io.BytesIO)


def test_async_methods_return_coroutine():
    """Check that the async read returns a coroutine object."""
    stream = apyio.StringIO()
    coro = stream.read()
    assert hasattr(coro, '__await__')


def test_sync_methods_dont_return_coroutine():
    """Check that the async write does not return a coroutine object."""
    stream = apyio.BytesIO()
    assert not hasattr(stream.write(b''), '__await__')


@async_test()
async def test_async_methods_can_be_awaited():
    """Check that the async reads can be awaited."""
    stream = apyio.StringIO()
    value = await stream.read()
    assert value == ''


@async_test()
async def test_streams_are_async_iterable():
    """Check that the streams are async iterable."""
    stream = apyio.StringIO()
    stream.writelines(('test\n', 'test2\n'))
    await stream.drain()
    await stream.seek(0)
    async for line in stream:

        assert line
        break

    else:

        pytest.fail('Did not async iter lines.')


@async_test()
async def test_streams_are_async_contexts(tmpdir):
    """Check that the streams are async context managers."""
    async with apyio.open(str(tmpdir.join('testfile.txt')), 'w') as test_file:

        assert test_file
