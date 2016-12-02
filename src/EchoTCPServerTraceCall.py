# coding: utf-8
from __future__ import absolute_import

# Standard imports
import sys
import logging

# External imports
import aoiktracecall.config
import aoiktracecall.logging
import aoiktracecall.trace


# Traced modules should be imported after `trace_calls_in_specs` is called.


# Set configs
aoiktracecall.config.set_configs({
    # Whether use wrapper class.
    #
    # Wrapper class is more adaptive to various types of callables but will
    # break if the code that was using the original function requires a real
    # function, instead of a callable. Known cases include PyQt slot functions.
    #
    'WRAP_USING_WRAPPER_CLASS': True,

    # Whether wrap base class attributes in a subclass.
    #
    # If enabled, wrapper attributes will be added to a subclass even if the
    # wrapped original attributes are defined in a base class.
    #
    # This helps in the case that base class attributes are implemented in C
    # extensions thus can not be traced directly.
    #
    'WRAP_BASE_CLASS_ATTRIBUTES': True,

    # Indentation unit text
    'INDENT_UNIT_TEXT': ' ' * 8,

    # Whether highlight title shows `self` argument's class instead of called
    # function's defining class.
    #
    # This helps reveal the real type of the `self` argument on which the
    # function is called.
    #
    'HIGHLIGHT_TITLE_SHOW_SELF_CLASS': True,

    # Highlight title line character count max
    'HIGHLIGHT_TITLE_LINE_CHAR_COUNT_MAX': 265,

    # Whether show function's file path and line number in pre-call hook
    'SHOW_FUNC_FILE_PATH_LINENO_PRE_CALL': True,

    # Whether show function's file path and line number in post-call hook
    'SHOW_FUNC_FILE_PATH_LINENO_POST_CALL': False,

    # Whether wrapper function should debug info dict's URIs
    'WRAPPER_FUNC_DEBUG_INFO_DICT_URIS': False,

    # Whether printing handler should debug arguments inspect info
    'PRINTING_HANDLER_DEBUG_ARGS_INSPECT_INFO': False,

    # Whether printing handler should debug info dict.
    #
    # Notice info dict contains called function's arguments and printing these
    # arguments may cause errors.
    #
    'PRINTING_HANDLER_DEBUG_INFO_DICT': False,

    # Whether printing handler should debug info dict, excluding arguments.
    #
    # Use this if `PRINTING_HANDLER_DEBUG_INFO_DICT` causes errors.
    #
    'PRINTING_HANDLER_DEBUG_INFO_DICT_SAFE': False,
})


# Add debug logger handler
aoiktracecall.logging.get_debug_logger().addHandler(logging.NullHandler())

# Add info logger handler
aoiktracecall.logging.get_info_logger().addHandler(
    logging.StreamHandler(sys.stdout)
)

# Add error logger handler
aoiktracecall.logging.get_error_logger().addHandler(
    logging.StreamHandler(sys.stderr)
)


# Constant for `highlight`
HL = 'highlight'

