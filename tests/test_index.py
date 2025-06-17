"""Tests of ``headingmd`` plugin."""

from markdown_it import MarkdownIt
import pytest

from headingmd import headingmd_plugin
from headingmd.index import check_token, remove_heading, convert_paragraph


@pytest.fixture
def md():
    """MarkdownIt instance."""
    return MarkdownIt()


@pytest.fixture
def headings():
    """Markdown headings, from level 1 to 6."""
    return "\n\n".join([f"{'#' * level} H{level}" for level in range(1, 7)])


@pytest.fixture
def hshift1():
    """HTML result of shifting Markdown headings up one level."""
    hs = [f"<h{level}>H{level - 1}</h{level}>" for level in range(2, 7)]
    hs.append("<p>H6</p>")
    return "\n".join(hs) + "\n"


@pytest.fixture
def hshift_1():
    """HTML result of shifting Markdown headings down one level."""
    hs = [f"<h{level}>H{level + 1}</h{level}>" for level in range(1, 6)]
    return "\n".join(hs) + "\n"


@pytest.fixture
def hselect():
    """HTML result of shifting Markdown headings up one level, in range 1--3."""
    hs = [f"<h{level}>H{level - 1}</h{level}>" for level in range(2, 5)]
    hs += [f"<h{level}>H{level}</h{level}>" for level in range(4, 7)]
    return "\n".join(hs) + "\n"


def test_check_token(md):
    """Test token checking."""
    h1tokens = md.parse("# L1 Heading")
    h4tokens = md.parse("#### L4 Heading")
    ptokens = md.parse("Paragraph text.")
    for idx in range(3):
        check = idx != 1
        assert check_token(h1tokens[idx], 1, 6) is check
        assert not check_token(h1tokens[idx], 2, 6)
        assert check_token(h4tokens[idx], 1, 6) is check
        assert not check_token(h4tokens[idx], 1, 3)
        assert not check_token(ptokens[idx], 1, 6)


def test_remove_heading(md, headings):
    """Test heading removal."""
    tokens = md.parse(headings)
    desired = tokens[0:3] + tokens[6:]
    remove_heading(tokens, 3)
    assert tokens == desired


def test_convert_paragraph(md):
    """Test conversion of headings to paragraphs."""
    htokens = md.parse("# L1 Heading\n\n## L2 Heading\n\nParagraph text.")
    ptokens = md.parse("# L1 Heading\n\nL2 Heading\n\nParagraph text.")
    convert_paragraph(htokens, 3)
    convert_paragraph(htokens, 5)
    assert htokens == ptokens


def test_headingmd(headings, hshift1, hshift_1, hselect):
    """Test plugin."""
    md_up = MarkdownIt().use(headingmd_plugin, 1)
    actual_up = md_up.render(headings)
    md_down = MarkdownIt().use(headingmd_plugin, -1)
    actual_down = md_down.render(headings)
    md_select = MarkdownIt().use(headingmd_plugin, 1, hmin=1, hmax=3)
    actual_select = md_select.render(headings)
    assert actual_up == hshift1
    assert actual_down == hshift_1
    assert actual_select == hselect
