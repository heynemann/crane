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

from crane.context import Context, LogEntry

def test_can_create_context():
    context = Context()
    assert context
    assert isinstance(context, Context)

def test_context_starts_with_null_result():
    context = Context()
    assert not context.run_result

def test_context_starts_with_null_structure():
    context = Context()
    assert not context.build_structure

def test_context_keeps_track_of_run_result():
    context = Context(run_result="something")
    assert context.run_result == "something"

def test_context_keeps_track_of_parsed_build_structure():
    context = Context(build_structure="else")
    assert context.build_structure == "else"

