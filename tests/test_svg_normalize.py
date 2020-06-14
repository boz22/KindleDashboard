import sys
sys.path.append('../')
import requests
from svg_normalize import normalizeSvg
import unittest
from svg_normalize import convertSvgToPng
import os.path
from os import path
import os
import base64
from images_utils import base64_add_png_mimetype
from images_utils import to_base64


class TestSvgNormalize( unittest.TestCase ):

    def testPngConversion(self):
        svgFile = open("/home/bogdan/work/KindleDashboard/tests/test.svg", "r")
        svgStr = svgFile.read();
        svgFile.close();
        pngContent = convertSvgToPng(svgStr)
        self.assertNotEqual(None, pngContent)
        pngBase64 = to_base64(pngContent)
        pngBase64 = base64_add_png_mimetype( pngBase64 )
        startsWithPngMimeType = pngBase64.startswith("data:image/png;base64,")
        self.assertTrue( startsWithPngMimeType )


if __name__ == '__main__':
    unittest.main()
