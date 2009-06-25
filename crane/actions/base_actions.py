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

from crane.actions import ActionBase

class ShowAction(ActionBase):
    regex = "show ['\"](?P<text>.*)['\"]"
    
    def execute(self, build_structure, text):
        build_structure.log(text)

class CreateDirectoryAction(ActionBase):
    regex = "create directory at (?P<directory_path>.*)"
    
    def execute(self, build_structure, directory_path):
        if self.file_system.directory_exists(directory_path):
            raise DirectoryAlreadyExistsError(directory_path)
        self.file_system.create_directory(directory_path)
        build_structure.log("Directory created at %s" % directory_path)

class RemoveDirectoryAction(ActionBase):
    regex = "remove directory at (?P<directory_path>.*)"
    
    def execute(self, build_structure, directory_path):
        if not self.file_system.directory_exists(directory_path):
            raise DirectoryNotFoundError(directory_path)
        self.file_system.remove_directory(directory_path)
        build_structure.log("Directory removed at %s" % directory_path)

class DirectoryAlreadyExistsError(Exception):
    pass

class DirectoryNotFoundError(Exception):
    pass
