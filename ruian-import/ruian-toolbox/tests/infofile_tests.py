# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        infofile_tests
# Purpose:     InfoFile class testing routines.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import unittest
import shared_tools.configuration, os

infofile = shared_tools.configuration.ruian_download_info_file()

class TestInfoFile(unittest.TestCase):
    FILENAME = "test.txt"
    LASTFULLDOWNLOAD_VALUE = "lastfulldownload"
    LASTPATCHDOWNLOAD_VALUE = "lastpatchdownload"


    def tearDown(self):
        if os.path.exists(self.FILENAME):
            os.remove(self.FILENAME)


    def testSave(self):
        """ Tests Save and consequently Init """
        f = shared_tools.configuration.InfoFile(self.FILENAME)
        f.lastFullDownload = self.LASTFULLDOWNLOAD_VALUE
        f.lastPatchDownload = self.LASTPATCHDOWNLOAD_VALUE
        f.save()

        f = shared_tools.configuration.InfoFile(self.FILENAME)
        self.assertEqual(f.lastFullDownload,  self.LASTFULLDOWNLOAD_VALUE,  "lastFullDownload not read correctly")
        self.assertEqual(f.lastPatchDownload, self.LASTPATCHDOWNLOAD_VALUE, "lastPatchDownload not read correctly")

if __name__ == '__main__':
    unittest.main()

