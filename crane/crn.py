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

from crane.context import TargetNotFoundError
from crane.versioning import Version, Release
from crane.runners import Runner

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
    parser.add_option("-d", "--dir", dest="dir", default=None, help="Directory to build from. Defines where to look for build files, actions and anything else [default: current dir].")
    parser.add_option("-v", "--verbosity", dest="verbosity", default=2, help="Verbosity level. 0 for no log, 1 for no dates and 2 for full logging [default: 2].")

    options, args = parser.parse_args()

    if not args:
        show_usage(options, args)
        return

    if options.dir:
        root_dir = abspath(options.dir)
    else:
        root_dir = abspath(os.curdir)

    if options.file:
        build_file_path = join(root_dir, options.file)
    else:
        build_file_path = join(root_dir, 'Cranefile')

    if not exists(build_file_path):
        print "Build file not found at %s" % build_file_path
        sys.exit(1)

    runner = Runner(verbosity=int(options.verbosity))

    script = codecs.open(build_file_path, 'r', 'UTF-8').read()

    try:
        result = runner.run(script, args[0])
    except TargetNotFoundError, err:
        print "The target %s was not found!" % err
        sys.exit(1)

    print_results(result)
    
    if not result or result.status != "SUCCESSFUL":
        sys.exit(1)

    sys.exit(0)

def print_results(result):
    print "Build result: %s" % result.status
    print result.log

if __name__ == "__main__":
    main()
