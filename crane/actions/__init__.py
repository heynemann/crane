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

import os
from os.path import exists, abspath
import re

from crane.actions.shell_executer import ShellExecuter, ExecuteResult

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

class ActualFileSystem(object):
    def __init__(self):
        self.executer = ShellExecuter()

    def create_directory(self, path):
        os.mkdir(path)

    def remove_directory(self, path):
        os.removedirs(path)
    
    def directory_exists(self, path):
        return exists(path)

class ActionBase(object):
    __metaclass__ = MetaActionBase
    failed = ActionFailedError

    def __init__(self, file_system=None):
        self.file_system = file_system and file_system or ActualFileSystem()

    def execute_shell(self, script, base_path=None):
        base_path = base_path or abspath(os.curdir)
        return self.file_system.executer.execute(script, base_path)

    def execute_action(self, context, *args, **kw):
        for i in range(len(args)):
            args[i] = context.expand_variable(args[i])

        for k, v in kw.iteritems():
            kw[k] = context.expand_variable(kw[k])

        return self.execute(context, *args, **kw)

#    def execute_action(self, line):
#        Action, args, kwargs = ActionRegistry.suitable_for(line)

#        if not Action:
#            raise ActionNotFoundError(line, None, None)

#        if isinstance(self, Action):
#            raise RuntimeError('A action can not execute itself for infinite recursion reasons :)')

#        action_to_execute = Action()
#        action_to_execute.execute(*args, **kwargs)

