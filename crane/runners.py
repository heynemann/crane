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

import time
from datetime import datetime

from crane.parsers import Parser, VariableAssignment
from crane.context import Context, LogEntry, TargetNotFoundError

Successful = "Successful"
Failed = "Failed"
Unknown = "Unknown"

class Runner(object):
    def __init__(self, verbosity=2, parser=None, executer=None):
        self.parser = parser or Parser()
        self.executer = executer or TargetExecuter()
        self.verbosity = verbosity

    def run(self, script, target):
        start_secs = time.time()
        build_structure = self.parser.parse_script(script)
        if target.lower() not in build_structure.targets:
            raise TargetNotFoundError(target)

        actual_target = build_structure.targets[target.lower()]

        context = Context(RunResult(), build_structure)
        context.run_result.start_time = datetime.now()

        for variable, assignment in build_structure.variable_assignments.iteritems():
            context.assign_variable(assignment.variable, assignment.value)

        self.executer.execute_target(build_structure=build_structure, target=actual_target, context=context)

        context.run_result.log = "\n".join([entry.render(self.verbosity) for entry in context.log_entries])
        context.run_result.status = Successful
        context.run_result.end_time = datetime.now()
        context.run_result.ellapsed = time.time() - start_secs
        return context.run_result

class TargetExecuter(object):
    def execute_target(self, build_structure, target, context):
        for action_to_execute in target.actions:
            action_to_execute(context)

class RunResult(object):
    def __init__(self):
        self.log = ''
        self.status = Unknown
        self.start_time = None
        self.end_time = None
