# Contributing to Vehicle Tracking and Agriculture GIS

Thank you for your interest in contributing to **Vehicle Tracking and Agriculture GIS**! We appreciate your time and effort in making this project better for precision agriculture and UAV mesh networking. Whether it's fixing bugs, adding features, improving documentation, or testing in the field, every contribution counts.

This guide outlines how to get involved. By participating, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Table of Contents
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Submitting Code Changes](#submitting-code-changes)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Questions?](#questions)

## Reporting Bugs
If you encounter a bug (e.g., mesh connectivity issues or GIS rendering errors), please help us replicate it:

1. Check the [issues list](https://github.com/kdahal/agriculture-gis/issues) for similar reports.
2. Create a new issue with:
   - A clear title (e.g., "802.11s Mesh Fails on Raspberry Pi 4 with >50 Nodes").
   - Detailed steps to reproduce.
   - Expected vs. actual behavior.
   - Environment details (hardware, OpenWrt version, OS).
   - Screenshots, logs, or crash dumps if applicable.

Label it as `bug` for quick triage.

## Suggesting Enhancements
Ideas for new features (e.g., ROS2 integration or AI-based anomaly detection in crop data) are welcome!

1. Search existing issues for related discussions.
2. Open a new issue with:
   - A descriptive title.
   - Rationale: Why is this useful? (e.g., "Supports larger swarms for commercial farms").
   - Proposed implementation (high-level).
   - Potential challenges (e.g., RF interference in new bands).

Tag it as `enhancement`.

## Submitting Code Changes
We love pull requests (PRs)! Focus areas include:
- OpenWrt customizations (e.g., new feeds or UCI tweaks).
- GIS enhancements (e.g., Leaflet plugins for NDVI overlays).
- Scripts for simulation/testing (e.g., expanding drone-sim.py).
- Hardware integrations (e.g., ESP32 edge nodes).

### Development Setup
1. **Fork the Repository**: On GitHub, fork to your account.
2. **Clone Locally**:
   ```
   git clone https://github.com/kdahal/agriculture-gis.git
   cd agriculture-gis
   ```
3. **Create a Branch**: For your feature/fix:
   ```
   git checkout -b feature/anything
   ```
4. **Install Dependencies**:
   - For OpenWrt builds: Follow [OpenWrt toolchain setup](https://openwrt.org/docs/guide-developer/toolchain/install-buildsystem).
   - For GIS web: Node.js/npm for Leaflet dev (optional).
   - Python 3+ for scripts/tests.
5. **Build & Test**: Run `./openwrt-custom/build.sh` and local tests before committing.

## Coding Standards
To keep the codebase clean and consistent:

- **Language-Specific**:
  - Bash/Sh: Use shellcheck for linting.
  - Python: PEP 8; run `black` and `flake8` for formatting/linting.
  - JavaScript (GIS): ESLint with airbnb style.
  - UCI/OpenWrt Configs: Follow OpenWrt conventions (e.g., consistent indentation).

- **General**:
  - Commit messages: Imperative mood, <72 chars summary, body for details (e.g., "Fix mesh fwding option in UCI config").
  - One commit per logical change.
  - Include tests for new features.
  - Update docs if your change affects usage.

Run checks locally:
```
# Python lint/format
pip install black flake8
black .
flake8 .

# Shell lint
shellcheck scripts/*.sh
```

## Pull Request Guidelines
1. **Reference Issues**: In your PR description, link to the related issue (e.g., "Closes #42").
2. **Description Template**:
   ```
   ## Description
   Brief overview of changes.

   ## Changes
   - List key commits.

   ## Testing
   - How you verified (e.g., "Tested 90-node sim with latency-test.py").

   ## Checklist
   - [ ] Code lints/formats correctly.
   - [ ] Tests pass.
   - [ ] Docs updated if needed.
   ```
3. **Branch Naming**: `type/scope-description` (e.g., `fix/mesh-latency`).
4. Submit! We'll review promptly—expect feedback within 48 hours.

PRs must pass CI checks (if enabled) and be squash-merged.

## Testing
- **Unit/Integration**: Add tests to `tests/` (e.g., pytest for Python scripts).
- **Field Simulations**: Use `tests/drone-sim.py` for swarm scaling.
- **Hardware**: Test on real UAV setups; share logs if issues arise.
- Coverage: Aim for >80%; use `pytest --cov`.

## Documentation
- Update README.md for user-facing changes.
- Add to `docs/` for internals (e.g., new setup steps).
- Use Markdown consistently; preview with tools like grip.

## Questions?
- Join discussions on GitHub Issues or start a new one.
- For quick chats, mention [@kdahal](https://x.com/kumdahal) on X.
- Need hardware advice? Check `docs/setup-guide.md` or ask in issues.

Happy contributing! Let's make UAV agriculture smarter together. 🌾🚁