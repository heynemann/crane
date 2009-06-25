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

from crane.parsers import LogEntry

def test_can_create_log_entry():
    entry = LogEntry("message")
    assert entry
    assert isinstance(entry, LogEntry)
    
def test_created_log_entry_keeps_message():
    entry = LogEntry("message")
    assert entry.message == "message"

def test_created_log_entry_has_timestamp():
    entry = LogEntry("message")
    assert entry.timestamp

def test_created_log_entry_str_works():
    entry = LogEntry("message")
    assert re.match(r'^\[(.+)\] message$', str(entry))

def test_created_log_entry_unicode_works():
    entry = LogEntry("message")
    assert re.match(r'^\[(.+)\] message$', unicode(entry))

