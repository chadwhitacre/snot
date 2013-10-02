import unittest

import snot
from nose.plugins import Plugin
from nose.plugins.capture import Capture
from nose.util import ln


class SnotNose(Capture):
    """Snot is colored output from nose.
    """

    name = "snot"

    def __init__(self, *a, **kw):
        snot.install(unittest)  # This is the real work. Nose uses unittest.
        Capture.__init__(self, *a, **kw)

    def help(self):
        return self.__doc__

    def options(self, parser, env):
        """Override to un-conflict options with parent plugin.
        """
        Plugin.options(self, parser, env)

    def addCaptureToErr(self, ev, output):
        """Override to highlight captured output.
        """
        return '\n'.join([ str(ev)
                         , ln('>> begin captured stdout <<')
                         , '\033[1;36m' + output + '\033[0m'
                         , ln('>> end captured stdout <<')
                          ])
