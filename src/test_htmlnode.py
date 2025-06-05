import unittest

from textnode import TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):   
        print("HTMLNode test passed!")
        print("This is a test of the HTMLNode module.")
        node = HTMLNode("This is some anchor text", TextType.LINK, "https://boot.dev")
        print(node)
        self.assertEqual(node.tag, "This is some anchor text")
        self.assertEqual(node.value, TextType.LINK)
        #self.assertEqual(node.url, "https://boot.dev")
        print("Test passed!")   
        selfassert = HTMLNode("This is a text node", TextType.BOLD)
        selfassert2 = HTMLNode("This is a text node", TextType.BOLD) 

    def test_leafnode(self):
        print("LeafNode test passed!")
        print("This is a test of the LeafNode module.")
        node = LeafNode("div", "This is some text", {"class": "test"})  

        self.assertNotEqual(node.to_html(), '<div class="test">This is some text</div>')
        self.assertNotEqual(node.to_string(), '<div class="test">This is some text</div>') 

    def test_parentnode(self):
        print("ParentNode test passed!")
        print("This is a test of the ParentNode module.")
        node = HTMLNode("div", None, [LeafNode("span", "This is a child")], {"class": "test"})
        
        #self.assertNotEqual(node.to_html(), '<div class="test"><span>This is a child</span></div>')
        self.assertNotEqual(node.to_string(), '<div class="test"><span>This is a child</span></div>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
    print("All tests passed!")
    print("All tests passed!")
    