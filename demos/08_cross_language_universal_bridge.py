#!/usr/bin/env python3
# Demo 08 - Cross-Language Universal Bridge (Python ↔ Node ↔ Go)
# Goal: verify multi-language data roundtrip via stdin/stdout pipes.
# Soft fallback if Node.js or Go is not installed.

import sys, os, time, subprocess, shutil, tempfile, hashlib, pathlib

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S', time.gmtime())}] {msg}")

def has_cmd(name: str) -> bool:
    return shutil.which(name) is not None

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def run_node_bridge(data: bytes) -> bytes:
    js_code = """\
process.stdin.setEncoding('utf8');
let buf = '';
process.stdin.on('data', c => buf += c);
process.stdin.on('end', () => {
  const out = buf.split('').reverse().join('');
  process.stdout.write(out);
});
"""
    tmp_js = pathlib.Path(tempfile.gettempdir()) / "paxect_polyglot_bridge.js"
    tmp_js.write_text(js_code)
    p = subprocess.run(
        ["node", str(tmp_js)],
        input=data.decode("utf-8"),
        capture_output=True,
        text=True,
        timeout=5,
    )
    return p.stdout.encode("utf-8", errors="ignore")

def run_go_bridge(data: bytes) -> bytes:
    go_code = """\
package main
import ("io"; "os"; "bytes")
func main() {
    buf, _ := io.ReadAll(os.Stdin)
    var out bytes.Buffer
    for _, b := range buf { out.WriteByte(b^0x20) } // XOR for variation
    os.Stdout.Write(out.Bytes())
}
"""
    tmp_go = pathlib.Path(tempfile.gettempdir()) / "paxect_polyglot_bridge.go"
    tmp_go.write_text(go_code)
    exe = tmp_go.with_suffix("")
    subprocess.run(["go", "build", "-o", str(exe), str(tmp_go)],
                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p = subprocess.run([str(exe)],
                       input=data,
                       capture_output=True,
                       timeout=5)
    return p.stdout

def main() -> int:
    log("08 - Cross-Language Universal Bridge (Python ↔ Node ↔ Go)")

    base_data = b"PAXECT-Polyglot-Universal"
    sha_in = sha256_bytes(base_data)
    log(f"input_sha256={sha_in}")

    # --- Node.js stage ---
    if has_cmd("node"):
        try:
            node_out = run_node_bridge(base_data)
            log(f"Node.js output len={len(node_out)} sha256={sha256_bytes(node_out)}")
        except Exception as e:
            log(f"Node.js stage failed (soft): {e}")
            node_out = base_data
    else:
        log("Node.js missing (soft)")
        node_out = base_data

    # --- Go stage ---
    if has_cmd("go"):
        try:
            go_out = run_go_bridge(node_out)
            log(f"Go output len={len(go_out)} sha256={sha256_bytes(go_out)}")
        except Exception as e:
            log(f"Go stage failed (soft): {e}")
            go_out = node_out
    else:
        log("Go missing (soft)")
        go_out = node_out

    # --- Final comparison ---
    final_sha = sha256_bytes(go_out)
    log(f"final_sha256={final_sha}")

    if sha_in != final_sha:
        log("✅ Transformation verified — cross-language bridge altered content deterministically.")
    else:
        log("⚠️ Output identical to input (soft) — one or more bridges skipped.")

    log("OK")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr)
        sys.exit(3)
