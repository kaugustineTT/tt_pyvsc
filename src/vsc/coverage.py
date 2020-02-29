
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

import enum
from vsc.model.coverpoint_bin_enum_model import CoverpointBinEnumModel
from vsc.model import expr_mode, get_expr_mode, enter_expr_mode, leave_expr_mode,\
    get_expr_mode_depth
from vsc.impl.covergroup_int import CovergroupInt
from vsc.impl.options import Options
from vsc.impl.type_options import TypeOptions
'''
Created on Aug 3, 2019

@author: ballance
'''
# marks 

from enum import Enum, auto

from vsc.impl.ctor import pop_expr
from vsc.model.covergroup_model import CovergroupModel
from vsc.model.coverpoint_bin_array_model import CoverpointBinArrayModel
from vsc.model.coverpoint_bin_collection_model import CoverpointBinCollectionModel
from vsc.model.coverpoint_bin_model import CoverpointBinModel
from vsc.model.coverpoint_cross_model import CoverpointCrossModel
from vsc.model.coverpoint_model import CoverpointModel
from vsc.model.rangelist_model import RangelistModel
from vsc.types import rangelist, bit_t, to_expr, type_base


            


class _covergroup(object):
        
    def __init__(self, sample_f=None, type_options=None, options=None):
        self.model = None
        self.coverpoint_l = []
        self.cross_l = []

        self.options = Options()
        self.type_options = TypeOptions()
        
        if type_options is not None:
            self.type_options.set(type_options)
            
        if options is not None:
            self.options.set(options)

        # Determine the sampling arguments
#         self.sample_var_l = []
#         if sample_f is not None:
#             c = sample_f.__code__
#             d = sample_f.__defaults__
#         
#             for i in range(len(c.co_varnames)):
#                 t = sample_f.__defaults__[i]
#                 n = c.co_varnames[i]
#            
#                 v = t.clone()
#                 self.sample_var_l.append(v)
#                 setattr(self, n, v)
                
    def get_model(self):
        if self.model is None:
            self.model = CovergroupModel(self)
            
        return self.model
        
    def finalize(self):
        self.get_model()
        
#         self.model = CovergroupModel(self)
#         
# #         for cp_n in dir(self):
# #             cp_o = getattr(self, cp_n)
# #             if isinstance(cp_o, coverpoint):
# #                 self.model.coverpoint_l.append(cp_o.build_model(cp_n))
# #    
# #         # Initialize the cross models second         
# #         for cp_n in dir(self):
# #             cp_o = getattr(self, cp_n)
# #             if isinstance(cp_o, cross):
# #                 self.model.cross_l.append(cp_o.build_model(cp_n))
#                 
#         self.finalized = True
                
    def init_model(self):
        self.get_model()
        
    def _lock(self):
        self.locked = True
        self.options._lock()
        self.type_options._lock()
   
    
    def sample(self, *args):
        '''
        Base sampling method that samples all coverpoints and crosses
        '''

        # Build the model if we haven't yet
        model = self.get_model()
        
        if len(args) != len(self.sample_var_l):
            raise Exception("Wrong number of parameters: expect " + str(len(self.sample_var_l)) + " receive " + str(len(args)))
        
        for i in range(len(args)):
            if isinstance(args[i], type(self.sample_var_l[i])):
                # Just set the field from the arguments
                pass
            else:
                raise Exception("Sample method parameter \"XX\" is of the wrong type")
            self.sample_var_l[i].set_val(args[i])
        
        model.sample()

        pass
    
    def get_coverage(self):
        raise Exception("get_coverage unimplemented")
        pass
    
    def get_inst_coverage(self):
        raise Exception("get_inst_coverage unimplemented")
        pass
    
    def set_inst_name(self, name):
        raise Exception("set_inst_name unimplemented")
        pass
    
    def dump(self, ind=""):
        model = self.get_model()
        model.dump(ind)
        

        
