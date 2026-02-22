#!/usr/bin/env python
"""
Final Comprehensive Test Summary for Task 15
Runs all test suites and provides a complete status report
"""

import subprocess
import sys

# All test files in the project
test_files = [
    "test_utils.py",
    "test_pattern_detector.py",
    "test_credibility_analyzer.py",
    "test_task8.py",
    "test_task8_integration.py",
    "test_integration_credibility.py",
    "test_json_formatter.py",
    "test_json_formatter_comprehensive.py",
    "test_integration_json_formatter.py",
    "test_flask_analyze_endpoint.py",
    "test_requirements_validation.py",
    "test_security.py"
]

print("=" * 80)
print("FINAL COMPREHENSIVE TEST SUITE - TASK 15")
print("News Credibility and Misinformation Analysis Assistant")
print("=" * 80)
print()

all_passed = True
results = []
total_tests = len(test_files)

for i, test_file in enumerate(test_files, 1):
    print(f"[{i}/{total_tests}] Running: {test_file}")
    print("-" * 80)
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Show abbreviated output
            lines = result.stdout.strip().split('\n')
            if len(lines) > 10:
                print('\n'.join(lines[:3]))
                print(f"... ({len(lines) - 6} lines omitted) ...")
                print('\n'.join(lines[-3:]))
            else:
                print(result.stdout)
            results.append((test_file, "✅ PASSED"))
        else:
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            results.append((test_file, "❌ FAILED"))
            all_passed = False
    except subprocess.TimeoutExpired:
        print(f"⏱️  TIMEOUT: Test exceeded 30 seconds")
        results.append((test_file, "⏱️  TIMEOUT"))
        all_passed = False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        results.append((test_file, "❌ ERROR"))
        all_passed = False
    
    print()

print("=" * 80)
print("FINAL TEST RESULTS SUMMARY")
print("=" * 80)
print()

# Group results by category
categories = {
    "Core Utilities": ["test_utils.py"],
    "Pattern Detection": ["test_pattern_detector.py"],
    "Credibility Analysis": ["test_credibility_analyzer.py", "test_integration_credibility.py"],
    "Task 8 Implementation": ["test_task8.py", "test_task8_integration.py"],
    "JSON Formatting": ["test_json_formatter.py", "test_json_formatter_comprehensive.py", "test_integration_json_formatter.py"],
    "Flask Integration": ["test_flask_analyze_endpoint.py"],
    "Requirements Validation": ["test_requirements_validation.py"],
    "Security": ["test_security.py"]
}

for category, files in categories.items():
    print(f"\n{category}:")
    for test_file, status in results:
        if test_file in files:
            print(f"  {status} {test_file}")

print()
print("=" * 80)

passed_count = sum(1 for _, status in results if "PASSED" in status)
failed_count = total_tests - passed_count

print(f"Total Tests: {total_tests}")
print(f"Passed: {passed_count}")
print(f"Failed: {failed_count}")
print()

if all_passed:
    print("🎉 ALL TEST SUITES PASSED SUCCESSFULLY!")
    print()
    print("The News Credibility and Misinformation Analysis Assistant is fully")
    print("functional and ready for deployment. All requirements have been validated.")
    sys.exit(0)
else:
    print("⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
    sys.exit(1)