# Create trace specs.
#
# The order of the specs determines the matching precedence, with one exception
# that URI patterns consisting of only alphanumerics, underscores, and dots are
# considered as exact URI matching, and will have higher precedence over all
# regular expression matchings. The rationale is that a spec with exact URI
# matching is more specific therefore should not be shadowed by any spec with
# regular expression matching that has appeared early.
#
trace_specs = [
    # ----- aoiktracecall -----
    ('aoiktracecall([.].+)?', False),

    # ----- * -----
    # Tracing `__setattr__` will reveal instances' attribute assignments.
    # Notice Python 2 old-style classes have no `__setattr__` attribute.
    ('.+[.]__setattr__', False),

    # Not trace most of double-underscore functions.
    # Tracing double-underscore functions is likely to break code, e.g. tracing
    # `__str__` or `__repr__` may cause infinite recursion.
    ('.+[.]__(?!init|call)[^.]+__', False),

    # ----- socket._socketobject (Python 2), socket.socket (Python 3) -----
    # Notice in Python 2, class `socket._socketobject`'s instance methods
    # - recv
    # - recvfrom
    # - recv_into
    # - recvfrom_into
    # - send
    # - sendto
    # are dynamically generated in `_socketobject.__init__`. The approach of
    # wrapping class attributes is unable to trace these methods.

    ('socket[.](_socketobject|socket)[.]__init__', HL),

    ('socket[.](_socketobject|socket)[.]bind', HL),

    ('socket[.](_socketobject|socket)[.]listen', HL),

    ('socket[.](_socketobject|socket)[.]connect', HL),

    ('socket[.](_socketobject|socket)[.]accept', HL),

    ('socket[.](_socketobject|socket)[.]setblocking', HL),

    ('socket[.](_socketobject|socket)[.]setsockopt', HL),

    ('socket[.](_socketobject|socket)[.]settimeout', HL),

    ('socket[.](_socketobject|socket)[.]makefile', HL),

    ('socket[.](_socketobject|socket)[.]recv.*', HL),

    ('socket[.](_socketobject|socket)[.]send.*', HL),

    ('socket[.](_socketobject|socket)[.]shutdown', HL),

    ('socket[.](_socketobject|socket)[.]close', HL),

    # ----- socket._fileobject (Python 2), socket.SocketIO (Python 3) -----
    ('socket[.](SocketIO|_fileobject)[.]__init__', HL),

    ('socket[.](SocketIO|_fileobject)[.]readable', True),

    ('socket[.](SocketIO|_fileobject)[.]read.*', HL),

    ('socket[.](SocketIO|_fileobject)[.]writable', True),

    ('socket[.](SocketIO|_fileobject)[.]write.*', HL),

    ('socket[.](SocketIO|_fileobject)[.]flush', HL),

    ('socket[.](SocketIO|_fileobject)[.]close', HL),

    ('socket[.](SocketIO|_fileobject)[.].+', True),

    # ----- socket -----
    ('socket._intenum_converter', False),

    ('socket[.].+[.]_decref_socketios', False),

    ('socket[.].+[.]fileno', False),

    # Ignore to avoid error in `__repr__` in Python 3
    ('socket[.].+[.]getpeername', False),

    # Ignore to avoid error in `__repr__` in Python 3
    ('socket[.].+[.]getsockname', False),

    ('socket[.].+[.]gettimeout', False),

    ('socket([.].+)?', True),

    # ----- select (Python 2) -----
    ('select.select', HL),

    ('select([.].+)?', True),

    # ----- selectors (Python 3) -----
    ('selectors.SelectSelector.__init__', HL),

    ('selectors.SelectSelector.register', HL),

    ('selectors.SelectSelector.select', HL),

    ('selectors([.].+)?', True),

    # ----- SocketServer (Python 2), socketserver (Python 3) -----
    ('SocketServer._eintr_retry', False),

    ('(socketserver|SocketServer)[.]BaseServer[.]__init__', HL),

    ('(socketserver|SocketServer)[.]TCPServer[.]__init__', HL),

    ('(socketserver|SocketServer)[.]ThreadingMixIn[.]process_request', HL),

    (
        '(socketserver|SocketServer)[.]ThreadingMixIn[.]'
        'process_request_thread', HL
    ),

    # Ignore to avoid error:
    # ```
    # 'WSGIServer' object has no attribute '_BaseServer__is_shut_down'
    # ```
    ('(socketserver|SocketServer)[.]ThreadingMixIn[.].+', False),

    ('(socketserver|SocketServer)[.]BaseRequestHandler[.]__init__', HL),

    ('(socketserver|SocketServer)[.].+[.]service_actions', False),

    ('.+[.]server_bind', HL),

    ('.+[.]server_activate', HL),

    ('.+[.]serve_forever', HL),

    ('.+[.]_handle_request_noblock', HL),

    ('.+[.]get_request', HL),

    ('.+[.]verify_request', HL),

    ('.+[.]process_request', HL),

    ('.+[.]process_request_thread', HL),

    ('.+[.]finish_request', HL),

    ('.+[.]setup', HL),

    ('.+[.]handle', HL),

    ('.+[.]finish', HL),

    ('.+[.]shutdown_request', HL),

    ('.+[.]close_request', HL),

    ('.+[.]fileno', False),

    ('(socketserver|SocketServer)([.].+)?', True),

    # ----- twisted -----
    # Ignore to avoid error
    ('twisted[.](.+)Mixin[.]__init__', False),

    ('twisted.internet.abstract.FileDescriptor.__init__', HL),

    ('twisted.internet.abstract.FileDescriptor._maybePauseProducer', HL),

    ('twisted.internet.abstract.FileDescriptor.doWrite', HL),

    ('twisted.internet.abstract.FileDescriptor.startReading', HL),

    ('twisted.internet.abstract.FileDescriptor.startWriting', HL),

    ('twisted.internet.abstract.FileDescriptor.stopWriting', HL),

    ('twisted.internet.abstract.FileDescriptor.write', HL),

    ('twisted.internet.base.BasePort.createInternetSocket', HL),

    ('twisted.internet.base.DelayedCall.__init__', HL),

    ('twisted.internet.base.DelayedCall.activate_delay', HL),

    ('twisted.internet.base.ReactorBase._insertNewDelayedCalls', HL),

    ('twisted.internet.base.ReactorBase.callLater', HL),

    ('twisted.internet.base.ReactorBase.fireSystemEvent', HL),

    ('twisted.internet.base.ReactorBase.runUntilCurrent', HL),

    ('twisted.internet.base.ReactorBase.startRunning', HL),

    ('twisted.internet.base.ReactorBase.stop', HL),

    ('twisted.internet.base.ReactorBase.timeout', HL),

    ('twisted.internet.base._SignalReactorMixin.mainLoop', HL),

    ('twisted.internet.base._SignalReactorMixin.run', HL),

    ('twisted.internet.base._SignalReactorMixin.startRunning', HL),

    ('twisted.internet.defer.Deferred.__init__', HL),

    ('twisted.internet.defer.Deferred._runCallbacks', HL),

    ('twisted.internet.defer.Deferred._startRunCallbacks', HL),

    ('twisted.internet.defer.Deferred.callback', HL),

    ('twisted.internet.defer.execute', HL),

    ('twisted.internet.defer.succeed', HL),

    ('twisted.internet.endpoints.TCP4ServerEndpoint.__init__', HL),

    ('twisted.internet.endpoints._TCPServerEndpoint.__init__', HL),

    ('twisted.internet.endpoints._TCPServerEndpoint.listen', HL),

    ('twisted.internet.posixbase.PosixReactorBase.listenTCP', HL),

    ('twisted.internet.protocol.BaseProtocol.connectionMade', HL),

    ('twisted.internet.protocol.BaseProtocol.makeConnection', HL),

    ('twisted.internet.protocol.Factory.buildProtocol', HL),

    ('twisted.internet.protocol.Factory.doStart', HL),

    ('twisted.internet.selectreactor.SelectReactor._doReadOrWrite', HL),

    ('twisted.internet.selectreactor.SelectReactor.addReader', HL),

    ('twisted.internet.selectreactor.SelectReactor.addWriter', HL),

    ('twisted.internet.selectreactor.SelectReactor.doIteration', HL),

    ('twisted.internet.tcp.Connection.__init__', HL),

    ('twisted.internet.tcp.Connection._dataReceived', HL),

    ('twisted.internet.tcp.Connection.doRead', HL),

    ('twisted.internet.tcp.Connection.writeSomeData', HL),

    ('twisted.internet.tcp.Port.__init__', HL),

    ('twisted.internet.tcp.Port.createInternetSocket', HL),

    ('twisted.internet.tcp.Port.doRead', HL),

    ('twisted.internet.tcp.Port.startListening', HL),

    ('twisted.internet.tcp.Server.__init__', HL),

    ('twisted.python.context.ContextTracker.callWithContext', HL),

    # Ignore to avoid error
    ('twisted.python.deprecate', False),

    ('twisted.python.log.callWithContext', HL),

    ('twisted.python.log.callWithLogger', HL),

    ('twisted.python.threadable.registerAsIOThread', HL),

    ('twisted([.].+)?', True),

    # ----- __main__ -----
    ('__main__', True),

    ('__main__.main', HL),

    ('__main__.EchoProtocol', True),

    ('__main__.EchoProtocol.__init__', HL),

    ('__main__.EchoProtocol.dataReceived', HL),
]


