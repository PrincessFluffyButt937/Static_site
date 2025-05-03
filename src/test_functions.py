import unittest

from functions import *

class TestFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_markdown_to_blocks(self):
        markdown = "  Hello there.  \n\n     General Kenobi! \n\n It is good to see you."
        result = markdown_to_blocks(markdown)
        self.assertListEqual(["Hello there.", "General Kenobi!", "It is good to see you."], result)

    def test_markdown_to_blocks1(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
    Hello        
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Hello\nThis is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks2(self):
        md = """
    
    
    Hello        
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Hello\nThis is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_title_exctractor0(self):
        mk = """
    # Tolkien Fan Club

    ![JRR Tolkien sitting](/images/tolkien.png)

    Here's the deal, **I like Tolkien**.

    """
        result = extract_title(mk)
        self.assertEqual(result, "Tolkien Fan Club")
    
    def test_title_exctractor1(self):
        mk = """
    ## Tolkien Fan Club

    ![JRR Tolkien sitting](/images/tolkien.png)

    Here's the deal, **I like Tolkien**.

    """
        with self.assertRaises(Exception, msg="No title was found."):
            extract_title(mk)
    
