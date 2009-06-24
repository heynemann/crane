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

from crane import Tokenizer
from crane.tokenizer import IndentToken, DedentToken, TargetToken, TokenizerError
from utils import assert_raises

def test_tokenize_returns_a_tuple_of_tokens():
    tokens = Tokenizer.tokenize("")
    assert isinstance(tokens, tuple)

def test_tokenize_returns_indent_token():
    tokens = Tokenizer.tokenize("   ")
    assert len(tokens) == 1
    assert isinstance(tokens[0], IndentToken)

def test_tokenize_returns_dedent_token():
    tokens = Tokenizer.tokenize("""    
        
    """)
    
    assert len(tokens) == 3
    assert isinstance(tokens[2], DedentToken)

def test_tokenize_returns_target_token():
    tokens = Tokenizer.tokenize("    on SomeTarget do")
    
    assert len(tokens) == 2
    assert isinstance(tokens[1], TargetToken)

def test_tokenize_returns_target_name_in_token():
    tokens = Tokenizer.tokenize("    on SomeTarget do")
    
    assert tokens[1].name == "SomeTarget"
   
def test_tokenize_raises_if_target_found_after_target():
    script = """on SomeTarget do
on AnotherTarget do"""
    assert_raises(TokenizerError, Tokenizer.tokenize, script, exc_pattern=r'^A target was found when an ActionToken was excepted in line 2. TargetToken found after "SomeTarget" target.$')
