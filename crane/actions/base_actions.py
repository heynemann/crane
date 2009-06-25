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

from crane.actions import ActionBase

class ActualFileSystem():
    def create_directory(self, path):
        os.mkdir(path)

class ShowAction(ActionBase):
    regex = "show ['\"](?P<text>.*)['\"]"
    
    def execute(self, build_structure, text):
        build_structure.log(text)

class CreateDirectoryAction(ActionBase):
    regex = "create directory ['\"](?P<directory_path>.*)['\"]"
    
    def __init__(self, file_system=None):
        self.file_system = file_system and file_system or ActualFileSystem()

    def execute(self, build_structure, directory_path):
        self.file_system.create_directory(directory_path)
        build_structure.log("Directory created at %s" % directory_path)
