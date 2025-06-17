"""Plugin extension definition."""

from markdown_it import MarkdownIt
from markdown_it.rules_core.state_core import StateCore
from markdown_it.token import Token


def check_token(token: Token, hmin: int, hmax: int) -> bool:
    """Check for heading token in user-specified range."""
    hs = [f"h{level}" for level in range(hmin, hmax + 1)]
    return token.type in ["heading_open", "heading_close"] and token.tag in hs


def process_heading(state: StateCore, idx: int, shift: int) -> int:
    """Process headings based on new level."""
    new_level = int(state.tokens[idx].tag[-1]) + shift
    if new_level < 1:  # Remove headings below h1
        remove_heading(state.tokens, idx)
    elif new_level > 6:  # Convert headings above h6 to paragraphs
        convert_paragraph(state.tokens, idx)
        idx += 1
    else:
        state.tokens[idx].tag = f"h{new_level}"
        idx += 1
    # Return the current position
    return idx


def remove_heading(tokens: list[Token], idx: int) -> None:
    """Remove heading tokens (open, inline, close)."""
    while idx < len(tokens):
        if tokens[idx].type == "heading_close":
            tokens.pop(idx)
            break
        tokens.pop(idx)


def convert_paragraph(tokens: list[Token], idx: int) -> None:
    """Convert heading to paragraph."""
    types = {"heading_open": "paragraph_open", "heading_close": "paragraph_close"}
    tokens[idx].type = types[tokens[idx].type]
    tokens[idx].tag = "p"
    tokens[idx].markup = ""


def validate(shift: int, hmin: int, hmax: int) -> None:
    """Raise error if shift, hmin, and hmax are not integers."""
    for param, name in zip([shift, hmin, hmax], ["shift", "hmin", "hmax"]):
        if not isinstance(param, int):
            raise TypeError(
                f"Parameter {name} must be an integer; argument passed: {param}."
            )


def headingmd_plugin(
    md: MarkdownIt, shift: int = 1, hmin: int = 1, hmax: int = 6
) -> None:
    """Add ``headingmd`` function to the MarkdownIt instance."""
    validate(shift, hmin, hmax)

    def headingmd(state: StateCore):
        """Shift heading levels."""
        idx = 0
        while idx < len(state.tokens):
            if check_token(state.tokens[idx], hmin, hmax):
                idx = process_heading(state, idx, shift)
            else:
                idx += 1

    # Add function to core rules
    md.core.ruler.before("inline", "headingmd", headingmd)
