# Mah Jong 0.1.0 release preparation

**Publication of v0.1.0 was explicitly approved.** Calculator behavior is unchanged
by release preparation. Future releases still require explicit approval.

## Published v0.1.0

[Download Mah Jong 0.1.0](https://github.com/GregorLauter/MaJong/releases/tag/v0.1.0).
All three platform packages and the PDF were published from commit `d777c5e`.
[Release build run](https://github.com/GregorLauter/MaJong/actions/runs/35539753731)
and [test run](https://github.com/GregorLauter/MaJong/actions/runs/35539726667)
completed successfully.

| Release attachment | Platform / content | Verification |
| --- | --- | --- |
| `Mah-Jong-Windows-x64.zip` | Windows, Intel/AMD 64-bit | Built, tested and startup-checked on Windows |
| `Mah-Jong-macOS-arm64.zip` | macOS 13+, Apple Silicon | Built, tested and startup-checked on macOS |
| `Mah-Jong-Linux-x64.tar.gz` | Ubuntu 24.04, Intel/AMD 64-bit | Built, tested and startup-checked on Linux |
| `Mah-Jong-rules.pdf` | Complete English/German rulebook | Published from the canonical export |

The published downloads are the GitHub-built files from the same revision.
`dist/release/` holds the earlier locally verified Mac ZIP and PDF, not local
copies of all published assets. Build outputs remain ignored by Git.

## Procedure for future approved releases

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
5. Choose a new version and tag targeting the tested revision; `v0.1.0` is already
   published and must not be overwritten. Update version metadata and workflow
   release commands consistently.
   Update [release-notes.md](release-notes.md) for the new release.
6. Keep the release as a draft until all four attachments are present and any
   requested review is complete. Publish only with explicit approval. No automatic
   push-triggered publication is enabled.
7. Update and verify all six language-specific README app links. Use the newly
   approved version tag in the URLs.

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
- Public release assets do not require a GitHub account; temporary Actions
  artifacts do.
