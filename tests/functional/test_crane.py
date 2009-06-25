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

import os
from os.path import join, dirname, abspath, exists

import crane

def test_crane_builds_hello_world():
    build_script = """
on test do
    show 'hello world'
    """

    runner = crane.Runner()

    result = runner.run(script=build_script, target="test")
    assert result.log.endswith("hello world")

def test_crane_creates_directory():
    build_script = """
on test do
    create directory at %s"""
    path = join(abspath(dirname(__file__)), 'some_folder')
    build_script = build_script % path

    runner = crane.Runner()

    result = runner.run(script=build_script, target="test")
    
    assert exists(path)
    os.rmdir(path)
