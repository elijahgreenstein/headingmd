"""Plugin extension for Markdown-It-Py to shift heading levels.

Example usage (shift headings up one level).

>>> from markdown_it import MarkdownIt
>>> from headingmd import headingmd_plugin
>>> md = MarkdownIt().use(headingmd_plugin, 1)
>>> md.render("# Level-one heading")
<h2>Level-one heading</h2>
>>> md.render("###### Level-six heading")
<p>Level-six heading</p>

Note that the level-six heading was converted to a paragraph; headings above
level six (``<h6>`` tags) are converted to paragraphs. Headings below level one
(``<h1>`` tags) are removed entirely.
"""

from .index import headingmd_plugin

__all__ = ("headingmd_plugin",)
