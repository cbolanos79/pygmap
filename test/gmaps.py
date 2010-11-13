import unittest
import sys
sys.path.append("..")
from gmaps import GMap3

class TestGMap3(unittest.TestCase):
    def setUp(self):
        self.width = 500
        self.height = 500
        self.longitude = 0
        self.latitude = 0

    def testInvalidSize(self):
        try:
            m = GMap3(-1, -1, self.width, self.height)
        except e, GMapInvalidSize:
            pass

    def testInvalidMapType(self):
        try:
            m = GMap3(self.width, self.height, self.longitude, self.latitude)
        except e, GMap3InvalidMapType:
            pass

    def testInvalidDomIdValue(self):
        try:
            m = GMap3(self.width, self.height, self.longitude, self.latitude, "--")
        except e, GMap3InvalidDomIdValue:
            pass

    def testInvalidZoomValue(self):
        try:
            m = GMap3(self.width, self.height, self.longitude, self.latitude, zoom = -1)
        except e, GMap3InvalidZoomValue:
            pass

if __name__ == 'main':
    unittest.main() 
