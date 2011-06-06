"""Extension for Markdown which turns any URLs into href links."""

import markdown

ANYURL_RE = "(http://[^ ]*)"

class AnyURLPattern(markdown.inlinepatterns.Pattern):
    """ Return a url header element:"""
    def handleMatch(self, m):
	if not m.group(2):
		raise SyntaxError('Error in AnyURL')

	el = markdown.etree.Element("a")
	el.text = markdown.AtomicString(m.group(2))
	el.set('href', m.group(2))
        return el

class AnyURLExtension(markdown.Extension):
    """ AnyURL Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Replace subscript with AnyURLPattern """
        md.inlinePatterns['anyurl'] = AnyURLPattern(ANYURL_RE, md)

def makeExtension(configs=None):
    return AnyURLExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
