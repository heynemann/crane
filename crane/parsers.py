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

from datetime import datetime

from crane.tokenizer import Tokenizer, TargetToken, ActionToken, IndentToken, DedentToken
from crane.actions import ActionBase, ActionRegistry, ActionNotFoundError

class LogEntry(object):
    def __init__(self, message):
        self.timestamp = datetime.now()
        self.message = message

    def __str__(self):
        return self.__unicode__()
    
    def __unicode__(self):
        return "[%s] %s" % (self.timestamp, self.message)

class ParsedBuildStructure(object):
    def __init__(self):
        self.targets = {}
        self.log_entries = []

    def process_token(self, token):
        target = Target(token.name)
        self.targets[token.name] = target
        return target
    
    def log(self, message):
        self.log_entries.append(LogEntry(message))

class Target(object):
    def __init__(self, name):
        self.name = name
        self.actions = []

    def process_token(self, token):
        action_type, args, kw = ActionRegistry.suitable_for(token.line)
        if not action_type:
            raise ActionNotFoundError("The action for the line \"%s\" was not found. Are you sure you have that action right?" % token.line)

        action = Action(action_type, args, kw)
        self.actions.append(action)
        return action

class Action(object):
    def __init__(self, action_type, args, kw):
        self.action_type = action_type
        self.args = args
        self.kw = kw

class Parser(object):
    def parse_script(self, script):
        structure = ParsedBuildStructure()
        
        tokens = Tokenizer.tokenize(script)

        current_target = None
        for token in tokens:
            if isinstance(token, (IndentToken, DedentToken)):
                continue

            if isinstance(token, TargetToken):
                current_target = structure.process_token(token)
                continue

            if isinstance(token, ActionToken):
                current_action = current_target.process_token(token)
                continue

        return structure


