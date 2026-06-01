import unittest

from docreader.parser import Parser
from docreader.parser.registry import registry


class HTMLParserTest(unittest.TestCase):
    def test_builtin_registry_supports_html_extensions(self):
        self.assertEqual(
            registry.get_parser_class("builtin", "html").__name__,
            "HTMLParser",
        )
        self.assertEqual(
            registry.get_parser_class("builtin", "htm").__name__,
            "HTMLParser",
        )

    def test_parse_html_file_to_markdown(self):
        html = b"""
<!doctype html>
<html>
  <head><title>HTML Sample</title></head>
  <body>
    <article>
      <h1>HTML Sample</h1>
      <p>Hello <a href="https://example.com">Example</a>.</p>
      <table><tr><th>Name</th><th>Value</th></tr><tr><td>A</td><td>1</td></tr></table>
    </article>
  </body>
</html>
"""

        document = Parser().parse_file("sample.html", "html", html)

        self.assertIn("HTML Sample", document.content)
        self.assertIn("Hello", document.content)
        self.assertIn("Example", document.content)
        self.assertEqual(document.metadata.get("title"), "HTML Sample")


if __name__ == "__main__":
    unittest.main()
