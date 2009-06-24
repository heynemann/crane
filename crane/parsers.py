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

from crane.tokenizer import Tokenizer, TargetToken, ActionToken
from crane.actions import Action

class ParsedBuildStructure(object):
    def __init__(self):
        self.targets = {}
    
    def add_target(self, target_name):
        target = Target(target_name)
        self.targets[target_name] = target
        
class Target(object):
    def __init__(self, name):
        self.name = name
        self.actions = []

    def add_action(self, action_text):
        action = Action(action_text)
        self.targets.append(target)

class Parser(object):
    def parse_script(self, script):
        structure = ParsedBuildStructure()
        
        tokens = Tokenizer.tokenize(script)

        for token in tokens:
            if isinstance(token, TargetToken):
                current_target = structure.add_target(token.name)

        return structure
