import os
import random
import shutil

# Params to change

# Where you're getting data from
data_dir = "C:/Users/danie/OneDrive/Documentos/Fall_2024_Classes/EECE5554/project/sample/2015-08-12-15-04-18" # Replace with your actual data directory

# Dataset name
data_name = "2015-08-12-15-04-18" # Replace with your dataset name (if needed)

# Who collected the data
collector_name = "dk"

# Where you're putting the data
output_base_dir = "C:/Users/danie/OneDrive/Documentos/Fall_2024_Classes/EECE5554/project/three_sec" # Replace with the path where you want 'test_outputs' to be created

centre_dir = os.path.join(data_dir, 'stereo', 'centre')
timestamps_file = os.path.join(data_dir, 'stereo.timestamps')

test_outputs_dir = os.path.join(output_base_dir, f"{data_name}_samples")

# Create the 'test_outputs' directory
os.makedirs(test_outputs_dir, exist_ok=True)

# Read the timestamps from the file
with open(timestamps_file, 'r') as f:
    lines = f.readlines()

# Extract timestamps and ensure corresponding images exist
timestamps = []
timestamp_lines = []
for line in lines:
    timestamp = line.strip().split()[0]
    image_file = os.path.join(centre_dir, f"{timestamp}.png")
    if os.path.isfile(image_file):
        timestamps.append(timestamp)
        timestamp_lines.append(line.strip())

# Check if there are enough images
sequence_length = 45
total_images = len(timestamps)
number_of_samples = total_images // sequence_length

if number_of_samples == 0:
    print(f"Not enough images to create sequences of {sequence_length} images.")
    exit(1)

# Generate start indices for sequences
start_indices = [i * sequence_length for i in range(number_of_samples)]

# Randomize the order of sequences
random.shuffle(start_indices)

# Create sample folders and copy images and timestamps
for sample_number, start_idx in enumerate(start_indices, 1):
    # Define the sample directory path inside 'test_outputs'
    sample_dir_name = f"{data_name}_sample_{sample_number}_{collector_name}"
    sample_dir = os.path.join(test_outputs_dir, sample_dir_name)
    sample_stereo_dir = os.path.join(sample_dir, 'stereo')
    sample_centre_dir = os.path.join(sample_stereo_dir, 'centre')
    os.makedirs(sample_centre_dir, exist_ok=True)
    
    sample_timestamps = []
    for idx in range(start_idx, start_idx + sequence_length):
        timestamp = timestamps[idx]
        src_file = os.path.join(centre_dir, f"{timestamp}.png")
        dst_file = os.path.join(sample_centre_dir, f"{timestamp}.png")
        shutil.copyfile(src_file, dst_file)
        sample_timestamps.append(timestamp_lines[idx])
    
    # Write the stereo.timestamps file in the sample directory
    sample_timestamps_file = os.path.join(sample_dir, 'stereo.timestamps')
    with open(sample_timestamps_file, 'w') as f:
        f.write('\n'.join(sample_timestamps))

print(f"Successfully created {number_of_samples} samples with {sequence_length} consecutive images each in '{test_outputs_dir}'.")
