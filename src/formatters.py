# -*- coding: utf-8 -*-
"""
===================================
Formatter Utilities Module
===================================

Provides various content formatting utility functions for converting generic
formats into platform-specific formats.
"""

import re
from typing import List

import markdown2

TRUNCATION_SUFFIX = "\n\n...(this section has been truncated due to length)"
PAGE_MARKER_PREFIX = f"\n\n📄"
PAGE_MARKER_SAFE_BYTES = 16 # "\n\n📄 9999/9999"
PAGE_MARKER_SAFE_LEN = 13   # "\n\n📄 9999/9999"
MIN_MAX_WORDS = 10
MIN_MAX_BYTES = 40

# Unicode code point ranges for special characters.
_SPECIAL_CHAR_RANGE = (0x10000, 0xFFFFF)
_SPECIAL_CHAR_REGEX = re.compile(r'[\U00010000-\U000FFFFF]')


def _page_marker(i: int, total: int) -> str:
    return f"{PAGE_MARKER_PREFIX} {i+1}/{total}"


def _is_special_char(c: str) -> bool:
    """Check whether a character is a special character.

    Args:
        c: character to check

    Returns:
        True if the character is a special character, False otherwise
    """
    if len(c) != 1:
        return False
    cp = ord(c)
    return _SPECIAL_CHAR_RANGE[0] <= cp <= _SPECIAL_CHAR_RANGE[1]


def _count_special_chars(s: str) -> int:
    """
    Count the number of special characters in a string.

    Args:
        s: input string
    """
    # reg find all (0x10000, 0xFFFFF)
    match = _SPECIAL_CHAR_REGEX.findall(s)
    return len(match)


def _effective_len(s: str, special_char_len: int = 2) -> int:
    """
    Calculate the effective length of a string.

    Args:
        s: input string
        special_char_len: counted length per special character, default 2

    Returns:
        effective length of s
    """
    n = len(s)
    n += _count_special_chars(s) * (special_char_len - 1)
    return n


def _slice_at_effective_len(s: str, effective_len: int, special_char_len: int = 2) -> tuple[str, str]:
    """
    Split a string at the given effective length.

    Args:
        s: input string
        effective_len: effective length at which to split
        special_char_len: counted length per special character, default 2

    Returns:
        Tuple of (head, tail) strings after the split
    """
    if _effective_len(s, special_char_len) <= effective_len:
        return s, ""
    
    s_ = s[:effective_len]
    n_special_chars = _count_special_chars(s_)
    residual_lens = n_special_chars * (special_char_len - 1) + len(s_) - effective_len
    while residual_lens > 0:
        residual_lens -= special_char_len if _is_special_char(s_[-1]) else 1
        s_ = s_[:-1]
    return s_, s[len(s_):]


