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

''' The accumulator classes are designed to allow a number of observations
    to be "accumulated" and the various statistics we want recorded.
    Each accumulator is simply fed a number of observations and records
    the data required together with timestamp data to allow the duration
    of observations to be determined. No attempt is made to limit the
    timespan of an accumulator - this is left to the caller to control.
'''

import math

from wxconnector.measurement import *

class HiLoIncompatibleType(Exception):
    pass

def _convert_if_required(val1, value):
    if value.units != val1.units:
        if value.units.category != val1.units.category:
            raise HiLoIncompatibleType('%s are not a measure of %s' % (
                             value.units.description, val1.units.category))
        return value.convert_to(val1.units.abbr)
    return value.value

class _PlainHiLo(object):
    ''' Maintains a record of highest or lowest value with the time it
        was recorded. Measurements can be passed in any unit of a
        compatible type, but the result is always recorded in the unit
        of the initial measurement.
    '''
    def __init__(self):
        self.lo_value = None
        self.lo_when = 0
        self.hi_value = None
        self.hi_when = 0

    def check(self, value, when):
        self.check_lo(value, when)
        self.check_hi(value, when)
        
    def check_lo(self, value, when):
        if not self.lo_value:
            self.lo_value = WxMeasurement(value.value, value.units)
            self.lo_when = when
            return
        _val = _convert_if_required(self.lo_value, value)
        if _val < self.lo_value.value:
            self.lo_value.value = _val
            self.lo_when = when

    def check_hi(self, value, when):
        if not self.hi_value:
            self.hi_value = WxMeasurement(value.value, value.units)
            self.hi_when = when
            return
        _val = _convert_if_required(self.hi_value, value)
        if _val > self.hi_value.value:
            self.hi_value.value = _val
            self.hi_when = when

class _PlainAvg(object):
    ''' Maintains records to allow calculation of the average value.
        Measurements can be passed in any unit of a compatible type, 
        but the result is always recorded in the unit of the initial
        measurement.
    '''
    # todo This is overly niave and should take account of the time for
    #      values.
    def __init__(self):
        self.sum_value = None
        self.count = 0

    def add(self, value):
        if not self.sum_value:
            self.sum_value = WxMeasurement(value.value, value.units)
            self.count = 1
        else:
            _val = _convert_if_required(self.sum_value, value)
            self.sum_value.value += _val
            self.count += 1

    def avg(self):
        _val = float(self.sum_value.value) / self.count
        return WxMeasurement(_val, self.sum_value.units)

class _RmsAvg(object):
    ''' Average a set of measurements using a Root Mean Square. '''
    def __init__(self):
        self.sum_value = None
        self.count = 0

    def add(self, value):
        if not self.sum_value:
            sq = value.value ** 2
            self.sum_value = WxMeasurement(sq, value.units)
            self.count = 1
        else:
            _val = _convert_if_required(self.sum_value, value) ** 2
            self.sum_value.value += _val
            self.count += 1

    def avg(self):
        _val = self.sum_value.units.convert_value(
                              math.sqrt(self.sum_value.val() / self.count))
        return WxMeasurement(_val, self.sum_value.units)
    
class _Wind(object):
    ''' Maintains wind records, including hi/low for strength and an
        averaged direction/speed. '''
    def __init__(self):
        self.hilo = _PlainHiLo()
        self.speed_rms = _RmsAvg()
        
class BasicAccumulator(object):
    ''' Throw observations at it and it will accumulate statistics '''
    # Which readings do we record hi/low figures for?
    HILO = ['barometer','temperature','wind_speed','humidity','uv',
                                                         'solar_radiation']
    # Which readings do we record an average for?
    AVG = HILO

    def __init__(self):
        self.hilos = {}
        self.avgs = {}
        self.first = 0
        self.last = 0
        self.nobs = 0
        
    def add_observation(self, obs):
        if self.first == 0:
            self.first = obs.when
        # what should we do about observations that are from before last
        # timestamp?
        for k,v in obs.measurements.items():
            if k in self.HILO:
                if not self.hilos.has_key(k):
                    self.hilos[k] = _PlainHiLo()
                self.hilos[k].check(v, obs.when)
            if k in self.AVG:
                if not self.avgs.has_key(k):
                    self.avgs[k] = _PlainAvg()
                self.avgs[k].add(v)
                
        if obs.when > self.last:
            self.last = obs.when
        self.nobs += 1

    @property
    def timespan(self):
        ''' Returns the timespan in seconds '''
        return self.last - self.first
        
    def get_lowest(self, what):
        hilo = self.hilos.get(what, None)
        if hilo:
            return (hilo.lo_value, hilo.lo_when)
        return (None, 0)

    def get_highest(self, what):
        hilo = self.hilos.get(what, None)
        if hilo:
            return (hilo.hi_value, hilo.hi_when)
        return (None, 0)
        
    def debug_print(self):
        print "BasicAccumulator: %d obsersvations" % self.nobs
        print "From %d to %d" % (self.first, self.last)
        print "Averages"
        for k in self.avgs.keys():
            print "%30s %10s" % (k, self.avgs[k].avg())

        print "Highs/Lows"
        for k in self.hilos.keys():
            print "%30s %10s @ %d %10s @ %d" % (k, self.hilos[k].lo_value, 
                                  self.hilos[k].lo_when, self.hilos[k].hi_value, self.hilos[k].hi_when)

