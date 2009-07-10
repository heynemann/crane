#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Bernardo Heynemann <heynemann@gmail.com>
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from os.path import exists, dirname, join, abspath
import sys
import optparse
import codecs

from versioning import Version, Release
from runners import Runner

__version_string__ = "crane %s (release '%s')" % (Version, Release)
__docformat__ = 'restructuredtext en'

# fixing print in non-utf8 terminals
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def show_usage(options, args):
    print "duh"

def main():
    """ Main function - parses args and runs action """

    parser = optparse.OptionParser(usage="%prog or type %prog -h (--help) for help", description=__doc__, version=__version_string__)
    parser.add_option("-f", "--file", dest="file", default=None, help="Build file. Defines which file will get executed [default: Cranefile].")

    options, args = parser.parse_args()

    if not args:
        show_usage(options, args)
        return

    root_dir = abspath(os.curdir)

    if options.file:
        build_file_path = join(root_dir, options.file)
    else:
        build_file_path = join(root_dir, 'Cranefile')
    
    if not exists(build_file_path):
        print "Build file not found at %s" % build_file_path
        sys.exit(1)        

    runner = Runner()
    
    script = codecs.open(build_file_path, 'r', 'UTF-8').read()
    result = runner.run(script, args[0]).run_result

    print_results(result)
    
    if not result or result.status != "SUCCESSFUL":
        sys.exit(1)

    sys.exit(0)

def print_results(result):
    print "Build result: %s" % result.status
    print result.log

if __name__ == "__main__":
    main()
