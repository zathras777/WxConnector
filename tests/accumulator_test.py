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
from wxconnector.measurement import WxMeasurement
from wxconnector.accumulator import _PlainHiLo, HiLoIncompatibleType

class TestPlain(unittest.TestCase):
    def test_001_lo(self):
        lo = _PlainHiLo()
        ts = 100        
        initial = WxMeasurement(100, WXUNITS['mm'])
        self.assertNotEqual(initial, None)
        lo.check_lo(initial, ts)
        self.assertEqual(lo.value.value, 100)
        self.assertEqual(lo.when, 100)
        checks = [
          [ 99, 'mm', 110, 99, 110 ],
          [ 10, 'cm', 120, 99, 110 ],
          [ 1, 'm', 130, 99, 110 ],
          [ 1.5, 'in', 130, 38.1, 130 ],
        ]
        for c in checks:
            _val = WxMeasurement(c[0], WXUNITS[c[1]])
            lo.check_lo(_val, c[2])
            self.assertEqual(lo.value.value, c[3])
            self.assertEqual(lo.when, c[4])
        incompat = WxMeasurement('20', WXUNITS['mph'])
        self.assertRaises(HiLoIncompatibleType, lo.check_lo, incompat, 100)
        
    def test_002_hi(self):
        hi = _PlainHiLo()
        ts = 100        
        initial = WxMeasurement(1000, WXUNITS['hPa'])
        self.assertNotEqual(initial, None)
        hi.check_hi(initial, ts)
        self.assertEqual(hi.value.value, 1000)
        self.assertEqual(hi.when, 100)
        checks = [
          [ 1000.1, 'hPa', 110, 1000.1, 110 ],
          [ 999.9, 'hPa', 120, 1000.1, 110 ],
          [ 1001.2, 'mbar', 130, 1001.2, 130 ],
          [ 29.592, 'inHg', 140, 1002.1, 140 ],
        ]
        for c in checks:
            _val = WxMeasurement(c[0], WXUNITS[c[1]])
            hi.check_hi(_val, c[2])
            self.assertEqual(hi.value.value, c[3])
            self.assertEqual(hi.when, c[4])

if __name__ == '__main__':
    unittest.main()
