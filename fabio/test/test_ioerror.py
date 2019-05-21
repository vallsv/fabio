#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: Fable Input Output
#             https://github.com/silx-kit/fabio
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Deep test to check IOError exceptions
"""

from __future__ import print_function, with_statement, division, absolute_import

import unittest
import os
import logging
import shutil

logger = logging.getLogger(__name__)

import fabio
from .utilstest import UtilsTest

TEST_DIRECTORY = None
# Temporary directory where storing test data


def setUpModule():
    global TEST_DIRECTORY
    TEST_DIRECTORY = os.path.join(UtilsTest.tempdir, __name__)
    os.makedirs(TEST_DIRECTORY)


def tearDownModule():
    shutil.rmtree(TEST_DIRECTORY)
    pass


class TestIOError(unittest.TestCase):
    """Test the class format"""

    def create_bad_image(self, filename, pos):
        name, ext = os.path.os.path.splitext(os.path.basename(filename))
        new_filename = "%s__%s%s" % (name, pos, ext)
        new_filename = os.path.join(TEST_DIRECTORY, new_filename)
        with open(filename, "r+b") as fsource:
            with open(new_filename, "wb") as ftest:
                ftest.write(fsource.read())
                ftest.seek(pos)
                ftest.write(b"\xAA")
        return new_filename

    def check_image(self, filename):
        try:
            image = fabio.open(filename)
        except IOError:
            # The image is bad
            return
        except Exception:
            # The lib should not raise that
            raise

        # Image should be well valid
        self.assertIsNotNone(image)
        self.assertIsNotNone(image.data)
        self.assertIsNotNone(image.data.shape)
        self.assertIsNotNone(image.header)

    FILENAMES = [
        "100nmfilmonglass_1_1.img",
        "a0009.edf",
        "a0009.tif",
        "binned_data_uint8.jp2",
        "binned_data_uint16.jp2",
        "corkcont2_H_0089.mccd",
    ]

    def test_all_images(self):
        for filename in self.FILENAMES:
            filename = UtilsTest.getimage(filename + ".bz2")[:-4]
            with self.subTest(filename=filename):
                for pos in range(os.path.getsize(filename)):
                    if pos > 200:
                        break
                    with self.subTest(pos=pos):
                        filename_bad = self.create_bad_image(filename, pos)
                        self.check_image(filename_bad)


def suite():
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loader(TestIOError))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
