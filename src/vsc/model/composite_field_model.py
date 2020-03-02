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
Created on Jul 24, 2019

@author: ballance
'''

class CompositeFieldModel(object):
    
    def __init__(self, name, is_rand=False, rand_if=None):
        self.name = name
        self.is_rand = is_rand
        self.rand_if = rand_if
        self.parent = None
        self.field_l = []
        self.constraint_model_l = []

    def finalize(self):
        pass
                    
    def build(self, builder):
        # First, build the fields
        for f in self.field_l:
            f.build(builder)

        # Next, build out the constraints
        for c in self.constraint_model_l:
            c.build(builder)

#        for f in self.field_l:
#            if isinstance(f, CompositeFieldModel):
#                f.build

    def add_field(self, f):
        f.parent = self
        self.field_l.append(f)
        
    def add_constraint(self, c):
        c.parent = self
        self.constraint_model_l.append(c)
        
    def get_constraints(self, constraint_l):
        for f in self.field_l:
            f.get_constraints(constraint_l)
            
        for c in self.constraint_model_l:
            constraint_l.append(c)
            
    def get_fields(self, field_l):
        for f in self.field_l:
            if isinstance(f, CompositeFieldModel):
                f.get_fields(field_l)
            else:
                field_l.append(f)

    def pre_randomize(self):
        """Called during the randomization process to propagate pre_randomize event"""
        
        # Perform a phase callback if available
        if self.rand_if is not None:
            self.rand_if.pre_randomize()
            
        for f in self.field_l:
            f.pre_randomize()
    
    def post_randomize(self):
        """Called during the randomization process to propagate post_randomize event"""
        
        # Perform a phase callback if available
        if self.rand_if is not None:
            self.rand_if.post_randomize()
            
        for f in self.field_l:
            f.post_randomize()

    def accept(self, visitor):
        visitor.visit_composite_field(self)
            