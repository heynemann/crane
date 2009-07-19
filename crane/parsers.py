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

from crane.tokenizer import Tokenizer, TargetToken, ActionToken, IndentToken, DedentToken, VariableAssignmentToken
from crane.actions import ActionBase, ActionRegistry, ActionNotFoundError
from crane.actions.base_actions import *
from crane.context import Context, LogEntry

class ParsedBuildStructure(object):
    def __init__(self):
        self.variable_assignments = {}
        self.targets = {}

    def process_token(self, token):
        target = Target(token.name)
        self.targets[token.name.lower()] = target
        return target

class Target(object):
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.variable_assignments = {}

    def process_token(self, token):
        action_type, args, kw = ActionRegistry.suitable_for(token.line)
        if not action_type:
            raise ActionNotFoundError("The action for the line \"%s\" was not found. Are you sure you have that action right?" % token.line)

        action = lambda context: action_type().execute_action(context, *args, **kw)
        self.actions.append(action)

class Action(object):
    def __init__(self, action_type, args, kw):
        self.action_type = action_type
        self.args = args
        self.kw = kw

class VariableAssignment(object):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

class Parser(object):
    def parse_script(self, script):
        structure = ParsedBuildStructure()
        
        tokens = Tokenizer.tokenize(script)

        current_target = None
        for token in tokens:
            if isinstance(token, IndentToken):
                continue

            if isinstance(token, DedentToken):
                current_target = None
                continue

            if isinstance(token, VariableAssignmentToken):
                if current_target:
                    assignment = lambda context, token=token: context.assign_variable(token.variable, token.value)

                    current_target.actions.append(assignment)
                    continue

                assignment = VariableAssignment(variable=token.variable, value=token.value)
                structure.variable_assignments[assignment.variable] = assignment
                continue

            if isinstance(token, TargetToken):
                current_target = structure.process_token(token)
                continue

            if isinstance(token, ActionToken):
                current_target.process_token(token)
                continue

        return structure


