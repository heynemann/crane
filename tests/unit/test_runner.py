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
from crane import Runner, RunResult, ParsedBuildStructure, Successful, Context

def test_can_create_runner():
    runner = Runner()
    assert isinstance(runner, Runner)

def test_can_create_runner_with_given_parser():
    runner = Runner(parser="mock parser")
    assert runner.parser == "mock parser"

def test_run_script_returns_result():
    executer_mock = Mock()
    
    parsed_build_structure = ParsedBuildStructure()
    executer_mock.expects(once()).method('execute_target').with_at_least(build_structure=eq(parsed_build_structure), target=eq(None))

    parser_mock = Mock()
    parsed_build_structure.targets["some target"] = None
    parser_mock.expects(once()).parse_script(eq("some script")).will(return_value(parsed_build_structure))

    runner = Runner(parser=parser_mock, executer=executer_mock)
    result = runner.run("some script", "some target")
    assert result is not None
    parser_mock.verify()

def test_run_script_returns_RunResult():
    executer_mock = Mock()
    parsed_build_structure = ParsedBuildStructure()

    executer_mock.expects(once()).method('execute_target').with_at_least(build_structure=eq(parsed_build_structure), target=eq(None))

    parser_mock = Mock()
    parsed_build_structure.targets["some target"] = None
    parser_mock.expects(once()).parse_script(eq("some script")).will(return_value(parsed_build_structure))

    runner = Runner(parser=parser_mock, executer=executer_mock)
    result = runner.run("some script", "some target")
    assert isinstance(result, RunResult)
    parser_mock.verify()

def test_run_script_returns_proper_result():
    some_result = RunResult()
    some_result.log = "some log"
    some_result.status = Successful

    mock_target = Mock()
    executer_mock = Mock()
    parser_mock = Mock()
    parsed_build_structure = ParsedBuildStructure()
    parsed_build_structure.log_entries = ["some log"]
    parsed_build_structure.targets["some target"] = mock_target
    parser_mock.expects(once()).parse_script(eq("some script")).will(return_value(parsed_build_structure))

    executer_mock.expects(once()).method('execute_target').with_at_least(build_structure=eq(parsed_build_structure), target=eq(mock_target))

    runner = Runner(parser=parser_mock, executer=executer_mock)
    result = runner.run("some script", "some target")

    assert result.status == Successful
    parser_mock.verify()
    mock_target.verify()
    executer_mock.verify()

