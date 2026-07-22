#!/usr/bin/env python3
"""
Antigravity Masked Console (Region-Lock Bypass Wrapper)

This script provides an interactive REPL frontend for the Antigravity CLI ('agy').
It allows users to bypass strict region-based UI locks by utilizing the CLI's
non-interactive '--print' mode under the hood, while maintaining the illusion
of a seamless conversational interface.

Key Features:
- Replaces the TUI (Bubbletea) which immediately crashes on Google API Eligibility checks.
- Maintains conversation continuity using '--continue'.
- Safely handles flawed terminal character encoding (UTF-8 binary reading).
- Injects HTTP/SOCKS5 proxies uniformly to both Python and the nested 'agy' process.

Author: Open Source Community
License: MIT
"""

import subprocess
import os
import shutil
import sys
import argparse

# Console color codes for UI aesthetics
COLOR_RESET = "\033[0m"
COLOR_CYAN = "\033[1;36m"
COLOR_YELLOW = "\033[1;33m"
COLOR_RED = "\033[1;31m"

def print_ui_header(model: str, proxy: str):
    """Prints the application banner."""
    print("=" * 60)
    print(f" {COLOR_CYAN}Antigravity Masked Console (Region-Lock Bypass){COLOR_RESET}")
    print(f" Model: {model}")
    print(f" Proxy: {proxy if proxy else 'None (Direct Connection)'}")
    print(" Type 'exit' or 'quit' to close the session.")
    print("=" * 60 + "\n")

def get_parser() -> argparse.ArgumentParser:
    """Configures command-line arguments."""
    parser = argparse.ArgumentParser(description="Antigravity Masked Console")
    parser.add_argument(
        "-m", "--model", 
        type=str, 
        default="Gemini 3.1 Pro (High)",
        help="Specify the target model to run (e.g. 'Gemini 3.1 Pro (High)')."
    )
    parser.add_argument(
        "-p", "--proxy", 
        type=str, 
        default=os.environ.get("HTTP_PROXY", "socks5h://10.9.9.2:1080"),
        help="Proxy URL (socks5h://... or http://...). Defaults to internal VPN proxy."
    )
    parser.add_argument(
        "-a", "--auto-approve", 
        action="store_true", 
        help="Auto-approve all tool permission requests (--dangerously-skip-permissions)."
    )
    parser.add_argument(
        "--no-proxy", 
        action="store_true", 
        help="Disable proxy injection completely."
    )
    return parser

def main():
    # Force pure UTF-8 stream handling to prevent UnicodeDecodeError 
    # when processing chaotic cyrillic input from some imperfect SSH terminals.
    sys.stdin.reconfigure(encoding='utf-8', errors='backslashreplace')
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

    parser = get_parser()
    args = parser.parse_args()

    # Determine proxy settings
    active_proxy = None if args.no_proxy else args.proxy
    
    # Clone the environment and apply proxies so 'agy' backend fetches through them
    env = os.environ.copy()
    if active_proxy:
        env["HTTP_PROXY"] = active_proxy
        env["HTTPS_PROXY"] = active_proxy
        env["ALL_PROXY"] = active_proxy

    print_ui_header(args.model, active_proxy)

    # Tracks whether we need to initiate a fresh context
    is_first_turn = True
    
    while True:
        try:
            # 1. Prompt User
            sys.stdout.write(f"{COLOR_CYAN}[You]{COLOR_RESET}\n> ")
            sys.stdout.flush()
            
            # Use raw buffer readline. Avoids input() which eagerly drops exceptions on bad bytes.
            raw_input = sys.stdin.buffer.readline()
            if not raw_input:
                break # EOF detected (Ctrl+D)
                
            # Safely decode user input 
            user_input = raw_input.decode('utf-8', errors='replace').strip()
            
            # Empty entries are ignored
            if not user_input:
                continue
                
            # Exit conditions
            if user_input.lower() in ['quit', 'exit']:
                break
                
            # 2. Inform the user we are processing
            print(f"\n{COLOR_YELLOW}[Agy] (thinking...){COLOR_RESET}")
            
            # 3. Resolve binary and construct the backend shell array
            agy_bin = shutil.which("agy") or shutil.which("agy.exe")
            if not agy_bin:
                print(f"{COLOR_RED}[Fatal]{COLOR_RESET} Antigravity binary ('agy' / 'agy.exe') not found in system PATH.")
                break
                
            cmd = [agy_bin, "--model", args.model]
            
            if args.auto_approve:
                cmd.append("--dangerously-skip-permissions")

            # First turn forces a fresh slate, subsequent turns use Antigravity's continuity 
            if is_first_turn:
                cmd.append("--new-project")
            else:
                cmd.append("--continue")
            
            # The heart of the bypass: --print executes generation fully headless, skipping UI block flags
            cmd.extend(["--print", user_input])
            
            # Execute subprocess natively
            result = subprocess.run(cmd, env=env, text=True)
            
            # 4. Handle Subprocess Edge Cases
            if result.returncode != 0:
                print(f"{COLOR_RED}[Error]{COLOR_RESET} Process exited with code {result.returncode}")
            
            # State mutation: subsequent loops must use --continue
            is_first_turn = False
            print("\n" + "-" * 60)
            
        except (KeyboardInterrupt, EOFError):
            print("\nExiting gracefully. Goodbye!")
            break
        except Exception as e:
            print(f"\n{COLOR_RED}[System Error]{COLOR_RESET} {str(e)}")

if __name__ == "__main__":
    main()