# Trace calls according to trace specs.
#
# This function will hook the module importing system in order to intercept and
# process newly imported modules. Callables in these modules which are matched
# by one of the trace specs will be wrapped to enable tracing.
#
# Already imported modules will be processed as well. But their callables may
# have been referenced elsewhere already, making the tracing incomplete. This
# explains why import hook is needed and why modules must be imported after
# `trace_calls_in_specs` is called.
#
aoiktracecall.trace.trace_calls_in_specs(specs=trace_specs)


# Import modules after `trace_calls_in_specs` is called
import socket

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol


class EchoProtocol(Protocol):
    """
    This protocol echoes request body in response body.
    """

    def __init__(self):
        pass

    def close_reactor(self):
        # Close connection
        self.transport.socket.shutdown(socket.SHUT_WR)

        # Stop reactor
        self.transport.reactor.stop()

    def dataReceived(self, data):
        # Write response data
        self.transport.write(data)

        # Add callback to close reactor
        reactor.callLater(0.5, self.close_reactor)


def main():
    try:
        # Create end point
        endpoint = TCP4ServerEndpoint(
            reactor=reactor,
            port=8000,
            interface='127.0.0.1',
        )

        # Start listening
        endpoint.listen(Factory.forProtocol(EchoProtocol))

        # Run reactor
        reactor.run()

    # If have `KeyboardInterrupt`
    except KeyboardInterrupt:
        # Stop gracefully
        pass


# Trace calls in this module.
#
# Calling this function is needed because at the point `trace_calls_in_specs`
# is called, this module is being initialized, therefore callables defined
# after the call point are not accessible to `trace_calls_in_specs`.
#
aoiktracecall.trace.trace_calls_in_this_module()


# If is run as main module
if __name__ == '__main__':
    # Call main function
    exit(main())
