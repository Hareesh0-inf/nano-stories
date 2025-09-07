#!/usr/bin/env python3
"""
Test runner script for the Brand Storytelling API
"""
import sys
import subprocess
import os
from pathlib import Path

def run_tests(test_type="all", coverage=True):
    """Run tests with specified configuration"""

    # Get the project root directory
    project_root = Path(__file__).parent

    # Change to project root
    os.chdir(project_root)

    # Base pytest command
    cmd = ["python", "-m", "pytest"]

    if test_type == "unit":
        cmd.append("backend/tests/unit/")
        cmd.append("-m unit")
    elif test_type == "integration":
        cmd.append("backend/tests/integration/")
        cmd.append("-m integration")
    elif test_type == "contract":
        cmd.append("backend/tests/contract/")
        cmd.append("-m contract")
    else:
        # Run all tests
        cmd.append("backend/tests/")

    if coverage:
        cmd.extend([
            "--cov=backend/src",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-fail-under=80"
        ])

    cmd.extend([
        "--verbose",
        "--tb=short",
        "--strict-markers"
    ])

    print(f"Running command: {' '.join(cmd)}")
    print("=" * 50)

    try:
        result = subprocess.run(cmd, check=True)
        print("=" * 50)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print("=" * 50)
        print(f"❌ Tests failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ Python or pytest not found. Please ensure Python and pytest are installed.")
        return False

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        if test_type not in ["unit", "integration", "contract", "all"]:
            print("Usage: python run_tests.py [unit|integration|contract|all]")
            print("Default: all")
            sys.exit(1)
    else:
        test_type = "all"

    # Check if coverage should be enabled
    coverage = "--no-cov" not in sys.argv

    success = run_tests(test_type, coverage)

    if not success:
        sys.exit(1)

    print("\n🎉 Test run completed successfully!")

if __name__ == "__main__":
    main()
