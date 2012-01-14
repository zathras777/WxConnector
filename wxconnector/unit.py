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

'''
  WxUnit
  In what units is a reading given? How do we convert between units?
'''

from decimal import Decimal

class WxConversionUnavailable(Exception):
    pass
    
class WxUnit(object):
    ''' The base class for a WxUnit. '''
    def __init__(self, abbr, description, category, conversions = {}):
        self.abbr = abbr
        self.category = category
        self.description = description
        self._conversions = conversions

    def conversions_available(self):
        ''' Returns a list of units we can convert to '''
        return self._conversions.keys()

    def convert_value(self, value, into):
        ''' Given a value, convert it into different units. Returns a
            Decimal formatted to correct number of decimal places. '''
        _value = float(Decimal(value))
        try:
            fp = Decimal(10) ** -DECIMAL_PLACES[into]
        except KeyError:
            fp = Decimal('1.')
        try:
            return Decimal(self._conversions[into](_value)).quantize(fp)
        except KeyError:
            return WxConversionUnavailable("Cannot convert from %s to %s" % (self.abbr, into))

    @property
    def decimal_places(self):
        try:
            return DECIMAL_PLACES[self.abbr]
        except KeyError:
            return 0
    
    def format_value(self, value):
        _fmt = "%%.0%sf" % self.decimal_places
        _value = float(Decimal(value))
        return _fmt % _value + self.abbr
        
def make_unit_data():
    categories = {}
    units = {}
    for u in UNIT_DATA:
        units[u[0]] = WxUnit(*u)
        if not categories.has_key(u[2]):
            categories[u[2]] = []
        categories[u[2]].append(u[0])
    return categories, units

def check_units(units, categories):
    errors = []
    for k,v in units.items():
        lbl = '%s:%s' % (v.category, v.abbr)
        if k != v.abbr:
            errors.append("%s has an key that differs from it's abbreviation" % lbl)
        if v.abbr in v.conversions_available():
            errors.append("%s has a conversion for itself!" % lbl)
        # Check we have sane conversions and none are missing
        runits = list(categories[v.category])
        missing = []
        while (runits):
            ck = runits[0]
            del(runits[0])
            if v.abbr != ck and ck not in v.conversions_available():
                missing.append(ck)
        if missing:
            errors.append("%s is missing conversions for %s" %
                                                 (lbl, ', '.join(missing)))
        # Check all conversions work
        for c in v.conversions_available():
            try:
                _ck = v.convert_value(1.0, c)
            except:
               errors.append("%s - conversion to %s fails" % (lbl, c))

    return errors

# If values require decimal places, enter the number of decimal places
# required below. If no decimals are required it should not appear.
DECIMAL_PLACES = {
  'inHg': 2, 'mbar': 1, 'hPa': 1
}

UNIT_DATA = [
  ('inHg', 'inches of Mercury', 'pressure', {'mbar' : lambda x : x * 33.86388640341,
                            'hPa' :  lambda x : x * 33.86388640341}),
  ('mbar', 'millibars', 'pressure', {'inHg' : lambda x : x / 33.86388640341,
                                     'hPa' :  lambda x : x * 1}),
  ('hPa', 'hectopascals', 'pressure', {'inHg' : lambda x : x / 33.86388640341,
                                       'mbar' :  lambda x : x * 1}),
  ('F', 'degrees Fahrenheit', 'temperature',
                                   {'C': lambda x : (x-32.0) * (5.0/9.0)}),
  ('C', 'degrees Celcius', 'temperature',
                                   {'F': lambda x : x * (9.0/5.0) + 32.0}),
  ('in', 'inches', 'distance', 
                   {'cm': lambda x : x * 2.54, 'mm': lambda x : x * 25.4,
                    'ft': lambda x: x / 12}),
  ('ft', 'feet', 'distance', 
                   {'in': lambda x: x * 12, 'cm': lambda x: x * 30.48, 
                    'm': lambda x : x * 0.3048}),
  ('cm', 'centimetre', 'distance', 
             {'in': lambda x : x * 0.393700787, 'mm': lambda x : x * 10.0, 
              'm': lambda x: x / 100, 'ft': lambda x: x * 0.032808399}),
  ('mph', 'miles per hour', 'speed', {'kph': lambda x : x * 1.609344,
         'mps':  lambda x : x * 0.44704, 'kn': lambda x : x * 0.868976242}),
  ('kph', 'kilometres per hour', 'speed', {'mph': lambda x : x / 1.609344,
         'mps':  lambda x : x * 0.44704, 'kn': lambda x : x * 0.868976242}),
  ('mps', 'metres per second', 'speed', {'kph': lambda x : x * 1.609344,
         'mph':  lambda x : x / 0.44704, 'kn': lambda x : x * 0.868976242}),
  ('kn', 'knots', 'speed', {'kph': lambda x : x * 1.609344,
         'mps':  lambda x : x * 0.44704, 'mph': lambda x : x / 0.868976242}),        
]

