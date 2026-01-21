import unittest
import subprocess
import sys
from pathlib import Path

class TestVaultGhostVerification(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
        self.verify_script = self.root_dir / "tools" / "verify_run.py"
        self.expected_output_file = self.root_dir / "EXPECTED_OUTPUT.txt"

    def test_deterministic_output(self):
        """Ensure the verification script produces exactly the expected output."""
        result = subprocess.run(
            [sys.executable, str(self.verify_script)],
            capture_output=True,
            text=True,
            check=True
        )
        
        with open(self.expected_output_file, 'r') as f:
            expected = f.read().strip()
            
        self.assertEqual(result.stdout.strip(), expected)
        self.assertEqual(result.returncode, 0)

    def test_failure_on_tamper(self):
        """Ensure verification fails if the manifest is tampered with."""
        manifest_path = self.root_dir / "data" / "run_manifest.json"
        original_content = manifest_path.read_text()
        
        try:
            # Tamper with the manifest
            # Replace ONLY the output_hash in one step to break the chain or receipt match
            # The original content has "6b86b273" in both the last step output and the final receipt.
            # By replacing only one occurrence, we break the consistency.
            tampered_content = original_content.replace("6b86b273", "deadbeef", 1)
            manifest_path.write_text(tampered_content)
            
            # Use the same python as the one running the test (which should be the poetry venv)
            result = subprocess.run(
                [sys.executable, str(self.verify_script)],
                capture_output=True,
                text=True
            )
            
            print(f"DEBUG: returncode={result.returncode}")
            print(f"DEBUG: stdout={result.stdout}")
            
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Verification Failed", result.stdout)
            
        finally:
            # Restore original content
            manifest_path.write_text(original_content)

if __name__ == "__main__":
    unittest.main()
