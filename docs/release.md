# Mah Jong 0.1.0 release preparation

**Publication of v0.1.0 was explicitly approved.** Calculator behavior is unchanged
by release preparation. Future releases still require explicit approval.

## Four release attachments

| Filename | Platform / content | Current preparation |
| --- | --- | --- |
| `Mah-Jong-Windows-x64.zip` | Windows, Intel/AMD 64-bit | Configured in the existing Windows runner; not built locally |
| `Mah-Jong-macOS-arm64.zip` | macOS 13+, Apple Silicon | Built locally; see `dist/release/` |
| `Mah-Jong-Linux-x64.tar.gz` | Ubuntu 24.04, Intel/AMD 64-bit | Configured in the existing Linux runner; not built locally |
| `Mah-Jong-rules.pdf` | Complete English/German rulebook | Copied unchanged to `dist/release/` |

The local Mac app is at `dist/release-build/Mah Jong.app`. The release ZIP is
created with `ditto` to preserve its bundle permissions and links. Build outputs
remain ignored by Git. The old `dist/MaJong.app` is not this release candidate.

## After explicit approval

1. Review and commit the intended source, documentation, canonical artwork,
   packaging files and `output/pdf/Mah-Jong-rules.pdf`. Do not include local game
   saves, old PDF drafts, original combined artwork or personal documents.
2. Push that reviewed version to the separate `GregorLauter/MaJong` repository.
3. Run **Desktop packages** against that exact revision. The three platform jobs
   test, build and smoke-test the apps. The rulebook job uploads the existing PDF.
   The default run only uploads temporary artifacts. After explicit approval,
   select `publish` to create the release after all platform builds succeed. Only
   the release job has repository-content write permission.
4. Download the four workflow artifacts and extract GitHub's artifact wrappers.
   Attach the inner platform archives and PDF, using the four filenames above.
   Prefer the Mac archive from this same workflow run so all platform candidates
   have the same recorded source revision.
5. Prepare release **Mah Jong 0.1.0**, tag **v0.1.0**, targeting the tested revision.
   Use [release-notes.md](release-notes.md) as the description. The version matches
   the existing Python and Mac bundle metadata. Verify the tag is available.
6. Keep the release as a draft until all four attachments are present and any
   requested review is complete. Publish only with explicit approval. No automatic
   push-triggered publication is enabled.
7. Remove the README's two “being prepared” notices when publication is approved.
   Verify all six language-specific app links resolve to the correct three files.
   The README uses version-specific `v0.1.0` URLs, which also work for a prerelease.

## User-facing limitations

- These are portable app bundles, not click-through installers.
- The Mac app is ad-hoc signed by the bundler, not Developer-ID signed/notarized.
  Download quarantine/Gatekeeper can block it. A local smoke test does not test
  the experience of downloading onto another Mac.
- Windows has no publisher certificate and can show SmartScreen warnings.
  An actual Windows user installation test is still required.
- The Mac bundle is ARM64 only; it does not support Intel Macs.
- The Linux bundle targets Ubuntu 24.04 x64. Other distributions and desktops may
  require system libraries or different executable-launch handling.
- Public release assets will not require a GitHub account; temporary Actions
  artifacts do. Until publication, the prepared app download URLs will not work.
