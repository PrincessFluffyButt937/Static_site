import unittest

from block import *

class TestBlock(unittest.TestCase):
    def test_is_heading(self):
        block = "###"
        result = is_heading(block)
        self.assertEqual(result, False)

    def test_is_heading1(self):
        block = "### "
        result = is_heading(block)
        self.assertEqual(result, True)

    def test_is_heading2(self):
        block = " "
        result = is_heading(block)
        self.assertEqual(result, False)

    def test_is_heading3(self):
        block = "### Hello"
        result = is_heading(block)
        self.assertEqual(result, True)

    def test_is_heading4(self):
        block = "# "
        result = is_heading(block)
        self.assertEqual(result, True)

    def test_is_heading5(self):
        block = "######  Hello world."
        result = is_heading(block)
        self.assertEqual(result, True)

    def test_is_heading6(self):
        block = "####### Hello world."
        result = is_heading(block)
        self.assertEqual(result, False)

    def test_is_heading7(self):
        block = "#######Hello world."
        result = is_heading(block)
        self.assertEqual(result, False)
    
    # is ordered tests
    def test_is_ordered(self):
        block = "1. Hello world.\n2. I have no idea.\n3. What to type here."
        result = is_ordered(block)
        self.assertEqual(result, True)
    
    def test_is_ordered1(self):
        block = "1. Hello world.\n4. I have no idea.\n3. What to type here."
        result = is_ordered(block)
        self.assertEqual(result, False)
    
    def test_is_ordered2(self):
        block = "Hello world.\n2. I have no idea.\n3. What to type here."
        result = is_ordered(block)
        self.assertEqual(result, False)