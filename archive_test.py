#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
import datetime
import calendar
import subprocess
import shutil


class TestArchive(unittest.TestCase):

    ROOT = os.getcwd()
    BACK95 = calendar.timegm((datetime.datetime.utcnow() - (datetime.timedelta(days=95))).timetuple())
    BACK46 = calendar.timegm((datetime.datetime.utcnow() - (datetime.timedelta(days=46))).timetuple())

    @classmethod
    def setUpClass(cls):
        # do a bit of pre-emptive cleanup
        try:
            shutil.rmtree(os.path.join(cls.ROOT, "testout"), ignore_errors=True)
        except:
            None
        try:
            shutil.rmtree(os.path.join(cls.ROOT, "1Folder Space"), ignore_errors=True)
        except:
            None
        try:
            os.remove(os.path.join(cls.ROOT, "archive.log"))
        except:
            None

        # create tree of data to be processed
        os.mkdir(os.path.join(cls.ROOT, "testout"))
        os.mkdir(os.path.join(cls.ROOT, "1Folder Space"))
        os.mkdir(os.path.join(cls.ROOT, "1Folder Space", "2Folder"))
        os.mkdir(os.path.join(cls.ROOT, "1Folder Space", "3Folder With Space"))
        os.mkdir(os.path.join(cls.ROOT, "1Folder Space", "3Folder With Space", "4Folder"))
        os.mkdir(os.path.join(cls.ROOT, "1Folder Space", "3Folder With Space", "5Folder"))

        thepath = os.path.join(cls.ROOT, "1Folder Space")
        open(os.path.join(thepath, "1A.txt"), 'a').close()
        os.utime(os.path.join(thepath, "1A.txt"), (cls.BACK95, cls.BACK95))
        open(os.path.join(thepath, "1B.txt"), 'a').close()
        os.utime(os.path.join(thepath, "1B.txt"), (cls.BACK95, cls.BACK95))

        open(os.path.join(thepath, "Iris–Waveguide Interface - MechanicAspects.pptx"), 'a').close()
        os.utime(os.path.join(thepath, "Iris–Waveguide Interface - MechanicAspects.pptx"), (cls.BACK95, cls.BACK95))

        thepath = os.path.join(cls.ROOT, "1Folder Space", "2Folder")
        open(os.path.join(thepath, "2A.txt"), 'a').close()
        os.utime(os.path.join(thepath, "2A.txt"), (cls.BACK46, cls.BACK46))
        open(os.path.join(thepath, "2B.txt"), 'a').close()
        os.utime(os.path.join(thepath, "2B.txt"), (cls.BACK95, cls.BACK95))

        thepath = os.path.join(cls.ROOT, "1Folder Space", "3Folder With Space", "4Folder")
        open(os.path.join(thepath, "4A.txt"), 'a').close()
        os.utime(os.path.join(thepath, "4A.txt"), (cls.BACK46, cls.BACK46))
        open(os.path.join(thepath, "4B.txt"), 'a').close()
        os.utime(os.path.join(thepath, "4B.txt"), (cls.BACK95, cls.BACK95))

        thepath = os.path.join(cls.ROOT, "1Folder Space", "3Folder With Space", "5Folder")
        open(os.path.join(thepath, "5A.txt"), 'a').close()
        os.utime(os.path.join(thepath, "5A.txt"), (cls.BACK95, cls.BACK95))
        open(os.path.join(thepath, "5B.txt"), 'a').close()
        os.utime(os.path.join(thepath, "5B.txt"), (cls.BACK95, cls.BACK95))
        for i in range(100):
            open(os.path.join(thepath, ("%dC.txt" % i)), 'a').close()
            os.utime(os.path.join(thepath, ("%dC.txt" % i)), (cls.BACK95, cls.BACK95))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(os.path.join(cls.ROOT, "testout"), ignore_errors=True)
        shutil.rmtree(os.path.join(cls.ROOT, "1Folder Space"), ignore_errors=True)
        None


    def testFirstPass(self):
        # run a pass of archive
        subprocess.check_call(['/usr/bin/python', 'archive.py', '-a90', '-s./1Folder Space', '-d./testout/1Folder Space'])

        # check what we have in the source
        thepath = os.path.join(self.ROOT, "1Folder Space")
        self.assertTrue(os.path.exists(thepath))
        self.assertFalse(os.path.exists(os.path.join(thepath, "1A.txt")))
        self.assertFalse(os.path.exists(os.path.join(thepath, "1B.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "2Folder")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "3Folder With Space")))
        self.assertFalse(os.path.exists(os.path.join(thepath, "Iris–Waveguide Interface - MechanicAspects.pptx")))

        thepath = os.path.join(self.ROOT, "1Folder Space", "2Folder")
        self.assertTrue(os.path.exists(os.path.join(thepath, "2A.txt")))
        self.assertFalse(os.path.exists(os.path.join(thepath, "2B.txt")))

        thepath = os.path.join(self.ROOT, "1Folder Space", "3Folder With Space")
        self.assertTrue(os.path.exists(os.path.join(thepath, "4Folder")))
        self.assertFalse(os.path.exists(os.path.join(thepath, "5Folder")))

        thepath = os.path.join(self.ROOT, "1Folder Space", "3Folder With Space", "4Folder")
        self.assertTrue(os.path.exists(os.path.join(thepath, "4A.txt")))
        self.assertFalse(os.path.exists(os.path.join(thepath, "4B.txt")))

        for i in range(100):
            self.assertFalse(os.path.exists(os.path.join(thepath, ("%dC.txt" % i))))

        # check what we have in the destination
        thepath = os.path.join(self.ROOT, "testout", "1Folder Space")
        self.assertTrue(os.path.exists(thepath))
        self.assertTrue(os.path.exists(os.path.join(thepath, "1A.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "1B.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "2Folder")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "3Folder With Space")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "Iris–Waveguide Interface - MechanicAspects.pptx")))

        thepath = os.path.join(self.ROOT, "testout", "1Folder Space", "2Folder")
        self.assertFalse(os.path.exists(os.path.join(thepath, "2A.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "2B.txt")))

        thepath = os.path.join(self.ROOT, "testout", "1Folder Space", "3Folder With Space")
        self.assertTrue(os.path.exists(os.path.join(thepath, "4Folder")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "5Folder")))

        thepath = os.path.join(self.ROOT, "testout", "1Folder Space", "3Folder With Space", "4Folder")
        self.assertFalse(os.path.exists(os.path.join(thepath, "4A.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "4B.txt")))

        thepath = os.path.join(self.ROOT, "testout", "1Folder Space", "3Folder With Space", "5Folder")
        self.assertTrue(os.path.exists(os.path.join(thepath, "5A.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "5B.txt")))

        for i in range(100):
            self.assertTrue(os.path.exists(os.path.join(thepath, ("%dC.txt" % i))))

    def testSecondPass(self):
        # run a pass of archive
        subprocess.check_call(['/usr/bin/python', 'archive.py', '-a30', '-s./1Folder Space', '-d./testout/1Folder Space'])

        # check what we have in the source
        thepath = os.path.join(self.ROOT, "1Folder Space")
        self.assertFalse(os.path.exists(thepath))

        # check what we have in the destination
        thepath = os.path.join(self.ROOT, "testout", "1Folder Space")
        self.assertTrue(os.path.exists(thepath))
        self.assertTrue(os.path.exists(os.path.join(thepath, "1A.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "1B.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "2Folder")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "3Folder With Space")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "Iris–Waveguide Interface - MechanicAspects.pptx")))

        thepath = os.path.join(self.ROOT, "testout", "1Folder Space", "2Folder")
        self.assertTrue(os.path.exists(os.path.join(thepath, "2A.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "2B.txt")))

        thepath = os.path.join(self.ROOT, "testout", "1Folder Space", "3Folder With Space")
        self.assertTrue(os.path.exists(os.path.join(thepath, "4Folder")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "5Folder")))

        thepath = os.path.join(self.ROOT, "testout", "1Folder Space", "3Folder With Space", "4Folder")
        self.assertTrue(os.path.exists(os.path.join(thepath, "4A.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "4B.txt")))

        thepath = os.path.join(self.ROOT, "testout", "1Folder Space", "3Folder With Space", "5Folder")
        self.assertTrue(os.path.exists(os.path.join(thepath, "5A.txt")))
        self.assertTrue(os.path.exists(os.path.join(thepath, "5B.txt")))


if __name__ == '__main__':
    unittest.main()