def covergroup(T):
    """Covergroup decorator marks as class as being a covergroup"""
    
    
    print("covergroup: " + str(T))

    if not hasattr(T, "_cg_init"):

        def dump(self, ind=""):
            model = self.get_model()
            model.dump(ind)
            
        # TODO: Make adding sample parameters additive?
        def with_sample(self, params):
            cg_i = self._get_int()
            for pn,pt in params.items():
                print("parameter: " + pn)
                setattr(self, pn, pt)
                cg_i.sample_var_l.append(pn)
            print("self=" + str(self) + " sample_var_l=" + str(len(cg_i.sample_var_l)))
                
        def sample(self, *args, **kwargs):
            """Base sampling method that samples all coverpoints and crosses"""
            # Build the model if we haven't yet
            cg_i = self._get_int()
            
            # TODO: Need to propagate values to base classes
            model = self.get_model()
            
            sample_var_len = len(cg_i.sample_var_l)
            
            if len(args) != sample_var_len:
                raise Exception("Wrong number of parameters: expect " + str(sample_var_len) + " receive " + str(len(args)))
        
            for i in range(len(args)):
                getattr(self, cg_i.sample_var_l[i]).set_val(args[i])

            model.sample()

        pass            
        
        def get_coverage(self):
            return self.get_model().get_coverage()
        
        def get_inst_coverage(self):
            return self.get_model().get_inst_coverage()
        
        def get_model(self):
            cg_i = self._get_int()
            if cg_i.model is None:
                cg_i.model = CovergroupModel(self)
            
            return cg_i.model
        
        def _get_int(self):
            if not hasattr(self, "_cg_int"):
                self._cg_int = CovergroupInt(self)
            return self._cg_int
        
        def _lock(self):
            cg_i = self._get_int()
            cg_i.locked = True
            self.options._lock()
            self.type_options._lock()
        
        def _setattr(self, field, val):
            if hasattr(val, "_build_model"):
                if not hasattr(self, "buildable_l"):
                    object.__setattr__(self, "buildable_l", [])
                self.buildable_l.append(val)
            object.__setattr__(self, field, val)
        
        setattr(T, "dump", dump)
        setattr(T, "with_sample", with_sample)
        setattr(T, "sample", sample)
        setattr(T, "get_coverage", get_coverage)
        setattr(T, "get_inst_coverage", get_inst_coverage)
        setattr(T, "get_model", get_model)
        setattr(T, "_get_int", _get_int)
        setattr(T, "_lock", _lock)
        setattr(T, "__setattr__", _setattr)
        setattr(T, "_cg_init", True)

    # This is the interposer class that wraps a user-defined
    # covergroup class. It ensures that the coverage model is
    # created while field refs are treated as expressions
    class covergroup_interposer(T):
        
        def __init__(self, *args, **kwargs):
            cg_i = self._get_int()
            
            # Ensure options/type_options created before 
            # calling (user) base-class __init__
            if not hasattr(self, "options"):
                self.options = Options()
            if not hasattr(self, "type_options"):
                self.type_options = TypeOptions()
                
            self.buildable_l = []

            with cg_i:                
                super().__init__(*args, **kwargs)

            # Construct the model once we've reached the top level
            if cg_i.ctor_level == 0:
                self.model = self.get_model()
    
    ret = type(T.__name__, (covergroup_interposer,), dict())
    
    return ret

        
class bin(object):
    def __init__(self, *args):
        self.range_l = args
        
    def build_model(self, name, cp):
        # Construct a range model
        range_l = RangelistModel(self.range_l)
        return CoverpointBinModel(name, cp, range_l)
        

class bin_array(object):
    
    def __init__(self, nbins, *args):
        self.nbins = nbins
        self.range_l = args
    
    def _build_model(self, parent, name):
        ret = CoverpointBinCollectionModel(parent, name, self)

        return ret
    
class binsof(object):
    # TODO: future implementation of the 'binsof' operator
    
    def __init__(self, cp):
        pass
    

    def intersect(self, rng):
        pass

    def __and__(self, rhs):
        pass
    
    def __not__(self, rhs):
        pass
    
    def __or__(self, rhs):
        pass
    
class coverpoint(object):
   
    def __init__(self, target, cp_t=None, iff=None, bins=None, options=None, type_options=None):
        self.have_var = False
        self.target = None
        self.model = None
        self.target_kind = None
        self.target_type = None
        self.get_val_f = None
        self.options = Options()
        self.type_options = TypeOptions()
        
        if options is not None:
            self.options.set(options)
            
        if type_options is not None:
            self.type_options.set(type_options)

        with expr_mode():
            print("target=" + str(target))
            if isinstance(target, type_base):
                self.have_var = True
                self.target = target
                self.get_val_f = target.get_val
                self.cp_t = type_base
            elif callable(target):
#             if cp_t is None:
#                 raise Exception("Coverpoint with a callable target must specify type")

                self.cp_t = cp_t
            
                self.target = target
                self.get_val_f = target
            else:
                # should be an actual variable (?)
                print("TODO: handle actual variables")
                to_expr(target)
                self.target = pop_expr()
                print("target=" + str(self.target))
                self.get_val_f = self.target.val
                print("self.get_val_f=" + str(self.get_val_f))
            
        self.iff = iff
        self.bins = bins
        
    def get_coverage(self):
        if self.model is None:
            return 0.0
        else:
            return self.model.get_coverage()
        pass
    
    def get_inst_coverage(self):
        if self.model is None:
            return 0.0
        else:
            return self.model.get_inst_coverage()
    
    def _build_model(self, parent, name):
        if self.model is None:
            self.model = CoverpointModel(parent, self, name)
        print("coverpoint::_build_model: " + str(self) + " " + str(self.model))
        return self.model
    
    def get_model(self):
        return self.model
    
    def get_val(self):
        ret = int(self.get_val_f())
        print("get_val: val=" + str(ret) + " get_val_f=" + str(self.get_val_f))
            
        return ret
    
    def set_val(self, val):
        self.target.set_val(val)
    
    def __le__(self, rhs):
        if self.have_var:
            self.target(rhs)
        else:
            raise Exception("Attempting to set value of non-variable coverpoint")
        
    def _lock(self):
        self.options._lock()
        self.type_options._lock()
    
class cross(object):
    
    def __init__(self, target_l, bins={}):
        for t in target_l:
            if not isinstance(t, coverpoint):
                raise Exception("Cross target \"" + str(t) + "\" is not a coverpoint")
        self.target_l = target_l
        self.bins = bins
        
    def _build_model(self, parent, name):
        ret = CoverpointCrossModel(parent, self, name)
#         coverpoint_model_l = []
#         for t in self.target_l:
#             coverpoint_model_l.append(t.model)
            
#        print("coverpoint_model_l: " + str(coverpoint_model_l))

        return ret
