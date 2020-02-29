
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

'''
Created on Jan 22, 2020

@author: ballance
'''

class RandInfo(object):
    """Contains information about a set of variables and constraints"""
    
    def __init__(self, randset_l, unconstrained_l, floating_constraint_l = []):
        self.randset_l = randset_l
        self.unconstrained_l = unconstrained_l
        self.floating_constraint_l = floating_constraint_l
        
    def add_randset(self, r):
        self.randset_l.append(r)
        
    def randsets(self):
        return self.randset_l
        
    def add_field(self, f):
        self.unconstrained_l.append(f)
        
    def unconstrained(self):
        return self.unconstrained_l
        