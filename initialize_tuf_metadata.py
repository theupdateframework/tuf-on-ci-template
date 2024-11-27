import os
from datetime import datetime, timedelta
from tuf.api.metadata import Metadata, Root, Targets, Snapshot, Timestamp
from tuf.api.serialization.json import JSONSerializer

# Paths
base_dir = os.getcwd()
targets_dir = os.path.join(base_dir, "targets")
metadata_dir = os.path.join(base_dir, "metadata")

# Ensure directories exist
os.makedirs(metadata_dir, exist_ok=True)

# Set expiration dates for metadata as datetime objects
root_expiration = datetime(2024, 11, 27, 0, 0, 0)
targets_expiration = datetime(2024, 2, 25, 0, 0, 0)
snapshot_expiration = datetime(2024, 1, 1, 0, 0, 0)
timestamp_expiration = datetime(2023, 12, 1, 0, 0, 0)

# Create Root metadata
root = Root()
root.version = 1
root.expires = root_expiration
root.add_key(
    "root", 
    "/home/sormazabal/src/TUF_Implementation/keys-tuf-on-ci-template/5ed593335ffa94b67518af247244c3002c9caa3227798b658c3b560c8d6af559.pub"
)

# Create Targets metadata
targets = Targets()
targets.version = 1
targets.expires = targets_expiration

# Add target files
for target_file in os.listdir(targets_dir):
    target_path = os.path.join(targets_dir, target_file)
    if os.path.isfile(target_path):
        targets.add_target(target_file)

# Create Snapshot metadata
snapshot = Snapshot()
snapshot.version = 1
snapshot.expires = snapshot_expiration

# Create Timestamp metadata
timestamp = Timestamp()
timestamp.version = 1
timestamp.expires = timestamp_expiration

# Serialize metadata to disk
serializer = JSONSerializer()

metadata_files = {
    "root.json": Metadata(root),
    "targets.json": Metadata(targets),
    "snapshot.json": Metadata(snapshot),
    "timestamp.json": Metadata(timestamp),
}

for filename, metadata in metadata_files.items():
    with open(os.path.join(metadata_dir, filename), "w") as f:
        f.write(serializer.serialize(metadata))

print(f"Metadata files created in {metadata_dir}")
