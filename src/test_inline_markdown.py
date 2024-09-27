import unittest

from inline_markdown import *

class TestSplitDelimiter(unittest.TestCase):
    def test_text_basic(self):
        node = [TextNode("This is text", text_type_text)]
        expected = [TextNode("This is text", text_type_text)]
        self.assertListEqual(node, expected)

    def test_text_bold(self):
        node = TextNode("This is **bold** text", text_type_text)
        result = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
              TextNode("This is ", text_type_text),
              TextNode("bold", text_type_bold),
              TextNode(" text", text_type_text),
        ]
        self.assertListEqual(result, expected)

    def test_text_italic(self):
        node = TextNode("This is *italic* text", text_type_text)
        result = split_nodes_delimiter([node], "*", text_type_italic)
        expected = [
              TextNode("This is ", text_type_text),
              TextNode("italic", text_type_italic),
              TextNode(" text", text_type_text),
        ]
        self.assertListEqual(result, expected)

    def test_text_code(self):
        node = TextNode("This is `code` text", text_type_text)
        result = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
              TextNode("This is ", text_type_text),
              TextNode("code", text_type_code),
              TextNode(" text", text_type_text),
        ]
        self.assertListEqual(result, expected)

    #def test_text_link(self):
        #node = "This is [link] text", text_type_text
        #result = split_nodes_delimiter([node], "()", text_type_link)
        #expected = [
                #TextNode("This is ", text_type_text),
                #TextNode("link", text_type_link),
                #TextNode(" text", text_type_text),
        #]
        #self.assertListEqual(node, expected)

    #def test_text_image(self):
         #node = "This is ![image](https://www.boot.dev) text", text_type_text
         #result = split_nodes_delimiter([node], "![]()", text_type_image)
         #expected = [
                # TextNode("This is , text_type_text"),
                # TextNode("image", text_type_image),
                # TextNode(" text", text_type_text),
                #]
         #self.assertListEqual(node, expected)

    def test_unmatched_delimiter(self):
        node = TextNode("This is unmatched **bold text", text_type_text)
        delimiter = "**"
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", text_type_bold)

        expected_message = f"Invalid Markdown Syntax: Missing closing delimiter for '{delimiter}'"
        self.assertEqual(str(context.exception), expected_message)

    def test_text_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
               TextNode("bold", text_type_bold),
               TextNode(" and ", text_type_text),
               TextNode("italic", text_type_italic),
            ],
            new_nodes,
         )
    
    def test_text_bold_double(self):
        node = TextNode(
             "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
             [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
             ],
             new_nodes,
        )

    def test_text_bold_multiword(self):
        node = TextNode(
             "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

class TestExtractors(unittest.TestCase):
    def test_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        extract = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extract, expected)

    def test_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        extract = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract, expected)

    def test_multi_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extract = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract, expected)


    def test_multi_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extract = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract, expected)

    def test_no_image_url(self):
        text = "This is text with a ![rick roll]"
        extract = extract_markdown_images(text)
        expected = []
        self.assertEqual(extract, expected)

    def test_no_image_alt_text(self):
        text = "This is text with a (https://i.imgur.com/aKaOqIh.gif)"
        extract = extract_markdown_images(text)
        expected = []
        self.assertEqual(extract, expected)

    def test_no_link_url(self):
        text = "This is text with a link [to boot dev]"
        extract = extract_markdown_links(text)
        expected = []
        self.assertEqual(extract, expected)

    def test_no_link_anchor_text(self):
        text = "This is text with a link (https://www.boot.dev)"
        extract = extract_markdown_links(text)
        expected = []
        self.assertEqual(extract, expected)

    def test_bad_markdown_image(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)"
        extract = extract_markdown_images(text)
        expected = []
        self.assertEqual(extract, expected)

    def test_bad_markdown_link(self):
        text = "This is text with a link [to boot dev(https://www.boot.dev)"
        extract = extract_markdown_links(text)
        expected = []
        self.assertEqual(extract, expected)

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_nodes_image(self):
        #No images
        node = TextNode("This is text without images", text_type_text)
        result = split_nodes_image([node])
        assert len(result) == 1
        assert result[0].text == "This is text without images"
        assert result[0].text_type == text_type_text

        #One image at start
        node = TextNode("![alt](url) This is text", text_type_text)
        result = split_nodes_image([node])
        assert len(result) == 2
        assert result[0].text == "alt"
        assert result[0].text_type == text_type_image
        assert result[0].url == "url"
        assert result[1].text == " This is text"
        assert result[1].text_type == text_type_text

        #One image at end
        node = TextNode("This is text ![alt](url)", text_type_text)
        result = split_nodes_image([node])
        assert len(result) == 2
        assert result[0].text == "This is text "
        assert result[0].text_type == text_type_text
        assert result[1].text == "alt"
        assert result[1].text_type == text_type_image
        assert result[1].url == "url"

        #Multiple images
        node = TextNode("![alt](url) text ![alt2](url2)", text_type_text)
        result = split_nodes_image([node])
        assert len(result) == 3
        assert result[0].text == "alt"
        assert result[0].text_type == text_type_image
        assert result[0].url == "url"
        assert result[1].text == " text "
        assert result[1].text_type == text_type_text
        assert result[2].text == "alt2"
        assert result[2].text_type == text_type_image
        assert result[2].url == "url2"

        #Text before, between, and after images
        node = TextNode("Start ![alt](url) middle ![alt2](url2) end", text_type_text)
        result = split_nodes_image([node])
        assert len(result) == 5
        assert result[0].text == "Start "
        assert result[0].text_type == text_type_text
        assert result[1].text == "alt"
        assert result[1].text_type == text_type_image
        assert result[1].url == "url"
        assert result[2].text == " middle "
        assert result[2].text_type == text_type_text
        assert result[3].text == "alt2"
        assert result[3].text_type == text_type_image
        assert result[3].url == "url2"
        assert result[4].text == " end"
        assert result[4].text_type == text_type_text

        #Empty alt text
        node = TextNode("![](url) text", text_type_text)
        result = split_nodes_image([node])
        assert len(result) == 2
        assert result[0].text == ""
        assert result[0].text_type == text_type_image
        assert result[0].url == "url"
        assert result[1].text == " text"
        assert result[1].text_type == text_type_text

        #Special characters in url
        node = TextNode("![alt](!`*) text", text_type_text)
        result = split_nodes_image([node])
        assert len(result) == 2
        assert result[0].text == "alt"
        assert result[0].text_type == text_type_image
        assert result[0].url == "!`*"
        assert result[1].text == " text"
        assert result[1].text_type == text_type_text

        #Multiple images no text
        node = TextNode("![alt](url)![alt2](url2)", text_type_text)
        result = split_nodes_image([node])
        assert len(result) == 2
        assert result[0].text == "alt"
        assert result[0].text_type == text_type_image
        assert result[0].url == "url"
        assert result[1].text == "alt2"
        assert result[1].text_type == text_type_image
        assert result[1].url == "url2"


    def test_split_nodes_link(self):
        #No link
        node = TextNode("This is text without links", text_type_text)
        result = split_nodes_link([node])
        assert len(result) == 1
        assert result[0].text == "This is text without links"
        assert result[0].text_type == text_type_text

        #One link at start
        node = TextNode("[anchor](url) This is text", text_type_text)
        result = split_nodes_link([node])
        assert len(result) == 2
        assert result[0].text == "anchor"
        assert result[0].text_type == text_type_link
        assert result[0].url == "url"
        assert result[1].text == " This is text"
        assert result[1].text_type == text_type_text

        #One link at end
        node = TextNode("This is text [anchor](url)", text_type_text)
        result = split_nodes_link([node])
        assert len(result) == 2
        assert result[0].text == "This is text "
        assert result[0].text_type == text_type_text
        assert result[1].text == "anchor"
        assert result[1].text_type == text_type_link
        assert result[1].url == "url"

        #Multiple links
        node = TextNode("[anchor](url) text [anchor2](url2)", text_type_text)
        result = split_nodes_link([node])
        assert len(result) == 3
        assert result[0].text == "anchor"
        assert result[0].text_type == text_type_link
        assert result[0].url == "url"
        assert result[1].text == " text "
        assert result[1].text_type == text_type_text
        assert result[2].text == "anchor2"
        assert result[2].text_type == text_type_link
        assert result[2].url == "url2"

        #Text before, between, and after link
        node = TextNode("Start [anchor](url) middle [anchor2](url2) end", text_type_text)
        result = split_nodes_link([node])
        assert len(result) == 5
        assert result[0].text == "Start "
        assert result[0].text_type == text_type_text
        assert result[1].text == "anchor"
        assert result[1].text_type == text_type_link
        assert result[1].url == "url"
        assert result[2].text == " middle "
        assert result[2].text_type == text_type_text
        assert result[3].text == "anchor2"
        assert result[3].text_type == text_type_link
        assert result[3].url == "url2"
        assert result[4].text == " end"
        assert result[4].text_type == text_type_text

        #Empty anchor text
        node = TextNode("[](url) text", text_type_text)
        result = split_nodes_link([node])
        assert len(result) == 2
        assert result[0].text == ""
        assert result[0].text_type == text_type_link
        assert result[0].url == "url"
        assert result[1].text == " text"
        assert result[1].text_type == text_type_text

        #Special characters in anchor text
        node = TextNode("[!`*](url) text", text_type_text)
        result = split_nodes_link([node])
        assert len(result) == 2
        assert result[0].text == "!`*"
        assert result[0].text_type == text_type_link
        assert result[0].url == "url"
        assert result[1].text == " text"
        assert result[1].text_type == text_type_text

        #Special characters in url
        node = TextNode("[anchor](!`*) text", text_type_text)
        result = split_nodes_link([node])
        assert len(result) == 2
        assert result[0].text == "anchor"
        assert result[0].text_type == text_type_link
        assert result[0].url == "!`*"
        assert result[1].text == " text"
        assert result[1].text_type == text_type_text

        #Multiple links no text
        node = TextNode("[anchor](url)[anchor2](url2)", text_type_text)
        result = split_nodes_link([node])
        assert len(result) == 2
        assert result[0].text == "anchor"
        assert result[0].text_type == text_type_link
        assert result[0].url == "url"
        assert result[1].text == "anchor2"
        assert result[1].text_type == text_type_link
        assert result[1].url == "url2"


if __name__ == "__main__":
	unittest.main(exit=False)
