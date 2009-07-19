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
from datetime import datetime

class LogEntry(object):
    def __init__(self, message, append_time=True):
        if not append_time:
            self.timestamp = None
        else:
            self.timestamp = datetime.now()
        self.message = message

    def __str__(self):
        return self.render(2)

    def __unicode__(self):
        return self.render(2)

    def render(self, verbosity):
        if verbosity > 1 and self.timestamp:
            return "[%s] %s" % (self.timestamp.strftime("%H:%M:%S"), self.message)
        return "%s" % self.message

class Context(object):
    def __init__(self, run_result=None, build_structure=None):
        self.run_result = run_result
        self.build_structure = build_structure
        self.log_entries = []
        self.variables = {}

    def log(self, message, append_time=True):
        self.log_entries.append(LogEntry(message, append_time))

    def assign_variable(self, variable, value):
        self.variables[variable] = self.expand_variable(value)

    def expand_variable(self, value):
        if not value:
            return value
        for k, v in self.variables.iteritems():
            value = re.sub("(?P<white>([^$]|^))[$]{1,1}%s" % k, "\g<white>%s" % v, value)
            value = value.replace("$$","$")

        return value

class TargetNotFoundError(ValueError):
    pass
