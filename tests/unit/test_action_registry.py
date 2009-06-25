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

from crane.actions import ActionNotFoundError, ActionFailedError, ActionBase, ActionRegistry
from utils import assert_raises

def test_action_not_found_error():
    error = ActionNotFoundError()
    assert error
    assert isinstance(error, ActionNotFoundError)

def test_action_failed_error():
    error = ActionFailedError()
    assert error
    assert isinstance(error, ActionFailedError)

def test_action_registry_returns_action():
    class ActionToTest(ActionBase):
        regex = r'^Test$'
        
        def execute():
            pass
    action, args, kw = ActionRegistry.suitable_for('Test')
    assert action is ActionToTest
    assert not args
    assert not kw

def test_action_registry_returns_groups_as_args():
    class ActionToTest2(ActionBase):
        regex = r'^Test2-(\d)$'
        
        def execute():
            pass

    action, args, kw = ActionRegistry.suitable_for('Test2-2')
    assert action is ActionToTest2
    assert len(args) == 1
    assert args[0] == '2'
    assert not kw

def test_action_registry_returns_named_groups_as_kw():
    class ActionToTest3(ActionBase):
        regex = r'^Test3-(?P<index>\d)$'
        
        def execute():
            pass

    action, args, kw = ActionRegistry.suitable_for('Test3-2')
    assert action is ActionToTest3
    assert kw.has_key('index')
    assert kw['index'] == '2'
    assert not args

def test_action_registry_returns_kw_only_when_both_named_and_unnamed_groups_are_specified():
    class ActionToTest4(ActionBase):
        regex = r'^Test4-(\d)-(?P<index>\d)$'
        
        def execute():
            pass

    action, args, kw = ActionRegistry.suitable_for('Test4-1-2')
    assert action is ActionToTest4
    assert kw.has_key('index')
    assert kw['index'] == '2'
    assert not args

def test_action_registry_raises_if_action_does_not_feature_regex():
    def should_raise():
        class ActionToTest5(ActionBase):
            def execute():
                pass
    
    assert_raises(NotImplementedError, should_raise, exc_pattern=r'^The action ActionToTest5 does not implement the attribute regex$')
    
def test_action_registry_raises_if_action_does_not_implement_execute():
    def should_raise():
        class ActionToTest6(ActionBase):
            regex = r'^Test6$'
    
    assert_raises(NotImplementedError, should_raise, exc_pattern='^The action ActionToTest6 does not implement the method execute\(\)$')

def test_action_registry_raises_if_action_features_regex_with_different_type_than_string():
    def should_raise():
        class ActionToTest7(ActionBase):
            regex = 10
            
            def execute():
                pass
    
    assert_raises(TypeError, should_raise, exc_pattern="^ActionToTest7.regex attribute must be a string, got 10\('int'\).$")


