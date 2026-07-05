import os
import subprocess

def search_files_for_key(directory, key_pattern):
    print("\n--- Scanning files for API Key pattern ---")
    found_any = False
    # Common extensions to scan
    text_extensions = {'.txt', '.py', '.js', '.jsx', '.json', '.html', '.css', '.sh', '.bat', '.env', '.example', '.md', '.yml', '.yaml'}
    
    for root, dirs, files in os.walk(directory):
        # Skip git directory
        if '.git' in root or 'node_modules' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            
            # Scan files with text extensions or files starting with '.' (like .env)
            if ext.lower() in text_extensions or file.startswith('.'):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if key_pattern in content:
                            print(f"[FOUND KEY] File: {os.path.relpath(file_path, directory)}")
                            found_any = True
                except Exception as e:
                    pass
    if not found_any:
        print("No files containing the API key pattern were found outside of git history.")

def run_git_diagnostics():
    print("=" * 60)
    print("Git Diagnostic Status, Tracked Files & Secret Scan")
    print("=" * 60)
    
    # 1. Run git status
    print("\n--- git status ---")
    status = subprocess.run(["git", "status"], capture_output=True, text=True, shell=True)
    print(status.stdout)
    if status.stderr:
        print("Error:")
        print(status.stderr)
        
    # 2. Run git ls-files to see tracked files
    print("\n--- git ls-files (files currently tracked in Git index) ---")
    ls_files = subprocess.run(["git", "ls-files"], capture_output=True, text=True, shell=True)
    print(ls_files.stdout)
    if ls_files.stderr:
        print("Error:")
        print(ls_files.stderr)

    # 3. Check if .env is ignored
    print("\n--- Checking if .env is ignored by Git ---")
    check_ignore = subprocess.run(["git", "check-ignore", "-v", ".env"], capture_output=True, text=True, shell=True)
    print(check_ignore.stdout)
    if check_ignore.stderr:
        print("Error/Info:")
        print(check_ignore.stderr)

    # 4. Search files for API Key
    search_files_for_key(".", "AQ.Ab8RN")

if __name__ == "__main__":
    run_git_diagnostics()
