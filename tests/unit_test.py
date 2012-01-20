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

from wxconnector.unit import *

class TestCreation(unittest.TestCase):
    def test_001_make(self):
        cats, units = make_unit_data()
        self.assertNotEqual(cats, {})
        self.assertNotEqual(units, {})

        ck = check_units(units, cats)
        self.assertEqual(ck, [])
        
        self.assertTrue('pressure' in cats.keys())
        self.assertEqual(len(cats['pressure']), 3)
        self.assertTrue('mbar' in cats['pressure'])
        self.assertFalse('mb' in cats['pressure'])

        self.assertTrue('mbar' in units.keys())
        self.assertFalse('mb' in units.keys())
        self.assertTrue(units['mbar'] is not None)
        self.assertTrue(isinstance(units['mbar'], WxUnit))
        self.assertEqual(units['mbar'].abbr, 'mbar')
        self.assertTrue(units['mbar'].conversions_available())
        self.assertEqual(len(units['mbar'].conversions_available()), 2)
        self.assertTrue('inHg' in units['mbar'].conversions_available())

        check_units(units, cats)
        
    def test_002_convert(self):
        cats, units = make_unit_data()
        mb = units['mbar']
        self.assertTrue(mb)
        self.assertTrue('hPa' in mb.conversions_available())
        mb_checks = (
            (1000, 'hPa', 1000),
            (1000, 'inHg', 29.53)
        )
        for ck in mb_checks:
            self.assertEqual(mb.convert_value(ck[0], ck[1]), ck[2])

    def test_003_conversion(self):
        cats, units = make_unit_data()
        cks = [
            ('C', 'F', 10, 50),
            ('F', 'C', 32, 0),
            ('inHg', 'mbar', '29.92', 1013.2),
            ('hPa', 'inHg', '1033.1', 30.51),
            ('inHg', 'hPa', 29.592, 1002.1),
        ]
        for c in cks:
            cc = units[c[0]]
            _val = cc.convert_value(c[2], c[1])
            self.assertEqual(_val, c[3])
            

    def test_004_formatting(self):
        cats, units = make_unit_data()
        mb = units['mbar']
        self.assertEqual(mb.format_value('1003.1'), '1003.1mbar')
        self.assertEqual(mb.format_value(1003.1), '1003.1mbar')

if __name__ == '__main__':
    unittest.main()
