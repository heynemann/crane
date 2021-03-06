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

from crane import Parser, ParsedBuildStructure
from crane.actions import ActionNotFoundError, ActionBase

from utils import assert_raises

test_show_something_script = """
on test do
    show('something')
    """

test_dummy_script = """
on test do
    dummy
    """

class ShowAction(ActionBase):
    regex = r"show\('(?P<message>\w+)'\)"

    def execute(self, message):
        print message

def test_can_create_parser():
    parser = Parser()
    assert parser is not None
    
def test_parse_script_returns_ParsedBuildStructure():
    parser = Parser()
    result = parser.parse_script(test_show_something_script)
    assert result

def test_parse_script_returns_ParsedBuildStructure():
    parser = Parser()
    result = parser.parse_script(test_show_something_script)
    assert isinstance(result, ParsedBuildStructure)

def test_parsed_script_contains_one_target():
    parser = Parser()
    result = parser.parse_script(test_show_something_script)
    assert len(result.targets) == 1

def test_script_parser_raises_when_action_not_found():
    parser = Parser()
    
    assert_raises(ActionNotFoundError, parser.parse_script, test_dummy_script, exc_pattern=r'The action for the line \"dummy\" was not found. Are you sure you have that action right?')

