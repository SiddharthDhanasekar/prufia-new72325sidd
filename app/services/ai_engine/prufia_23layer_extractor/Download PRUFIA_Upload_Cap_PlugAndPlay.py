
# PRUFIA Beta Limit Enforcement
def enforce_upload_limit(file_paths):
    if len(file_paths) > 50:
        raise ValueError("Upload limit exceeded: Maximum 50 documents allowed per batch during PRUFIA beta test.")
    return file_paths

# Example usage
# Inside your batch runner script before processing begins:
file_paths = enforce_upload_limit(file_paths)
