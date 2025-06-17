# Heading, MD

Heading, MD is a plugin extension for the [Markdown-It-Py][mditpy] Markdown parser. Heading, MD operates on headings: it can increase/decrease heading levels, convert headings to paragraphs, and/or excise headings completely from the rendered HTML.

## Installation

Clone this repository. Change into the repository directory, type the following command, and press enter:

```bash
pip install .
```

## Setup

Import the Markdown-It-Py parser and the Heading, MD plugin:

```python
from markdown_it import MarkdownIt
from headingmd import headingmd_plugin
```

## Basic usage

By default, Heading, MD shifts headings up one level (`<h1>` HTML tags become `<h2>` tags). Follow the plugin conventions outlined in the [Markdown-It-Py documentation][mditpy-doc-plugins] to load the plugin with default settings:

```python
md = MarkdownIt().use(headingmd_plugin)
```

Use the parser to render Markdown text as HTML.

```python
text = "# Level-one Markdown heading"
html = md.render(text)
```

The parser renders the level-one Markdown heading into HTML with `h2` HTML tags:

```html
<h2>Level-one Markdown heading</h2>
```

## Advanced usage

### Increase heading levels

Pass an argument to the `shift` parameter to specify how much to shift the heading levels. For example, to shift headings up two levels (`<h1>` HTML tags become `<h3>` tags):

```python
md = MarkdownIt().use(headingmd_plugin, shift=2)
text = "# Level-one Markdown heading"
html = md.render(text)
```

The text is rendered as:

```html
<h3>Level-one Markdown heading</h3>
```

Note that headings shifted above level six are converted to paragraphs. For example:

```python
md = MarkdownIt().use(headingmd_plugin, shift=6)
text = "# Level-one Markdown heading"
html = md.render(text)
```

This renders as:

```html
<p>Level-one Markdown heading</p>
```

### Decrease heading levels

Pass a negative integer to the `shift` parameter to shift heading levels down. Note that headings shifted below level one are removed from the rendered HTML. For example:

```python
md = MarkdownIt().use(headingmd_plugin, shift=-1)
text = "# Level-one Markdown heading\n\n## Level-two Markdown heading"
html = md.render(text)
```

This removes the original level-one Markdown heading and renders as:

```html
<h1>Level-two Markdown heading</h1>
```

### Specify a range of headings

The `hmin` and `hmax` parameters specify the minimum and maximum heading levels for Heading, MD operations. For example:

```python
md = MarkdownIt().use(headingmd_plugin, shift=3, hmin=2, hmax=3)
text = "# Level 1\n\n## Level 2\n\n### Level 3\n\n#### Level 4"
html = md.render(text)
```

In the above case, Heading, MD only operates on the level-two and level-three headings. The HTML renders as:

```html
<h1>Level 1</h1>
<h5>Level 2</h5>
<h6>Level 3</h6>
<h4>Level 4</h4>
```

### Use multiple Heading, MD plugins

Load the Heading, MD plugin repeatedly with different settings to operate on different headings in different ways. For example, the following removes all level-two headings and converts all level-three and level-four headings to paragraphs:

```python
md = MarkdownIt()
md = md.use(headingmd_plugin, shift=-2, hmin=2, hmax=2)
md = md.use(headingmd_plugin, shift=4, hmin=3, hmax=4)
text = "# Level 1\n\n## Level 2\n\n### Level 3\n\n#### Level 4"
html = md.render(text)
```

This renders as:

```html
<h1>Level 1</h1>
<p>Level 3</p>
<p>Level 4</p>
```

[mditpy]: https://markdown-it-py.readthedocs.io/en/latest/
    "Markdown-It-Py"

[mditpy-doc-plugins]: https://markdown-it-py.readthedocs.io/en/latest/plugins.html
    "Markdown-It-Py: Plugin Extensions"

