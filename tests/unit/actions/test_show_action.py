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

from crane.parsers import ParsedBuildStructure
from crane.actions.base_actions import ShowAction
from crane.context import Context

def test_show_action_execute_method_appends_text_to_build_structure():
    context = Context(None, None)
    action = ShowAction()
    action.execute(context, "some text")
    
    assert len(context.log_entries) == 2
    assert context.log_entries[0].message == "some text"
    assert context.log_entries[1].message == "\n"

def test_show_action_execute_method_appends_newline_if_no_text():
    context = Context(None, None)
    action = ShowAction()
    action.execute(context, "")
    
    assert len(context.log_entries) == 1
    assert context.log_entries[0].message == "\n"

