#!/usr/bin/python
#    Copyright 2013, 2014 Joshua Charles Campbell, Alex Wilson, Eddie Santos
#
#    This file is part of UnnaturalCode.
#    
#    UnnaturalCode is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    UnnaturalCode is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with UnnaturalCode.  If not, see <http://www.gnu.org/licenses/>.


import sys
from copy import copy
import token

from unnaturalcode.util import *
from unnaturalcode.source import Source, Lexeme, Position
from logging import debug, info, warning, error

from unnaturalcode import flexibleTokenize


try:
  from cStringIO import StringIO
except ImportError:
  from io import StringIO

COMMENT = 53

ws = re.compile('\s')


# TODO: Refactor so base class is genericSource

class pythonLexeme(Lexeme):
    
    @classmethod
    def stringify_build(cls, t, v):
        """
        Stringify a lexeme: produce a string describing it.
        In the case of comments, strings, indents, dedents, and newlines, and
        the endmarker, a string with '<CATEGORY-NAME>' is returned.  Else, its
        actual text is returned.
        """
        if t == 'COMMENT':
            return '<'+t+'>'
        # Josh though this would be a good idea for some strange reason:
        elif len(v) > 20 :
            return '<'+t+'>'
        elif ws.match(str(v)) :
            return '<'+t+'>'
        elif t == 'STRING' :
            return '<'+t+'>'
        elif len(v) > 0 :
            return v
        else:
            # This covers for <DEDENT> case, and also, probably some other
            # special cases...
            return '<' + t + '>'
    
    @classmethod
    def fromTuple(cls, tup):
        if isinstance(tup[0], int):
            t0 = token.tok_name[tup[0]]
        else:
            t0 = tup[0]
        new = tuple.__new__(cls, (t0, tup[1], Position(tup[2]), Position(tup[3]),  cls.stringify_build(t0, tup[1])))
        return new
          
    def comment(self):
        return (self.ltype == 'COMMENT')
      

class pythonSource(Source):
    
    lexemeClass = pythonLexeme
    
    def lex(self, code, mid_line=False):
        tokGen = flexibleTokenize.generate_tokens(StringIO(code).readline,
            mid_line)
        return [pythonLexeme.fromTuple(t) for t in tokGen]
    
   
    def unCommented(self):
        assert len(self)
        return filter(lambda a: not a.comment(), copy(self))
    
    def scrubbed(self):
        """Clean up python source code removing extra whitespace tokens and comments"""
        ls = copy(self.lexemes)
        assert len(ls)
        i = 0
        r = []
        for i in range(0, len(ls)):
            if ls[i].comment():
                continue
            elif ls[i].ltype == 'NL':
                continue
            elif ls[i].ltype == 'NEWLINE' and i < len(ls)-1 and ls[i+1].ltype == 'NEWLINE':
                continue
            elif ls[i].ltype == 'NEWLINE' and i < len(ls)-1 and ls[i+1].ltype == 'INDENT':
                continue
            else:
                r.append(ls[i])
        assert len(r)
        return pythonSource(r)

class LexPyMQ(object):
	def __init__(self, lexer):
		self.lexer = lexer
		self.zctx = zmq.Context()
		self.socket = self.zctx.socket(zmq.REP)

	def run(self):
		self.socket.bind("tcp://lo:32132")

		while True:
			msg = self.socket.recv_json(0)
			# there are definitely new lines in the code
			assert msg.get('python'), 'received non-python code'
			code = msg.get('body', '')
			self.socket.send_json(list(tokenize.generate_tokens(StringIO(code).readline)))

if __name__ == '__main__':
	LexPyMQ(LexPy()).run()
