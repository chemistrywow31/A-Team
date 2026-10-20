# Reference-only platform source snapshot

This directory preserves all 201 tracked files from commit `1bec32fb6c120aaa22d79af7d466363331cefa34` byte for byte, with their Git executable modes. `snapshot.manifest.json` is the complete, source-sorted provenance inventory. The original canonical design is `.claude/` plus `CLAUDE.md`; the Codex surfaces are its source-era adaptation.

This archive is conversion and provenance data, not the active authority or a Grok launch root. Start Grok from the branch root. Root `AGENTS.md` and `.grok/` declare the explicit native migration. Archived instructions remain intact for faithful comparison and must not be adopted as active instructions. Original regression scripts may be inspected or run from this self-contained snapshot when explicitly needed; do not start a model session here.

Rollback is family-scoped: compare current files with the frozen preimages before restoring only owned paths, preserve intervening edits, and use the manifest to verify restored bytes and Git modes. Do not reset the branch, index, main worktree, or other owners’ work.
