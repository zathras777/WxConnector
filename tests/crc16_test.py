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

from wxconnector.utils.crc16 import crc_ccitt_16

class TestCRC(unittest.TestCase):
    def test_001_generation(self):
        checks = [
            [ '123456789', 0x31C3 ],
            [ 'hello world', 0x3BE4 ],
            [ 'Hello world', 0x919E ],
            [ 'a', 0x7C87 ],
            [ ' ', 0x2462 ],
            [ 32, 0x2462 ],
            [ 0x20, 0x2462 ],
            
        ]
        for ck in checks:
            self.assertEqual(crc_ccitt_16(ck[0]), ck[1])

    def test_002_checksum(self):
        checks = [
            [ 0x20, 0x24, 0x62 ],
            [ 0x61, 0x7c, 0x87 ],
            [ 49, 50, 51, 52, 53, 54, 55, 56, 57, 0x31, 0xc3 ],
            [ 16, 52, 9, 16, 1, 112, 98, 222 ]
        ]
        for ck in checks:
            self.assertEqual(crc_ccitt_16(ck), 0)

    def test_003_multipass(self):
        checks = [
            [ [ '123', '456', '789' ], 0x31c3 ],
            [ [ '123', '456', '789', 0x31, 0xc3 ], 0 ],
            [ [ 49, 50, 51, 52, 53, 54, 55, 56, 57 ], 0x31c3 ],
            [ [ 49, 50, 51, 52, 53, 54, 55, 56, 57, 0x31, 0xc3 ], 0 ],
        ]
        for ck in checks:
            _crc = 0
            for part in ck[0]:
                _crc = crc_ccitt_16(part, _crc)
            self.assertEqual(_crc, ck[1])
            
if __name__ == '__main__':
    unittest.main()
