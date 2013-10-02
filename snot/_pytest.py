import py._code.code


_ReprEntryNative = py._code.code.ReprEntryNative

class SnottyReprEntryNative(py._code.code.ReprEntryNative):

    def toterminal(self, tw):
        """Extend to provide traceback highlighting.
        """
        from snot import colorize_traceback_lines
        colorize_traceback_lines(self.lines)
        return _ReprEntryNative.toterminal(self, tw)

py._code.code.ReprEntryNative = SnottyReprEntryNative
