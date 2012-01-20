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

class TestMeasurements(unittest.TestCase):
    def test_001_observation(self):
        obs = WxObservation(100)
        self.assertEqual(obs.when, 100)
        self.assertEqual(obs.count, 0)
        obs.add_measurement('temperature', 10.4, 'C')
        self.assertEqual(obs.count, 1)
        obs.add_measurement('temperature', 10.5, 'C')
        self.assertEqual(obs.count, 1)
        ck = obs.get_measurement('temperature')
        self.assertEqual(ck.value, 10.5)
        self.assertEqual(obs.get_measurement('wind_speed'), None)
        self.assertEqual(obs['temperature'].value, 10.5)
        self.assertEqual(obs['temperature'].units, WXUNITS['C'])
        obs.add_measurement('temperature', 38.5, 'F')
        self.assertEqual(obs['temperature'].units, WXUNITS['F'])
        aslist = obs.as_list()
        self.assertEqual(len(aslist), 2)
        self.assertEqual(len(aslist[1]), 1)
        asdict = obs.as_dict()
        self.assertEqual(asdict['when'], 100)
        
        obs.remove_measurement('temperature')
        self.assertEqual(obs.count, 0)
        
    def test_002_oddunits(self):
        wx = WxMeasurement(200, 'kPa')
        self.assertEqual(wx.value, 200)
        self.assertEqual(str(wx), "200 kPa")
        

if __name__ == '__main__':
    unittest.main()
