'''
This implements a syntax highlighter for C code using PyQt5's QSyntaxHighlighter. It defines various formatting rules for keywords, types, functions, numbers, strings,
 comments, and preprocessor directives to enhance the readability of C code in a QTextEdit widget.
'''

from PyQt5 import QtGui, QtCore

class CCodeHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
            'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void',
            'volatile', 'while', 'include', 'define'
        ]
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor("#81A1C1"))
        keyword_format.setFontWeight(QtGui.QFont.Bold)
        for word in keywords:
            pattern = QtCore.QRegExp(f'\\b{word}\\b')
            self.highlighting_rules.append((pattern, keyword_format))

        self.comment_format = QtGui.QTextCharFormat()
        self.comment_format.setForeground(QtGui.QColor("#616E88"))
        self.comment_format.setFontItalic(True)
        self.highlighting_rules.append((QtCore.QRegExp('//[^\n]*'), self.comment_format))
        self.highlighting_rules.append((QtCore.QRegExp('/\\*.*?\\*/'), self.comment_format))

        self.string_format = QtGui.QTextCharFormat()
        self.string_format.setForeground(QtGui.QColor("#A3BE8C"))
        self.highlighting_rules.append((QtCore.QRegExp('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), self.string_format))

        self.preprocessor_format = QtGui.QTextCharFormat()
        self.preprocessor_format.setForeground(QtGui.QColor("#B48EAD"))
        self.highlighting_rules.append((QtCore.QRegExp('#[A-Za-z]+'), self.preprocessor_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)