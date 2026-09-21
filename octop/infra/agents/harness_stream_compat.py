"""Compatibility for structured LangChain streaming content blocks.

Harness Agent 1.0.12 passes ``AIMessageChunk.content`` directly to its think
splitter, which accepts only strings. OpenAI Responses models can return a list
of typed content blocks, so a successful model response otherwise crashes the
stream before Octop can display it.
"""

from __future__ import annotations

from typing import Any


_TEXT_BLOCK_TYPES = frozenset({"text", "text_delta", "output_text"})
_REASONING_BLOCK_TYPES = frozenset({"reasoning", "reasoning_delta", "reasoning_text"})


def _content_block_parts(content: list[Any]) -> list[tuple[str, str]]:
    """Keep displayable text and reasoning without stringifying other blocks."""
    parts: list[tuple[str, str]] = []
    for block in content:
        if isinstance(block, str):
            parts.append(("text", block))
        elif isinstance(block, dict):
            kind = block.get("type")
            if not isinstance(kind, str):
                continue
            if kind in _TEXT_BLOCK_TYPES and isinstance(block.get("text"), str):
                parts.append(("text", block["text"]))
            elif kind in _REASONING_BLOCK_TYPES:
                value = block.get("reasoning") or block.get("text")
                if isinstance(value, str):
                    parts.append(("reasoning", value))
    return parts


def install_harness_stream_content_compat() -> None:
    """Adapt Harness Agent's splitter only while it lacks list support."""
    from harness_agent.protocols import langgraph

    splitter_type = langgraph.ThinkSplitter
    try:
        splitter_type().feed([{"type": "text", "text": "probe"}])
    except TypeError:
        pass
    else:
        return

    class ContentBlockThinkSplitter(splitter_type):
        def feed(self, content: str | list[Any]) -> tuple[str, str]:
            if not isinstance(content, list):
                return super().feed(content)

            final_parts: list[str] = []
            thinking_parts: list[str] = []
            for kind, value in _content_block_parts(content):
                if kind == "reasoning":
                    thinking_parts.append(value)
                else:
                    final, thinking = super().feed(value)
                    final_parts.append(final)
                    thinking_parts.append(thinking)
            return "".join(final_parts), "".join(thinking_parts)

    langgraph.ThinkSplitter = ContentBlockThinkSplitter
