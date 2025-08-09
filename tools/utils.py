import hashlib
import json


def generate_id(_dict):
    """Generate a unique hash ID based on repository information."""
    # Create a string representation of the repo info (excluding any existing _id)
    repo_str = json.dumps({k: v for k, v in _dict.items() if k != '_id'}, sort_keys=True)
    # Generate SHA256 hash
    return hashlib.sha256(repo_str.encode('utf-8')).hexdigest()
