# -*- coding: utf-8 -*-
#  Copyright 2012 David Reid
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import time

from wxconnector import WXUNITS
from wxconnector.unit import WxUnit, WxConversionUnavailable

class WxMeasurement(object):
    ''' A measurement of an aspect of the weather. '''
    def __init__(self, value, units):
        ''' Create a measurement. It is expected that a WxUnit instance
            and the value will be passed in. '''
        self.units = WXUNITS.get(units, units)
        self.value = value

    def __repr__(self):
        if isinstance(self.units, WxUnit):
            return self.units.format_value(self.value)
        return "%s %s" % (self.value, self.units)

    def val(self):
        return self.convert_to()
        
    def as_list(self, what = ''):
        ll = [self.value]
        ll.append(self.units.abbr if isinstance(self.units, WxUnit) else self.units)
        if what: ll.insert(0, what)
        return ll

    def convert_to(self, unit = ''):
        if isinstance(self.units, WxUnit):   
            return self.units.convert_value(self.value, unit)
        return self.value

class WxObservation(object):
    ''' An observation is a series of measurements taken at the same time. '''
    def __init__(self, timestamp = None):
        self.when = timestamp or time.time()
        self.measurements = {}

    def __getitem__(self, what):
        return self.measurements.get(what, None)
        
    @property
    def count(self):
        return len(self.measurements)

    def add_measurement(self, what, value, units):
        self.measurements[what] = WxMeasurement(value, units)

    def remove_measurement(self, what):
        if self.measurements.has_key(what):
            self.measurements.pop(what)
            
    def get_measurement(self, what):
        return self.measurements.get(what, None)

    def as_list(self):
        lm = []
        ll = [ self.when, lm ]
        for k,v in self.measurements.items():
            lm.append(v.as_list(k))
        return ll

    def as_dict(self):
        dd = {'when': self.when, 'measurements': []}
        for k,v in self.measurements.items():
            dd['measurements'].append(v.as_list(k))
        return dd
        
    def debug_print(self):
        print "Observation @ %s" % self.when
        for k,v in self.measurements.items():
            print '    ',"%30s" % k,': ', v