def markdown_to_html_document(markdown_text: str) -> str:
    """
    Convert Markdown to a complete HTML document (for email, md2img, etc.).

    Uses markdown2 with table and code block support, wraps with inline CSS
    for compact, readable layout. Reused by notification email and md2img.

    Args:
        markdown_text: Raw Markdown content.

    Returns:
        Full HTML document string with DOCTYPE, head, and body.
    """
    html_content = markdown2.markdown(
        markdown_text,
        extras=["tables", "fenced-code-blocks", "break-on-newline", "cuddled-lists"],
    )

    css_style = """
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                line-height: 1.5;
                color: #24292e;
                font-size: 14px;
                padding: 15px;
                max-width: 900px;
                margin: 0 auto;
            }
            h1 {
                font-size: 20px;
                border-bottom: 1px solid #eaecef;
                padding-bottom: 0.3em;
                margin-top: 1.2em;
                margin-bottom: 0.8em;
                color: #0366d6;
            }
            h2 {
                font-size: 18px;
                border-bottom: 1px solid #eaecef;
                padding-bottom: 0.3em;
                margin-top: 1.0em;
                margin-bottom: 0.6em;
            }
            h3 {
                font-size: 16px;
                margin-top: 0.8em;
                margin-bottom: 0.4em;
            }
            p {
                margin-top: 0;
                margin-bottom: 8px;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 12px 0;
                display: block;
                overflow-x: auto;
                font-size: 13px;
            }
            th, td {
                border: 1px solid #dfe2e5;
                padding: 6px 10px;
                text-align: left;
            }
            th {
                background-color: #f6f8fa;
                font-weight: 600;
            }
            tr:nth-child(2n) {
                background-color: #f8f8f8;
            }
            tr:hover {
                background-color: #f1f8ff;
            }
            blockquote {
                color: #6a737d;
                border-left: 0.25em solid #dfe2e5;
                padding: 0 1em;
                margin: 0 0 10px 0;
            }
            code {
                padding: 0.2em 0.4em;
                margin: 0;
                font-size: 85%;
                background-color: rgba(27,31,35,0.05);
                border-radius: 3px;
                font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            }
            pre {
                padding: 12px;
                overflow: auto;
                line-height: 1.45;
                background-color: #f6f8fa;
                border-radius: 3px;
                margin-bottom: 10px;
            }
            hr {
                height: 0.25em;
                padding: 0;
                margin: 16px 0;
                background-color: #e1e4e8;
                border: 0;
            }
            ul, ol {
                padding-left: 20px;
                margin-bottom: 10px;
            }
            li {
                margin: 2px 0;
            }
        """

    return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                {css_style}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """


def markdown_to_plain_text(markdown_text: str) -> str:
    """
    Convert Markdown to plain text.

    Removes Markdown formatting marks while preserving readability.
    """
    text = markdown_text

    # Remove heading markers # ## ###
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # Remove bold **text** -> text
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)

    # Remove italic *text* -> text
    text = re.sub(r'\*(.+?)\*', r'\1', text)

    # Remove blockquotes > text -> text
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)

    # Remove list markers - item -> item
    text = re.sub(r'^[-*]\s+', '• ', text, flags=re.MULTILINE)

    # Remove horizontal rules ---
    text = re.sub(r'^---+$', '────────', text, flags=re.MULTILINE)

    # Remove table syntax |---|---|
    text = re.sub(r'\|[-:]+\|[-:|\s]+\|', '', text)
    text = re.sub(r'^\|(.+)\|$', r'\1', text, flags=re.MULTILINE)

    # Clean up excess blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def _bytes(s: str) -> int:
    return len(s.encode('utf-8'))


def _chunk_by_max_bytes(content: str, max_bytes: int) -> List[str]:
    if _bytes(content) <= max_bytes:
        return [content]
    if max_bytes < MIN_MAX_BYTES:
        raise ValueError(f"max_bytes={max_bytes} < {MIN_MAX_BYTES}, may cause infinite recursion.")

    sections: List[str] = []
    suffix = TRUNCATION_SUFFIX
    effective_max_bytes = max_bytes - _bytes(suffix)
    if effective_max_bytes <= 0:
        effective_max_bytes = max_bytes
        suffix = ""
        
    while True:
        chunk, content = slice_at_max_bytes(content, effective_max_bytes)
        if content.strip() != "":
            sections.append(chunk + suffix)
        else:
            # Last section — append directly and exit the loop
            sections.append(chunk)
            break
    return sections


def chunk_content_by_max_bytes(content: str, max_bytes: int, add_page_marker: bool = False) -> List[str]:
    """
    Intelligently split message content by byte count.

    Args:
        content: full message content
        max_bytes: maximum bytes per message chunk
        add_page_marker: whether to append a page marker to each chunk

    Returns:
        list of content chunks
    """
    def _chunk(content: str, max_bytes: int) -> List[str]:
        # Prefer splitting on separators/headings for natural page breaks
        if max_bytes < MIN_MAX_BYTES:
            raise ValueError(f"max_bytes={max_bytes} < {MIN_MAX_BYTES}, may cause infinite recursion.")
        
        if _bytes(content) <= max_bytes:
            return [content]
        
        sections, separator = _chunk_by_separators(content)
        if separator == "" and len(sections) == 1:
            # Cannot split intelligently — force-split by byte count
            return _chunk_by_max_bytes(content, max_bytes)

        chunks: List[str] = []
        current_chunk: List[str] = []
        current_bytes = 0
        separator_bytes = _bytes(separator) if separator else 0
        effective_max_bytes = max_bytes - separator_bytes

        for section in sections:
            section += separator
            section_bytes = _bytes(section)

            # If a single section exceeds the limit, force-truncate it
            if section_bytes > effective_max_bytes:
                # Save any accumulated content first
                if current_chunk:
                    chunks.append("".join(current_chunk))
                    current_chunk = []
                    current_bytes = 0

                # Force-split by bytes to avoid losing the entire section
                section_chunks = _chunk(
                    section[:-separator_bytes], effective_max_bytes
                )
                section_chunks[-1] = section_chunks[-1] + separator
                chunks.extend(section_chunks)
                continue

            # Check whether adding this section would exceed the limit
            if current_bytes + section_bytes > effective_max_bytes:
                # Save current chunk and start a new one
                if current_chunk:
                    chunks.append("".join(current_chunk))
                current_chunk = [section]
                current_bytes = section_bytes
            else:
                current_chunk.append(section)
                current_bytes += section_bytes

        # Append the final chunk
        if current_chunk:
            chunks.append("".join(current_chunk))

        # Remove trailing separator from the last chunk
        if (chunks and
            len(chunks[-1]) > separator_bytes and
            chunks[-1][-separator_bytes:] == separator
        ):
            chunks[-1] = chunks[-1][:-separator_bytes]

        return chunks
    
    if add_page_marker:
        max_bytes = max_bytes - PAGE_MARKER_SAFE_BYTES
    
    chunks = _chunk(content, max_bytes)
    if add_page_marker:
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            chunks[i] = chunk + _page_marker(i, total_chunks)
    return chunks


def slice_at_max_bytes(text: str, max_bytes: int) -> tuple[str, str]:
    """
    Truncate a string at a byte boundary, ensuring no multi-byte character is split.

    Args:
        text: string to truncate
        max_bytes: maximum byte count

    Returns:
        (truncated string, remaining untruncated content)
    """
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text, ""

    # Walk backwards from max_bytes to find a complete UTF-8 character boundary
    truncated = encoded[:max_bytes]
    while truncated and (truncated[-1] & 0xC0) == 0x80:
        truncated = truncated[:-1]

    truncated = truncated.decode('utf-8', errors='ignore')
    return truncated, text[len(truncated):]


def format_feishu_markdown(content: str) -> str:
    """
    Convert generic Markdown to a format friendlier to Feishu lark_md.

    Conversion rules:
    - Feishu does not support Markdown headings (# / ## / ###) — replace with bold
    - Blockquotes are replaced with a prefix
    - Horizontal rules are normalized to a thin line
    - Tables are converted to item lists

    Args:
        content: raw Markdown content

    Returns:
        Markdown content converted to Feishu format

    Example:
        >>> markdown = "# Title\\n> Quote\\n| Col1 | Col2 |"
        >>> formatted = format_feishu_markdown(markdown)
        >>> print(formatted)
        **Title**
        💬 Quote
        • Col1: val1 | Col2: val2
    """
    def _flush_table_rows(buffer: List[str], output: List[str]) -> None:
        """Convert buffered table rows to Feishu format."""
        if not buffer:
            return

        def _parse_row(row: str) -> List[str]:
            """Parse a table row and extract cells."""
            cells = [c.strip() for c in row.strip().strip('|').split('|')]
            return [c for c in cells if c]

        rows = []
        for raw in buffer:
            # Skip separator rows (e.g. |---|---|)
            if re.match(r'^\s*\|?\s*[:-]+\s*(\|\s*[:-]+\s*)+\|?\s*$', raw):
                continue
            parsed = _parse_row(raw)
            if parsed:
                rows.append(parsed)

        if not rows:
            return

        header = rows[0]
        data_rows = rows[1:] if len(rows) > 1 else []
        for row in data_rows:
            pairs = []
            for idx, cell in enumerate(row):
                key = header[idx] if idx < len(header) else f"Col{idx + 1}"
                pairs.append(f"{key}：{cell}")
            output.append(f"• {' | '.join(pairs)}")

    lines = []
    table_buffer: List[str] = []

    for raw_line in content.splitlines():
        line = raw_line.rstrip()

        # Handle table rows
        if line.strip().startswith('|'):
            table_buffer.append(line)
            continue

        # Flush the table buffer
        if table_buffer:
            _flush_table_rows(table_buffer, lines)
            table_buffer = []

        # Convert headings (# ## ### etc.)
        if re.match(r'^#{1,6}\s+', line):
            title = re.sub(r'^#{1,6}\s+', '', line).strip()
            line = f"**{title}**" if title else ""
        # Convert blockquotes
        elif line.startswith('> '):
            quote = line[2:].strip()
            line = f"💬 {quote}" if quote else ""
        # Convert horizontal rules
        elif line.strip() == '---':
            line = '────────'
        # Convert list items
        elif line.startswith('- '):
            line = f"• {line[2:].strip()}"

        lines.append(line)

    # Handle any trailing table rows
    if table_buffer:
        _flush_table_rows(table_buffer, lines)

    return "\n".join(lines).strip()


def _chunk_by_separators(content: str) -> tuple[list[str], str]:
    """
    Split message content into sections using separator characters such as divider lines.

    Args:
        content: full message content

    Returns:
        sections: list of content sections after splitting
        separator: separator string used between sections; empty string means unable to split
    """
    # Smart split: prefer "---" separators (dividers between stocks),
    # then fall back to heading levels.
    if "\n---\n" in content:
        sections = content.split("\n---\n")
        separator = "\n---\n"
    elif "\n# " in content:
        # Split on # (level-1 headings)
        parts = content.split("\n## ")
        sections = [parts[0]] + [f"## {p}" for p in parts[1:]]
        separator = "\n"
    elif "\n## " in content:
        # Split on ## (level-2 headings)
        parts = content.split("\n## ")
        sections = [parts[0]] + [f"## {p}" for p in parts[1:]]
        separator = "\n"
    elif "\n### " in content:
        # Split on ### (level-3 headings)
        parts = content.split("\n### ")
        sections = [parts[0]] + [f"### {p}" for p in parts[1:]]
        separator = "\n"
    elif "\n**" in content:
        # Split on ** bold headings (handles AI output that omits standard Markdown headings)
        parts = content.split("\n**")
        sections = [parts[0]] + [f"**{p}" for p in parts[1:]]
        separator = "\n"
    elif "\n" in content:
        # Split on newlines
        sections = content.split("\n")
        separator = "\n"
    else:
        return [content], ""
    return sections, separator


def _chunk_by_max_words(content: str, max_words: int, special_char_len: int = 2) -> list[str]:
    """
    Split message content by word/character count.

    Args:
        content: full message content
        max_words: maximum character count per message chunk
        special_char_len: counted length per special character, default 2

    Returns:
        list of content chunks after splitting
    """
    if _effective_len(content, special_char_len) <= max_words:
        return [content]
    if max_words < MIN_MAX_WORDS:
        raise ValueError(
            f"max_words={max_words} < {MIN_MAX_WORDS}, may cause infinite recursion."
        )

    sections = []
    suffix = TRUNCATION_SUFFIX
    effective_max_words = max_words - len(suffix)  # Reserve space for the suffix to avoid boundary overflow
    if effective_max_words <= 0:
        effective_max_words = max_words
        suffix = ""

    while True:
        chunk, content = _slice_at_effective_len(content, effective_max_words, special_char_len)
        if content.strip() != "":
            sections.append(chunk + suffix)
        else:
            # Last section — append directly and exit the loop
            sections.append(chunk)
            break
    return sections


def chunk_content_by_max_words(
    content: str,
    max_words: int,
    special_char_len: int = 2,
    add_page_marker: bool = False
    ) -> list[str]:
    """
    Intelligently split message content by character count.

    Args:
        content: full message content
        max_words: maximum character count per message chunk
        special_char_len: counted length per special character, default 2
        add_page_marker: whether to append a page marker to each chunk

    Returns:
        list of content chunks after splitting
    """
    def _chunk(content: str, max_words: int, special_char_len: int = 2) -> list[str]:
        if max_words < MIN_MAX_WORDS:
            # Safety guard against infinite recursion.
            # In theory max_words could shrink to zero each recursion, but
            # that is only likely when _chunk_by_separators always succeeds
            # AND the initial max_words value is too small.
            raise ValueError(f"max_words={max_words} < {MIN_MAX_WORDS}, may cause infinite recursion.")
        
        if _effective_len(content, special_char_len) <= max_words:
            return [content]

        sections, separator = _chunk_by_separators(content)
        if separator == "" and len(sections) == 1:
            # Cannot split intelligently — force-split by character count
            return _chunk_by_max_words(content, max_words, special_char_len)

        chunks = []
        current_chunk = []
        current_word_len = 0
        separator_len = len(separator) if separator else 0
        effective_max_words = max_words - separator_len  # Reserve separator length to avoid boundary overflow

        for section in sections:
            section += separator
            section_word_len = _effective_len(section, special_char_len)

            # If a single section exceeds the limit, force-truncate it
            if section_word_len > max_words:
                # Save any accumulated content first
                if current_chunk:
                    chunks.append("".join(current_chunk))

                # Force-split this oversized section
                section_chunks = _chunk(
                    section[:-separator_len], effective_max_words, special_char_len
                    )
                section_chunks[-1] = section_chunks[-1] + separator
                chunks.extend(section_chunks)
                continue

            # Check whether adding this section would exceed the limit
            if current_word_len + section_word_len > max_words:
                # Save current chunk and start a new one
                if current_chunk:
                    chunks.append("".join(current_chunk))
                current_chunk = [section]
                current_word_len = section_word_len
            else:
                current_chunk.append(section)
                current_word_len += section_word_len

        # Append the final chunk
        if current_chunk:
            chunks.append("".join(current_chunk))

        # Remove trailing separator from the last chunk
        if (chunks and
            len(chunks[-1]) > separator_len and
            chunks[-1][-separator_len:] == separator
        ):
            chunks[-1] = chunks[-1][:-separator_len]
        return chunks
    
    
    if add_page_marker:
        max_words = max_words - PAGE_MARKER_SAFE_LEN
    
    chunks = _chunk(content, max_words, special_char_len)
    if add_page_marker:
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            chunks[i] = chunk + _page_marker(i, total_chunks)
    return chunks
