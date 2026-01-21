import subprocess
import sys
from pathlib import Path

def run_tamper_check():
    root_dir = Path(__file__).parent.parent
    manifest_path = root_dir / "data" / "run_manifest.json"
    verify_script = root_dir / "tools" / "verify_run.py"
    
    # Read original content
    with open(manifest_path, 'r') as f:
        original_content = f.read()
    
    try:
        # Tamper with the manifest
        tampered_content = original_content.replace("6b86b273", "deadbeef", 1)
        with open(manifest_path, 'w') as f:
            f.write(tampered_content)
        
        # Run the verification script
        result = subprocess.run(
            [sys.executable, str(verify_script)],
            capture_output=True,
            text=True
        )
        
        # We EXPECT it to fail (non-zero exit code)
        if result.returncode != 0:
            print("Tamper Detection Successful: Script returned non-zero exit code.")
            print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print("Tamper Detection FAILED: Script returned zero exit code despite tampering.")
            return False
            
    finally:
        # Restore original content
        with open(manifest_path, 'w') as f:
            f.write(original_content)

if __name__ == "__main__":
    success = run_tamper_check()
    # The auditor wants "Tamper Code" to be 1 (or >0) to signal an alert.
    # If success is True, it means tampering was detected, so we return 1.
    sys.exit(1 if success else 0)
