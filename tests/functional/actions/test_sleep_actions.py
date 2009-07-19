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

import time

from crane.actions.base_actions import SleepAction
from crane.context import Context

def test_sleep_action_execute_sleep_method_with_right_amount_of_seconds():
    context = Context(None, None)

    action = SleepAction()
    
    start_time = time.time()
    action.execute(context, 2)
    ellapsed = time.time() - start_time
    assert ellapsed > 1 and ellapsed < 3
    
