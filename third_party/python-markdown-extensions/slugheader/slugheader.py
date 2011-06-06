"""SLUG Header extension for Markdown.

SLUG emails use the following format for headers
==== H1 style header ====
---- H2 style header ----
"""

import markdown

# Global Vars
H1_RE = r'^==*([^=]*)==*'
H2_RE = r'^--*([^-]*)--*'

SH_RE = "(%s|%s)" % (H1_RE, H2_RE)

class SlugHeaderPattern(markdown.inlinepatterns.Pattern):
    """ Return a slug header element:"""
    def handleMatch(self, m):
	if m.group(3):
        	el = markdown.etree.Element("h1")
		text = m.group(3)
	elif m.group(4):
        	el = markdown.etree.Element("h2")
		text = m.group(4)
	else:
		raise SyntaxError('Unknown SLUG Header match.')
	el.text = markdown.AtomicString(text)
        return el

class SlugHeaderExtension(markdown.Extension):
    """ SlugHeader Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Replace subscript with SlugHeaderPattern """
        md.inlinePatterns['slugheader'] = SlugHeaderPattern(SH_RE, md)

def makeExtension(configs=None):
    return SlugHeaderExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
