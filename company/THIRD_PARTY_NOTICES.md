# Third-party notices

## obra/superpowers
Source: https://github.com/obra/superpowers (commit 22f0b463e7a5e579904dd6211a520321035526f7, fetched 2026-11-22)
Adapted skills (in ~/.claude/skills): brainstorming, systematic-debugging, test-driven-development, writing-plans,
verification-before-completion, requesting-code-review, receiving-code-review, dispatching-parallel-agents.
Changes: cross-references renamed for a plain install; references to skills that are not installed are marked;
brainstorming's visual-companion server and scripts removed and its trigger narrowed; a source note added to each SKILL.md.

MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Claude Code Game Studios
Used as the System Studio subsidiary inside its own game repository (not redistributed here):
https://github.com/Donchitos/Claude-Code-Game-Studios
## ccusage
https://github.com/ccusage/ccusage (MIT). Installed locally as an npm package (ccusage@20.0.48, --ignore-scripts) in company\vendor\ccusage; not redistributed in this repo. Used read-only with --offline.

## godot-mcp
https://github.com/Coding-Solo/godot-mcp (MIT). Installed locally (@coding-solo/godot-mcp@0.1.1, --ignore-scripts) in company\vendor\godot-mcp; not redistributed. npm audit (2026-11-22): 3 high findings in @modelcontextprotocol/sdk 0.6.0 (HTTP transport/OAuth issues) and zod (memory on oversized input); not reachable here because the server runs over local stdio only.
