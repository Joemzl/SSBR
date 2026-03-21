"""
Download and setup bge-reranker-base model.
Handles Windows symlink permission issues by copying files directly.
"""

import os
import sys
import shutil

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=" * 60)
print("Setup: BAAI/bge-reranker-base for Windows")
print("=" * 60)

# Paths
HF_CACHE = os.path.join(os.environ.get('USERPROFILE', ''), '.cache', 'huggingface', 'hub')
MODEL_DIR = os.path.join(HF_CACHE, 'models--BAAI--bge-reranker-base')
BLOBS_DIR = os.path.join(MODEL_DIR, 'blobs')
SNAPSHOT_DIR = os.path.join(MODEL_DIR, 'snapshots', '2cfc18c9415c912f9d8155881c133215df768a70')

# File mapping: blob hash -> filename
FILE_MAPPING = {
    'ff248a5f7d76e27b10778b3c593c9fba1df4c448': 'config.json',
    '059214673d9d6d2ee319411e2ffec8c024b816d5': 'tokenizer_config.json',
    '9eb652ac4e40cc093272bbbe0f55d521cf67570060227109b5cdc20945a4489e': 'tokenizer.json',
    'cfc8146abe2a0488e9e2a0c56de7952f7c11ab059eca145a0a727afce0db2865': 'sentencepiece.bpe.model',
    '68171d1ff68b731a33d119708476692c094a466b': 'special_tokens_map.json',
    '5b475bec40425c52229bbc63f9f50e290315c29f4e52c8f8dd404a159c0469fa': 'pytorch_model.bin',
    'ced967c45fd1902eb92716c9ceeca7c95a936770ea9db611f5a841b926e33fbd': 'model.safetensors',
}

# Check if blobs exist
if not os.path.exists(BLOBS_DIR):
    print("[ERROR] Model not downloaded yet!")
    print("The blobs directory does not exist.")
    print("\nPlease run the download first (may need good network):")
    print("  python -c \"from huggingface_hub import snapshot_download; snapshot_download('BAAI/bge-reranker-base', force_download=True)\"")
    sys.exit(1)

print(f"\nBlobs directory: {BLOBS_DIR}")
print(f"Snapshot directory: {SNAPSHOT_DIR}")

# Ensure snapshot directory exists
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Copy files from blobs to snapshot (workaround for Windows symlink issues)
print("\nCopying files from blobs to snapshot directory...")
copied = 0
for blob_hash, filename in FILE_MAPPING.items():
    src = os.path.join(BLOBS_DIR, blob_hash)
    dst = os.path.join(SNAPSHOT_DIR, filename)
    
    if os.path.exists(src):
        if not os.path.exists(dst):
            print(f"  Copying {filename}...")
            shutil.copy2(src, dst)
            copied += 1
        else:
            print(f"  {filename} already exists")
    else:
        print(f"  [WARN] Blob not found: {blob_hash} ({filename})")

print(f"\nCopied {copied} new files.")

# List snapshot directory
print("\nSnapshot directory contents:")
for f in os.listdir(SNAPSHOT_DIR):
    fpath = os.path.join(SNAPSHOT_DIR, f)
    if os.path.isfile(fpath):
        size = os.path.getsize(fpath)
        print(f"  {f}: {size:,} bytes")
    else:
        print(f"  {f}/ (directory)")

# Test loading
print("\n" + "=" * 60)
print("Testing CrossEncoder loading...")
print("=" * 60)

try:
    from sentence_transformers import CrossEncoder
    
    model = CrossEncoder('BAAI/bge-reranker-base')
    
    # Quick test
    pairs = [
        ("How to improve silica dispersion?", "TESPT coupling agent improves silica dispersion."),
        ("How to improve silica dispersion?", "This is about polymer synthesis.")
    ]
    scores = model.predict(pairs)
    
    print(f"\nTest scores: {scores}")
    print("\n" + "=" * 60)
    print("[SUCCESS] Reranker model is ready to use!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
