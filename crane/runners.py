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

from crane.parsers import Parser
from crane.context import Context, LogEntry

Successful = "Successful"
Failed = "Failed"
Unknown = "Unknown"

class Runner(object):
    def __init__(self, parser=None, executer=None):
        self.parser = parser or Parser()
        self.executer = executer or TargetExecuter()

    def run(self, script, target):
        build_structure = self.parser.parse_script(script)
        actual_target = build_structure.targets[target]

        result = self.executer.execute_target(build_structure, actual_target)
        return result

class TargetExecuter(object):
    def execute_target(self, build_structure, target):
        context = Context(RunResult(), build_structure)

        context.run_result.start_time = datetime.now()

        for action_to_execute in target.actions:
            action_type = action_to_execute.action_type
            action_type().execute(context, *action_to_execute.args, **action_to_execute.kw)
        
        context.run_result.log = "\n".join([unicode(entry) for entry in context.log_entries])
        context.run_result.status = Successful
        context.run_result.end_time = datetime.now()

        return context

class RunResult(object):
    def __init__(self):
        self.log = ''
        self.status = Unknown
        self.start_time = None
        self.end_time = None
