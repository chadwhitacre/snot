"""Hack test output to pop the tb info we care about.
"""
import os
import pprint
import re
import sys
import traceback


# py.test
# =======

try:
    import pytest
except ImportError:
    pass
else:
    import _pytest as SnotPyTest


# nose
# ====

try:
    import nose
except ImportError:
    pass
else:
    from _nose import SnotNose


# Highlighting
# ============

class Highlighter:

    def __init__(self, pattern, highlight):
        self.__pattern = re.compile(pattern)
        self.__highlight = highlight

    def highlight(self, line):
        return self.__pattern.sub(self.__highlight, line)


fileinfo_highlighter = Highlighter( r'^(.*"/?(?:.*/)*)([^"]+)", line (\d+)'
                                  , r'\1\033[1;31m\2\033[0m", line \033[1;31m\3\033[0m'
                                   )

def colorize_traceback_lines(lines):
    """Given a list of str, colorize some of them in place.
    """
    nlines = len(lines)
    if nlines > 1:

        # Highlight the error message.
        lines[-1] = exc_highlighter.highlight(lines[-1])

        # Highlight the file at the bottom of the stack.
        i = -2
        if lines[i].strip() == '^':
            # For a SyntaxError we get a line of code and a caret indicating a
            # position in that line. Back up two more line in that case.
            i = -4
        lines[i] = fileinfo_highlighter.highlight(lines[i])

        # Highlight the file with the breaking test.
        for i in range(nlines):
            if 'test_' in lines[i]:
                lines[i] = fileinfo_highlighter.highlight(lines[i])
                break

def _exc_highlighter(match):
    exc = match.group(1)
    msg = match.group(2)
    msg = '\033[1;36m' + msg + '\033[0m'
    return '\033[1;31m' + exc + '\033[0m: ' + msg

exc_highlighter = Highlighter(r'^([^:]+): (.*)$', _exc_highlighter)



# unittest
# ========

def _exc_and_assert_highlighter(match):
    exc = match.group(1)
    msg = match.group(2)
    if exc == 'AssertionError':
        try:
            # If an AssertionError gives us a Python data structure, we want to
            # format that nicely.
            msg = eval(msg)
            msg = pprint.pformat(msg, width=75)
            if os.linesep in msg:
                msg = os.linesep.join(['    ' + x for x in msg.splitlines()])
                msg = os.linesep + os.linesep + msg
        except:
            pass
    msg = '\033[1;36m' + msg + '\033[0m'
    return '\033[1;31m' + exc + '\033[0m: ' + msg

exc_and_assert_highlighter = Highlighter( r'^([^:]+): (.*)$'
                                        , _exc_and_assert_highlighter
                                         )

def _exc_info_to_string(self, err, test):
    """Converts a sys.exc_info()-style tuple of values into a string.

    Overriden to add ANSI color escapes at key moments.

    """
    exctype, value, tb = err
    # Skip test runner traceback levels
    while tb and self._is_relevant_tb_level(tb):
        tb = tb.tb_next

    if exctype is test.failureException:
        # Skip assert*() traceback levels
        length = self._count_relevant_tb_levels(tb)
        msgLines = traceback.format_exception(exctype, value, tb, length)
    else:
        msgLines = traceback.format_exception(exctype, value, tb)

    ############################### begin new
    #
    colorize_traceback_lines(msgLines)  # operates in-place

    if hasattr(self, 'buffer'):
        # This part is a red-hot hack.
        # https://github.com/whit537/snot/pull/1
        output = error = ""
        if hasattr(sys.stdout, 'getvalue'):
            output = sys.stdout.getvalue()
        if hasattr(sys.stderr, 'getvalue'):
            error = sys.stderr.getvalue()

        # These are constants from unittest/result.py.
        STDOUT_LINE = '\nStdout:\n%s'
        STDERR_LINE = '\nStderr:\n%s'
    #
    ############################### end new

        if output:
            if not output.endswith('\n'):
                output += '\n'
            msgLines.append(STDOUT_LINE % output)
        if error:
            if not error.endswith('\n'):
                error += '\n'
            msgLines.append(STDERR_LINE % error)
    return ''.join(msgLines)


is_installed = False

def install(unittest):
    """Monkey-patch unittest with snot highlighter.
    """
    global is_installed
    is_installed = True
    unittest.TestResult._exc_info_to_string = _exc_info_to_string
