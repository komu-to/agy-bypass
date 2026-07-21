# Antigravity CLI Masked Console (Region-Lock Bypass)

This repository provides a seamless conversational wrapper for the official **Antigravity CLI** (`agy`). It bypasses strict regional blocks and Google Account endpoint limitations that cause the interactive Terminal User Interface (TUI) to crash or throw `Eligibility check failed` errors.

## The Problem
When accessing the Antigravity CLI from a Datacenter IP (e.g. AWS, DigitalOcean, Datacamp) or an unsupported region, the Google CloudCode API endpoint blocks the UI initialization out of safety and regional compliance. 

```text
⚠ Eligibility Check
  ⎿  Eligibility check failed: Your current account is not eligible 
     for Antigravity, because it is not currently available in your location.
```

## The Solution
`agy` has a built-in headless argument (`--print`). The `--print` argument interacts with the standard inference generation API asynchronously and often entirely bypasses the strict `loadCodeAssist` UI account block. 

This wrapper (`agy-cli.py`) handles:
- Faking a full conversational TUI prompt using raw `stdin/stdout`.
- Stitching conversations gracefully using `--continue` and `--new-project`.
- Fixing `UnicodeDecodeError` issues when interacting via SSH with Cyrillic or other UTF-8 text on varying locales.
- Rapidly injecting explicit VPN / SOCKS5 proxies into the Go backend cleanly.

## Installation

Ensure you have `agy` installed and added to your system `$PATH`, as well as Python 3.

```bash
git clone https://github.com/your-username/agy-bypass.git
cd agy-bypass

# Make it executable and link it globally
chmod +x str_cli.py
sudo ln -s $(pwd)/agy-cli.py /usr/local/bin/agy-cli
```

## Usage

Start the REPL anywhere in your terminal:
```bash
agy-cli
```

### Options
```bash
agy-cli --model "Gemini 3.5 Flash (High)" --proxy "socks5h://127.0.0.1:1080"
```
- `-m, --model`: Provide any Antigravity-supported model. Default: `Gemini 3.1 Pro (High)`.
- `-p, --proxy`: Proxy URL that overrides the default. By default, it looks for `HTTP_PROXY` in the environment.
- `--no-proxy`: Forces direct connection, stripping all injected proxies.

## License
MIT License. Feel free to fork and improve!