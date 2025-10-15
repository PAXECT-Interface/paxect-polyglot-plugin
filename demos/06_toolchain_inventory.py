#!/usr/bin/env python3
# Demo 06 - Toolchain inventory (Python, cross-OS)
# Goal: softly list presence + version of common tools across OSes; always end with OK.

import sys, time, shutil, subprocess

TOOLS = [
    # shells
    ("bash", ["bash", "--version"]),
    ("zsh", ["zsh", "--version"]),
    ("pwsh", ["pwsh", "--version"]),
    ("powershell", ["powershell", "-NoLogo", "-NoProfile", "-Command", "$PSVersionTable.PSVersion"]),
    # VCS / net
    ("git", ["git", "--version"]),
    ("curl", ["curl", "--version"]),
    # languages / runtimes
    ("python3", ["python3", "--version"]),
    ("py", ["py", "-V"]),  # Windows launcher
    ("node", ["node", "--version"]),
    ("npm", ["npm", "--version"]),
    ("go", ["go", "version"]),
    ("rustc", ["rustc", "--version"]),
    ("cargo", ["cargo", "--version"]),
    ("javac", ["javac", "-version"]),
    ("java", ["java", "-version"]),
    ("dotnet", ["dotnet", "--version"]),
    ("php", ["php", "-v"]),
    ("swift", ["swift", "--version"]),
    # build tools
    ("gcc", ["gcc", "--version"]),
    ("g++", ["g++", "--version"]),
    ("clang", ["clang", "--version"]),
    ("cmake", ["cmake", "--version"]),
    ("make", ["make", "--version"]),
    # mobile / apple
    ("adb", ["adb", "version"]),
    ("xcodebuild", ["xcodebuild", "-version"]),
]

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S', time.gmtime())}] {msg}")

def has_cmd(name: str) -> bool:
    return shutil.which(name) is not None

def run(cmd):
    try:
        p = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = (p.stdout or "").strip()
        err = (p.stderr or "").strip()
        return p.returncode, out, err
    except Exception as e:
        return 127, "", str(e)

def main() -> int:
    log("06 - Toolchain inventory (Python)")
    for name, cmd in TOOLS:
        if not has_cmd(name):
            log(f"{name}: missing (soft)")
            continue
        rc, out, err = run(cmd)
        if rc == 0:
            # print the first line only (keep it tidy)
            first = (out or err).splitlines()[0] if (out or err) else f"{name} ok"
            log(f"{name}: {first}")
        else:
            msg = (out or err) or f"exit {rc}"
            log(f"{name}: detected but issue (soft): {msg}")

    log("OK")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr); sys.exit(3)
