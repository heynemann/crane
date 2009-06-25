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

from pmock import *

from crane.parsers import ParsedBuildStructure
from crane.actions.base_actions import *
from crane.context import Context, LogEntry

from ..utils import assert_raises

def test_create_directory_action_should_call_create_directory():
    mock_file_system = Mock()
    mock_file_system.expects(once()).directory_exists(eq("/some/path")).will(return_value(False))
    mock_file_system.expects(once()).create_directory(eq("/some/path"))
    context = Context(None, None)
    
    action = CreateDirectoryAction(file_system=mock_file_system)
    action.execute(context, "/some/path")
    
    assert len(context.log_entries) == 1
    assert context.log_entries[0].message == "Directory created at /some/path"

def test_create_directory_action_should_raise_if_directory_already_exists():
    mock_file_system = Mock()
    mock_file_system.expects(once()).directory_exists(eq("/some/path")).will(return_value(True))
    context = Context(None, None)
    
    action = CreateDirectoryAction(file_system=mock_file_system)
    assert_raises(DirectoryAlreadyExistsError, action.execute, context, "/some/path",
                   exc_pattern=r'/some/path')

def test_remove_directory_action_should_call_remove_directory():
    mock_file_system = Mock()
    mock_file_system.expects(once()).directory_exists(eq("/some/path")).will(return_value(True))
    mock_file_system.expects(once()).remove_directory(eq("/some/path"))
    context = Context(None, None)
    
    action = RemoveDirectoryAction(file_system=mock_file_system)
    action.execute(context, "/some/path")
    
    assert len(context.log_entries) == 1
    assert context.log_entries[0].message == "Directory removed at /some/path"

def test_remove_directory_action_should_raise_if_directory_does_not_exist():
    mock_file_system = Mock()
    mock_file_system.expects(once()).directory_exists(eq("/some/path")).will(return_value(False))
    context = Context(None, None)
    
    action = RemoveDirectoryAction(file_system=mock_file_system)
    assert_raises(DirectoryNotFoundError, action.execute, context, "/some/path",
                   exc_pattern=r'/some/path')

