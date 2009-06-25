#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Bernardo Heynemann <heynemann@gmail.com>
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

ACTIONS = []

class ActionNotFoundError(Exception):
    pass

class ActionFailedError(Exception):
    pass
    
class ActionRegistry(object):
    @classmethod
    def suitable_for(cls, line):
        for Action in ACTIONS:
            regex = Action.regex

            if isinstance(regex, basestring):
                Action.regex = re.compile(regex)

            matches = Action.regex.match(line)

            if matches:
                args = matches.groups()
                kw = matches.groupdict()
                for k, v in kw.items():
                    del kw[k]
                    kw[str(k)] = v
                
                if kw:
                    args = []
                return Action, args, kw

        return None, None, None
    
class MetaActionBase(type):
    def __init__(cls, name, bases, attrs):
        if name not in ('ActionBase', ):
            if 'execute' not in attrs:
                raise NotImplementedError("The action %s does not implement the method execute()" % name)
            if 'regex' not in attrs:
                raise NotImplementedError("The action %s does not implement the attribute regex" % name)

            if not isinstance(attrs['regex'], basestring):
                regex = attrs['regex']
                raise TypeError("%s.regex attribute must be a string, got %r(%r)." % (cls.__name__, regex, type(regex).__name__))

            # registering
            ACTIONS.append(cls)

        super(MetaActionBase, cls).__init__(name, bases, attrs)

class ActionBase(object):
    __metaclass__ = MetaActionBase
    failed = ActionFailedError

#    def execute_action(self, line):
#        Action, args, kwargs = ActionRegistry.suitable_for(line)

#        if not Action:
#            raise ActionNotFoundError(line, None, None)

#        if isinstance(self, Action):
#            raise RuntimeError('A action can not execute itself for infinite recursion reasons :)')

#        action_to_execute = Action()
#        action_to_execute.execute(*args, **kwargs)

