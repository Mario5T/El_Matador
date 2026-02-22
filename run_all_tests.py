#!/usr/bin/env python
"""
Test runner for Task 10 Checkpoint - runs all test suites
"""

import subprocess
import sys

test_files = [
    "test_utils.py",
    "test_pattern_detector.py",
    "test_credibility_analyzer.py",
    "test_task8.py",
    "test_task8_integration.py",
    "test_integration_credibility.py"
]

print("=" * 60)
print("Running All Tests for Task 10 Checkpoint")
print("=" * 60)
print()

all_passed = True
results = []

for i, test_file in enumerate(test_files, 1):
    print(f"Test Suite {i}: {test_file}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(result.stdout)
            results.append((test_file, "PASSED"))
        else:
            print(result.stdout)
            print(result.stderr)
            results.append((test_file, "FAILED"))
            all_passed = False
    except Exception as e:
        print(f"ERROR: {e}")
        results.append((test_file, "ERROR"))
        all_passed = False
    
    print()

print("=" * 60)
print("Test Results Summary")
print("=" * 60)
for test_file, status in results:
    status_symbol = "✅" if status == "PASSED" else "❌"
    print(f"{status_symbol} {test_file}: {status}")

print()
if all_passed:
    print("✅ ALL TEST SUITES COMPLETED SUCCESSFULLY!")
    sys.exit(0)
else:
    print("❌ SOME TESTS FAILED")
    sys.exit(1)
