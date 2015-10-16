===
aio
===

*Async wrappers for standard Python io streams.*

Example Usage
=============

For simple use cases this package provides the same high level utilities as
the Python `io` module:

.. code-block:: python

    import aio

    string_buff = aio.StringIO()
    bytes_buff = aio.BytesIO()
    file_handle = aio.open('somefile.txt', 'r')

The `write`, `writelines`, and `close` methods are left as normal functions
just as they are for the asyncio streams. However, any function which might
result in a read operation, such as `read`, `readline`, `readlines`, `read1`,
`seek`, `tell`, and `truncate`, are now `async def` functions that must be
`await`ed.

.. code-block:: python

    import aio

    async with aio.open('somefile.txt', 'w') as file_handle:

        file_handle.write('some data')
        await file_handle.drain()  # Same as flush().

    async with aio.open('somefile.txt', 'r') as file_handle:

        data = await file_handle.read()
        print(data)

    file_handle = aio.open('somefile.txt', 'r')
    async for line in file_handle:

        print(line)

For more advanced use cases, this package also contains async wrappers for all
classes defined in the Python `io` module. The wrappers are named using the
pattern `Async<>Wrapper`. For example, `BufferedReader` becomes
`AsyncBufferedReaderWrapper` and `FileIO` becomes `AsyncFileIOWrapper`. All
wrapper classes accept one argument in the constructor which must be the
original, synchronous stream.

.. code-block:: python

    import io
    import aio

    sync_stream = io.FileIO('somefile.txt', 'r')
    async_stream = aio.AsyncFileIOWrapper(sync_stream)
    print(sync_stream.readline())
    print((await async_stream.readline()))

If a file was opened using the built-in `open()` function it may not be an
instance of `io.FileIO`. Depending on the options given to `open()` different
kinds of streams may be returned. To help with wrapping arbitrary `open()`
return values use the `aio.wrap_file()` helper.

.. code-block:: python

    import aio
    file_handle = open('somefile.bin', 'r+b')
    async_handle = aio.wrap_file(file_handle)

Testing
=======

All tests are stored in the '/tests' subdirectory. All tests are expected to
pass for Python 3.5 and above. To run tests create a virtualenv and install
the test-requirements.txt list. After that using the `tox` command will launch
the test suite.

License
=======

    Copyright 2015 Kevin Conway

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Contributing
============

Firstly, if you're putting in a patch then thank you! Here are some tips for
getting your patch merged:

Style
-----

As long as the code passes the PEP8 and PyFlakes gates then the style is
acceptable.

Docs
----

The PEP257 gate will check that all public methods have docstrings. If you're
adding additional wrappers from the `io` module try to preserve the original
docstrings if possible. If you're adding something new, like a helper function,
try out the
`napoleon style of docstrings <https://pypi.python.org/pypi/sphinxcontrib-napoleon>`_.

Tests
-----

Make sure the patch passes all the tests. If you're adding a new feature don't
forget to throw in a test or two. If you're fixing a bug then definitely add
at least one test to prevent regressions.
