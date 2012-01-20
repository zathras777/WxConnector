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

class _PlainHiLo(object):
    ''' Maintains a record of highest or lowest value with the time it
        was recorded. Measurements can be passed in any unit of a
        compatible type, but the result is always recorded in the unit
        of the initial measurement.
    '''
    def __init__(self):
        self.value = None
        self.when = 0

    def check_lo(self, value, when):
        if not self.value:
            self.value = value
            self.when = when
            return
        _val = self.convert_if_required(value)
        if _val < self.value.value:
            self.value.value = _val
            self.when = when
        return

    def check_hi(self, value, when):
        if not self.value:
            self.value = value
            self.when = when
            return
        _val = self.convert_if_required(value)
        if _val > self.value.value:
            self.value.value = _val
            self.when = when
        return

    def convert_if_required(self, value):
        if value.units != self.value.units:
            if value.units.category != self.value.units.category:
                raise HiLoIncompatibleType('%s are not a measure of %s' % (
                      value.units.description, self.value.units.category))
            return value.convert_to(self.value.units.abbr)
        return value.value

