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

import sys
import unittest
from decimal import Decimal

from wxconnector import WXUNITS
from wxconnector.measurement import WxMeasurement, WxObservation
from wxconnector.accumulator import _PlainHiLo, HiLoIncompatibleType, BasicAccumulator

class TestPlain(unittest.TestCase):
    def test_001_lo(self):
        lo = _PlainHiLo()
        ts = 100        
        initial = WxMeasurement(100, WXUNITS['mm'])
        self.assertNotEqual(initial, None)
        lo.check_lo(initial, ts)
        self.assertEqual(lo.lo_value.value, 100)
        self.assertEqual(lo.lo_when, 100)
        checks = [
          [ 99, 'mm', 110, 99, 110 ],
          [ 10, 'cm', 120, 99, 110 ],
          [ 1, 'm', 130, 99, 110 ],
          [ 1.5, 'in', 130, 38.1, 130 ],
        ]
        for c in checks:
            _val = WxMeasurement(c[0], WXUNITS[c[1]])
            lo.check_lo(_val, c[2])
            self.assertEqual(lo.lo_value.value, c[3])
            self.assertEqual(lo.lo_when, c[4])
        incompat = WxMeasurement('20', WXUNITS['mph'])
        self.assertRaises(HiLoIncompatibleType, lo.check_lo, incompat, 100)
        
    def test_002_hi(self):
        hi = _PlainHiLo()
        ts = 100        
        initial = WxMeasurement(1000, WXUNITS['hPa'])
        self.assertNotEqual(initial, None)
        hi.check_hi(initial, ts)
        self.assertEqual(hi.hi_value.value, 1000)
        self.assertEqual(hi.hi_when, 100)
        checks = [
          [ 1000.1, 'hPa', 110, 1000.1, 110 ],
          [ 999.9, 'hPa', 120, 1000.1, 110 ],
          [ 1001.2, 'mbar', 130, 1001.2, 130 ],
          [ 29.592, 'inHg', 140, 1002.1, 140 ],
        ]
        for c in checks:
            _val = WxMeasurement(c[0], WXUNITS[c[1]])
            hi.check_hi(_val, c[2])
            self.assertEqual(hi.hi_value.value, c[3])
            self.assertEqual(hi.hi_when, c[4])

    def test_003_basic(self):
        ba = BasicAccumulator()
        self.assertNotEqual(ba, None)
        obs = WxObservation(121)
        initial_m = [
            ['temperature', 10.5, 'C'],
            ['barometer', 1000.2, 'hPa'],
        ]
        for m in initial_m:
            obs.add_measurement(m[0], m[1], m[2])
        ba.add_observation(obs)
        self.assertEqual(ba.nobs, 1)
        
        (val, when) = ba.get_highest('temperature')
        self.assertEqual(when, 121)
        self.assertEqual(val.value, 10.5)
        
        check_m = [
            ['temperature', 9.5, 'C'],
            ['barometer', 1000.3, 'hPa'],
        ]
        obs2 = WxObservation(125)
        for m in check_m:
            obs2.add_measurement(m[0], m[1], m[2])
        ba.add_observation(obs2)
        self.assertEqual(ba.nobs, 2)

        (val, when) = ba.get_lowest('temperature')
        self.assertEqual(when, 125)
        self.assertEqual(val.value, 9.5)

        (val, when) = ba.get_highest('barometer')
        self.assertEqual(when, 125)
        self.assertEqual(val.value, 1000.3)

        (val, when) = ba.get_highest('wind_speed')
        self.assertEqual(val, None)

if __name__ == '__main__':
    unittest.main()
