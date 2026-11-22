# rnd-007: 3D modeler pilot (Blender 5.1 headless), 2026-11-22
Two procedural assets: T1 low-poly coffee cup + saucer (<3k tris), T2 game-ready treasure chest (<8k tris). Same brief to Antigravity 3d-modeler (gemini-4-hydrogen-high) and Codex (gpt-6-luna, medium). Scripts run by the CEO with blender.exe --background --factory-startup.

| Arm | T1 cup | T2 chest | Runs first try | Tokens |
|---|---|---|---|---|
| Antigravity 3d-modeler | 4.5: correct dark brown glaze, smooth shading, tapered cup, 2,184 tris, 9.5 cm tall | 4.5: domed lid, coin pile, lock, side handle, 7,832 tris, 60 cm wide; lid opened wider than the 30 deg asked | 2/2 | ~1.4k est. (+ ~160-210 s each) |
| Codex gpt-6-luna | 2.5: geometry ok, flat-faceted shading, preview overexposed (dark brown renders salmon), ground plane exported in the .glb | 3.0 after one fix round: first run crashed (materials created before clear_scene purged them); good structure, same overexposed preview | 1/2 | 19,896 + 9,162 + 13,874 fix |
GLB check: Codex materials in the .glb are correct (dark brown, oak); only the preview render was washed out.

Harness findings:
- Antigravity cannot write files in headless print mode (write_file auto-denied). Not bypassed (no --dangerously-skip-permissions without user OK). Workflow: agent replies with the script, CEO runs Blender.
- Codex stderr ('tokens used' + number) got interleaved inside a code block. delegate now uses codex exec -o <file> and prints the clean final answer; tokens still parsed from the stream.

Decision (CEO): 3d-modeler passes the pilot and goes to production on Antigravity (script-in-reply workflow). Codex is the fallback and the script reviewer (bug-finder), not the primary modeller.