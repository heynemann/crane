#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Copyright Bernardo Heynemann <heynemann@gmail.com>

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

WORD_REGEX = '["\']?(?P<word>.*[^"\'])["\']?'

class Tokenizer(object):
    @classmethod
    def tokenize(cls, script):
        tokens = []
        non_indented_tokens = []
        
        indent_level = 0
        line_index = 0
        for line in script.splitlines():
            line_index += 1
            if not line.strip(): 
                continue
            if line.strip().startswith("#"):
                continue
            line_indent_level = cls.get_indent_level(line)
            
            if line_indent_level > indent_level:
                indent_level = line_indent_level
                tokens.append(IndentToken())
            if line_indent_level < indent_level:
                indent_level = line_indent_level
                tokens.append(DedentToken())

            assignment = cls.get_variable_assignment(line)
            if assignment:
                tokens.append(assignment)
                non_indented_tokens.append(assignment)
                continue

            target = cls.get_target(line)
            if target:
                if non_indented_tokens and isinstance(non_indented_tokens[-1], TargetToken):
                    cls.raise_invalid_target_tokenize_error(line_index, line, non_indented_tokens[-1])
                tokens.append(target)
                non_indented_tokens.append(target)
                continue

            if non_indented_tokens and isinstance(non_indented_tokens[-1], (TargetToken, ActionToken)):
                action = ActionToken(line=line.strip())
                tokens.append(action)
                non_indented_tokens.append(action)
                continue
            
            raise TokenizerError('An action("%s") was found when a TargetToken was expected in line %d.' %
                                  (line.strip(), line_index))
            
        return tuple(tokens)

    @classmethod
    def get_indent_level(cls, line):
        r = r'^(\s*)'
        match = re.match(r, line)

        return len(match.groups()[0])

    @classmethod
    def get_target(cls, line):
        r = r'on (?P<target_name>\w+) do'
        search = re.search(r, line)

        if not search:
            return None

        return TargetToken(search.groups()[0])

    @classmethod
    def get_variable_assignment(cls, line):
        r = r'set (?P<variable_name>\w+) to %s' % WORD_REGEX

        search = re.search(r, line)

        if not search:
            return None

        d = search.groupdict()
        return VariableAssignmentToken(d["variable_name"], d["word"])

    @classmethod
    def raise_invalid_target_tokenize_error(cls, line_index, line, token):
        raise TokenizerError("A target was found when an ActionToken was expected in line %d. TargetToken found after \"%s\" target." % (line_index, token.name))
        
class Token(object):
    pass

class IndentToken(Token):
    pass

class DedentToken(Token):
    pass

class TargetToken(Token):
    def __init__(self, name):
        self.name = name

class ActionToken(Token):
    def __init__(self, line):
        self.line = line

class VariableAssignmentToken(Token):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

class TokenizerError(Exception):
    pass
