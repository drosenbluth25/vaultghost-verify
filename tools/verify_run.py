import json
import sys
import hashlib
from pathlib import Path

def canonicalize(data):
    """Returns a deterministic JSON string representation."""
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def verify_manifest(manifest_path):
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        run_id = manifest.get("run_id", "unknown")
        steps = manifest.get("steps", [])
        final_receipt = manifest.get("final_receipt", "")
        
        # 1. Validate Hash Chain
        current_hash = None
        for i, step in enumerate(steps):
            # In a real scenario, we might re-calculate output_hash from input_hash + action
            # For this minimal version, we verify the chain link
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
            
        # 3. Print Deterministic Output
        print("VaultGhost Verification Report")
        print("==============================")
        print(f"Run ID: {run_id}")
        print("Status: VERIFIED")
        print(f"Steps Validated: {len(steps)}")
        print("Hash Chain: OK")
        print("Receipt Match: OK")
        print(f"Final Hash: {current_hash}")
        
        return True
    except Exception as e:
        print(f"Verification Error: {str(e)}")
        return False

if __name__ == "__main__":
    manifest_file = Path(__file__).parent.parent / "data" / "run_manifest.json"
    success = verify_manifest(manifest_file)
    sys.exit(0 if success else 1)
