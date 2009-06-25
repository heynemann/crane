#!/usr/bin/env python
# -*- coding:utf-8 -*-

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

import os
from subprocess import Popen, PIPE
import commands

class ShellExecuter(object):
    def execute(self, command, base_path, change_dir=True):
        try:
            if os.name == "nt":
                proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=base_path, shell=True)
                log = "\n".join(proc.communicate())
                exit_code = proc.returncode
            else:
                complement=""
                if change_dir:
                    complement = "cd %s && " % base_path
                result = commands.getstatusoutput("%s%s" % (complement, command))
                log = result[1]
                exit_code = result[0]

            return ExecuteResult(command, log, exit_code)
        except Exception, err:
            error_message = "An error occured while executing command %s: %s" % (command, err)
            return ExecuteResult(command, error_message, 1)

class ExecuteResult(object):
    def __init__(self, command, run_log, exit_code):
        self.command = command
        self.run_log = run_log
        self.exit_code = exit_code

