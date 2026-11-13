# 🚀 Tarn - A Blazing Fast Package Manager for Termux

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.2.0--alpha-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/platform-Termux-blue.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
</p>

**Tarn** is a lightweight, modern package manager built specifically for Termux. Say goodbye to slow official mirrors, outdated packages, and complex dependencies. 

## ✨ Features (v0.2)

- ⚡ **Blazing Fast**: Direct binary delivery from GitHub. No compilation required.
- 📦 **Latest Versions**: Get the newest CLI tools (`btop`, `yazi`, `fastfetch`, etc.) that official repos don't have.
- 🪶 **Zero Dependencies**: Written in pure Python using standard libraries.
- 🧹 **Clean Management**: Easily install, update, and completely remove packages.
- 🛠️ **Script Support**: Custom `post-install.sh` execution for automated environment configuration.

## 📥 Installation

Run this single command in your Termux terminal:

```bash
curl -sL https://raw.githubusercontent.com/termux-tarn/tarn/main/install.sh | bash
```

## 🛠️ Quick Start

Update the package index and install your first tool:

```bash
# 1. Fetch the latest package list
tarn update

# 2. Install the ultimate "hacker" visual effect package (Try it!)
tarn install hack

# 3. Run it
hack
```
*(💡 Tip: Press `Ctrl+C` to stop the hack effect!)*

## 📦 Available Packages

Want to see what's in the store? Check our [Repo Index](https://termux-tarn.github.io/repo/index.json).

## 🗺️ Roadmap

- [x] **v0.1** - Local package installation, extraction, and file tracking.
- [x] **v0.2** - GitHub Pages remote repository support (`tarn update`).
- [ ] **v0.3** - Multi-language (i18n) support & GitHub API integration (install directly via `tarn install gh:user/repo`).
- [ ] **v0.4** - Custom mirror acceleration (China mainland optimized).

## 💰 Donations

Tarn is developed with love and a lot of caffeine. If you find it useful, consider buying me a coffee!

- **USDT (TRC20)**: `TE5MecfcEv1Ww8KMvu6KrBTSCY6j7BvJMz`
- **TRX (TRON)**: `TE5MecfcEv1Ww8KMvu6KrBTSCY6j7BvJMz`

## 💬 Community & Support

- **Discord**: [Join our server](https://discord.gg/n54QeRqxTN)
- **Issues**: [Report a bug](https://github.com/termux-tarn/tarn/issues)

---
*Disclaimer: Tarn is currently in early alpha. Use at your own risk.*
