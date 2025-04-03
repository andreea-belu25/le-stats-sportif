import json
import sys
from pprint import pprint

def load_json_file(file_path):
    """Load data from a JSON file"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None

def compare_json_data(file1_path, file2_path):
    """Compare data from two JSON files"""
    # Load data from both files
    data1 = load_json_file(file1_path)
    data2 = load_json_file(file2_path)
    
    if data1 is None or data2 is None:
        return
    
    # Check if both are dictionaries
    if not isinstance(data1, dict) or not isinstance(data2, dict):
        print("One or both files don't contain a JSON object (dictionary)")
        return
    
    # Compare keys
    keys1 = set(data1.keys())
    keys2 = set(data2.keys())
    
    keys_only_in_1 = keys1 - keys2
    keys_only_in_2 = keys2 - keys1
    common_keys = keys1.intersection(keys2)
    
    # Print summary
    print(f"Comparing {file1_path} and {file2_path}:")
    print(f"Total keys in first file: {len(keys1)}")
    print(f"Total keys in second file: {len(keys2)}")
    print(f"Keys only in first file: {len(keys_only_in_1)}")
    print(f"Keys only in second file: {len(keys_only_in_2)}")
    print(f"Common keys: {len(common_keys)}")
    
    # Show keys that differ
    if keys_only_in_1:
        print("\nKeys only in first file:")
        for key in sorted(keys_only_in_1):
            print(f"  - {key}")
    
    if keys_only_in_2:
        print("\nKeys only in second file:")
        for key in sorted(keys_only_in_2):
            print(f"  - {key}")
    
    # Compare values for common keys
    value_differences = {}
    for key in common_keys:
        if data1[key] != data2[key]:
            value_differences[key] = {
                "file1": data1[key],
                "file2": data2[key],
                "difference": data2[key] - data1[key] if isinstance(data1[key], (int, float)) and isinstance(data2[key], (int, float)) else "N/A"
            }
    
    if value_differences:
        print("\nDifferent values for common keys:")
        for key, diff in sorted(value_differences.items()):
            if isinstance(diff["difference"], (int, float)):
                print(f"  - {key}: {diff['file1']} vs {diff['file2']} (diff: {diff['difference']:.6f})")
            else:
                print(f"  - {key}: {diff['file1']} vs {diff['file2']}")
    else:
        print("\nAll common keys have the same values.")

    # Check if files are identical
    if not keys_only_in_1 and not keys_only_in_2 and not value_differences:
        print("\nThe two JSON files contain identical data.")
    else:
        print("\nThe two JSON files contain different data.")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Use command line arguments if provided
        file1_path = sys.argv[1]
        file2_path = sys.argv[2]
    else:
        # Otherwise use hardcoded paths
        file1_path = "out.json"
        file2_path = "../tests/state_mean_by_category/output/out-1.json"
    
    compare_json_data(file1_path, file2_path)