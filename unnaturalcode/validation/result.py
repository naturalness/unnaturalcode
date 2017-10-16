#!/usr/bin/python
#    Copyright 2013, 2014, 2017 Joshua Charles Campbell
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

import logging
logger = logging.getLogger(__name__)
DEBUG = logger.debug
INFO = logger.info
WARNING = logger.warning
ERROR = logger.error
CRITICAL = logger.critical


class Result(object):
    @classmethod
    def column_names(cls):
        return [i % (cls.db_name)
                for i in [
                    "%s_rank",
                    "%s_index",
                    "%s_start_line",
                    "%s_start_col",
                    "%s_end_line",
                    "%s_end_col",
                    "%s_token_type",
                    "%s_token_value",
                    "%s_operation"
                ]
            ]
    
    def __init__(self, suggestions, vfile):
        self.vfile = vfile
        self.suggestions = suggestions
        rank = 2147483648
        for i in range(0, len(suggestions)):
            rank = i + 1
            suggestion = suggestions[i] 
            if self.hit(suggestion):
                self.rank = rank
                self.index = suggestion.token_index
                self.start_line = suggestion.change_start[0]
                self.start_col = suggestion.change_start[1]
                self.end_line = suggestion.change_end[0]
                self.end_col = suggestion.change_end[1]
                self.token_type = suggestion.change_token.type
                self.token_value = suggestion.change_token.value
                self.operation = suggestion.opcode
        if not hasattr(self, 'rank'):
            self.rank = None
            self.index = None
            self.start_line = None
            self.start_col = None
            self.end_line = None
            self.end_col = None
            self.token_type = None
            self.token_value = None
            self.operation = None
    
    def save(self, values, test):
        values[test.columns.index("%s_rank" % self.db_name)] = self.rank
        values[test.columns.index("%s_index" % self.db_name) ] = self.index
        values[test.columns.index("%s_start_line" % self.db_name)] = self.start_line
        values[test.columns.index("%s_start_col" % self.db_name)] = self.start_col
        values[test.columns.index("%s_end_line" % self.db_name)] = self.end_line
        values[test.columns.index("%s_end_col" % self.db_name)] = self.end_col
        values[test.columns.index("%s_token_type" % self.db_name)] = self.token_type
        values[test.columns.index("%s_token_value" % self.db_name)] = self.token_value
        values[test.columns.index("%s_operation" % self.db_name)] = self.operation
        return values

class LineLocation(Result):
    db_name = "line_location"
    def hit(self, suggestion):
        if suggestion.change_start.line == self.vfile.change.change_start[0]:
            return True
        else:
            return False
    
class WindowLocation(Result):
    db_name = "window_location"
    def hit(self, suggestion):
        if (suggestion.token_index >= (self.vfile.change.token_index - 10)
            and suggestion.token_index < (self.vfile.change.token_index - 10)):
            return True
        else:
            return False

class ExactLocation(Result):
    db_name = "exact_location"
    def hit(self, suggestion):
        if suggestion.token_index == self.vfile.change.token_index:
            return True
        else:
            return False
    
class ValidFix(Result):
    db_name = "valid_fix"
    def hit(self, suggestion):
        if suggestion.token_index == self.vfile.change.token_index:
            test = suggestion.do(self.vfile.bad_lexed)
            return (len(test.check_syntax()) == 0)
        else:
            return False
    
class TrueFix(Result):
    db_name = "true_fix"
    def hit(self, suggestion):
        if suggestion.token_index == self.vfile.change.token_index:
            return self.vfile.change.reverse().approx_equal(suggestion)
        else:
            return False
        