"""Regression coverage for list-valued model stream content."""

from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import patch

from octop.infra.agents.harness_stream_compat import install_harness_stream_content_compat


class StringOnlySplitter:
    def feed(self, text: str) -> tuple[str, str]:
        if not isinstance(text, str):
            raise TypeError('can only concatenate str (not "list") to str')
        return text, ""


class ListAwareSplitter(StringOnlySplitter):
    def feed(self, text: str | list[dict[str, str]]) -> tuple[str, str]:
        if isinstance(text, list):
            return "".join(block["text"] for block in text), ""
        return super().feed(text)


class HarnessStreamCompatTests(unittest.TestCase):
    def _install_with(self, splitter_type: type) -> types.ModuleType:
        package = types.ModuleType("harness_agent")
        protocols = types.ModuleType("harness_agent.protocols")
        langgraph = types.ModuleType("harness_agent.protocols.langgraph")
        langgraph.ThinkSplitter = splitter_type
        protocols.langgraph = langgraph
        modules = {
            "harness_agent": package,
            "harness_agent.protocols": protocols,
            "harness_agent.protocols.langgraph": langgraph,
        }
        with patch.dict(sys.modules, modules):
            install_harness_stream_content_compat()
            install_harness_stream_content_compat()
        return langgraph

    def test_list_content_keeps_text_and_reasoning_without_tool_payload(self) -> None:
        langgraph = self._install_with(StringOnlySplitter)
        final, thinking = langgraph.ThinkSplitter().feed(
            [
                {"type": "reasoning", "reasoning": "先想一想"},
                {"type": "text", "text": "答案"},
                {"type": "tool_call_chunk", "text": "private-tool-args"},
                {"type": "output_text", "text": "完成"},
            ]
        )
        self.assertEqual((final, thinking), ("答案完成", "先想一想"))
        self.assertEqual(langgraph.ThinkSplitter().feed("普通文本"), ("普通文本", ""))

    def test_does_not_replace_upstream_list_aware_splitter(self) -> None:
        langgraph = self._install_with(ListAwareSplitter)
        self.assertIs(langgraph.ThinkSplitter, ListAwareSplitter)


if __name__ == "__main__":
    unittest.main()
