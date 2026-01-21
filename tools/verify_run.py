import json
import sys
import hashlib
from pathlib import Path

def canonicalize(data):
    """Returns a deterministic JSON string representation."""
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def verify_manifest(manifest_path, expected_output_path=None):
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        run_id = manifest.get("run_id", "unknown")
        steps = manifest.get("steps", [])
        final_receipt = manifest.get("final_receipt", "")
        
        # 1. Validate Hash Chain
        current_hash = None
        for i, step in enumerate(steps):
            if i > 0:
                if step["input_hash"] != steps[i-1]["output_hash"]:
                    print(f"Verification Failed: Hash chain broken at step {step['id']}")
                    return False
            current_hash = step["output_hash"]
            
        # 2. Validate Receipt
        expected_receipt = f"vaultghost-receipt-v1-{current_hash}"
        if final_receipt != expected_receipt:
            print(f"Verification Failed: Receipt mismatch. Expected {expected_receipt}, got {final_receipt}")
            return False
            
        # 3. Generate Deterministic Output
        output_lines = [
            "VaultGhost Verification Report",
            "==============================",
            f"Run ID: {run_id}",
            "Status: VERIFIED",
            f"Steps Validated: {len(steps)}",
            "Hash Chain: OK",
            "Receipt Match: OK",
            f"Final Hash: {current_hash}"
        ]
        actual_output = "\n".join(output_lines)
        
        # 4. Byte-for-byte enforcement if expected output is provided
        if expected_output_path:
            with open(expected_output_path, 'r') as f:
                expected_output = f.read().strip()
            if actual_output.strip() != expected_output:
                print("Verification Failed: Output mismatch against EXPECTED_OUTPUT.txt")
                return False

        print(actual_output)
        return True
    except Exception as e:
        print(f"Verification Error: {str(e)}")
        return False

if __name__ == "__main__":
    root_dir = Path(__file__).parent.parent
    manifest_file = root_dir / "data" / "run_manifest.json"
    expected_file = root_dir / "EXPECTED_OUTPUT.txt"
    
    success = verify_manifest(manifest_file, expected_file)
    sys.exit(0 if success else 1)
