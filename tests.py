# -*- coding: utf-8 -*-

from juwparser import parse, get_last_time

from test_settings import test_ignore_user3 as settings_ignore_user3
from test_settings import test_ignore_zal as settings_ignore_zal
from test_settings import test_default as settings_default
from test_settings import test_ignore_zal_garaz as settings_ignore_zal_garaz

import unittest
import os
import datetime


class JuwparserTestCase(unittest.TestCase):

    lt_filename = "lasttime_test.txt"
    last_time = "2014-04-24 00:00:00"

    def setUp(self):
        with open(self.lt_filename, 'w') as f:
            f.write(self.last_time)

        with open('testdata/log.html', 'r') as td_f:
            self.testdata1 = td_f.read()

        with open('testdata/log2.html', 'r') as td_f:
            self.testdata2 = td_f.read()

    def tearDown(self):
        os.remove(self.lt_filename)

    def test_get_last_time(self):
        last_time = get_last_time(self.lt_filename)

        self.assertEqual(last_time, datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), 'Last time value is different than expected ' + self.last_time +'.')

    def test_parse_ignore_user3(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_ignore_user3)

        self.assertEqual(parsed, "ZALACZONO (John): garaz, parter czujki, parter okna, pietro okna, parter czujki, garaz, parter okna, pietro okna", "User's 3 actions not ignored or wrong contents of the input file.")

    def test_parse_ignore_zal(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_ignore_zal)

        self.assertEqual(parsed, "WYLACZONO (Alice): garaz, parter czujki, parter okna, pietro okna, parter czujki, garaz, pietro czujki, parter okna, pietro okna, parter czujki, garaz, pietro czujki, parter okna, pietro okna, garaz, parter czujki, parter okna, pietro okna", "'zal' action not ignored or wrong contents of the input file.")

    def test_wlamanie(self):

        parsed = parse(html=self.testdata2, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_default)

        self.assertIn("WLAMANIE: parter czujki", parsed, "No WLAMANIE action reported or wrong contents of the input file.")

    def test_napad(self):

        parsed = parse(html=self.testdata2, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_default)

        self.assertIn("NAPAD!", parsed, "No NAPAD action reported or wrong contents of the input file.")

    def test_user_names(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_default)

        self.assertIn("ZALACZONO (Alice, John)", parsed, "No user 3 and 6 ZALACZONO action present or wrong contents of the input file.")
        self.assertIn("WYLACZONO (Alice)", parsed, "No user 3 ZALACZONO action present or wrong contents of the input file.")

    def test_garaz_in_zal(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_default)

        self.assertIn("garaz", parsed, "Zone 'garaz' should be in the results.")

    def test_ignore_garaz_in_zal(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_ignore_zal_garaz)

        self.assertNotIn("garaz", parsed, "Zone 'garaz' in the results, where it shouldn't be.")
