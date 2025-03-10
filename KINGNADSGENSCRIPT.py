import os
import json
from PIL import Image

# Configuration
base_input_dir = 'REPLACE HEREEEEEEEEEEEEEEEEEEEEE DIR'  # Base folder for all layers
output_dir = 'NFTs'  # Define your output folder
json_output_dir = 'NFT_JSONs'  # Define output folder for individual JSONs
new_uri = "bafybeif6renouyi4trqqqlivqqmzc2do6jxwpi24mm52zrft7tqwkm56gy"  # New URI to replace placeholder

ranks = ["A", "B", "C", "D", "E"]  # List of ranks
num_nfts_per_rank = 18  # Total unique NFTs per rank
metadata = []

# Create output directories
os.makedirs(output_dir, exist_ok=True)
os.makedirs(json_output_dir, exist_ok=True)

# Function to combine layers
def combine_layers(base_layer, badge_layer, rank_layer):
    base = Image.open(base_layer).convert("RGBA")
    badge = Image.open(badge_layer).convert("RGBA")
    rank = Image.open(rank_layer).convert("RGBA")
    
    # Composite layers
    combined = Image.alpha_composite(base, badge)
    combined = Image.alpha_composite(combined, rank)
    
    return combined

# Generate NFTs
for rank_index, rank in enumerate(ranks):
    rank_input_dir = os.path.join(base_input_dir, f'RANK {rank}')  # Directory for the current rank
    rank_directory = f'RANK{rank}'  # New directory name without a space
    rank_output_dir = os.path.join(output_dir, rank_directory)
    os.makedirs(rank_output_dir, exist_ok=True)  # Create folder for each rank

    # Generate NFTs in reverse order (from 18 to 1)
    for idx in range(num_nfts_per_rank, 0, -1):  # Generates 18 to 1
        # Define file paths to layer images
        base_layer_path = os.path.join(rank_input_dir, 'BASE', f'{rank_index + 1}.png')  # Base is based on rank index
        badge_layer_path = os.path.join(rank_input_dir, 'BADGE', f'badge_rank_{num_nfts_per_rank - idx + 1}.png')  # Pick corresponding badge
        rank_layer_path = os.path.join(rank_input_dir, 'RANK', f'rank_{rank_index + 1}_{num_nfts_per_rank - idx + 1}.png')  # Pick corresponding rank

        # Check if all layers exist
        if os.path.exists(base_layer_path) and os.path.exists(badge_layer_path) and os.path.exists(rank_layer_path):
            # Combine layers to create final NFT image
            combined_image = combine_layers(base_layer_path, badge_layer_path, rank_layer_path)

            # Save the final NFT image in the corresponding rank folder
            nft_image_path = os.path.join(rank_output_dir, f'KINGNADS_{rank}_{idx}.png')
            combined_image.save(nft_image_path)

            # Create and append metadata entry
            metadata_entry = {
                "id": str(rank_index * num_nfts_per_rank + (num_nfts_per_rank - idx + 1)),  # Unique ID for each NFT
                "name": f"KINGNADS_{rank}_{idx}",  
                "high_res_img_url": f"ipfs://NewUriToReplace/KINGNADS_{rank}_{idx}.png",  # Placeholder URI
                "edition": rank_index * num_nfts_per_rank + (num_nfts_per_rank - idx + 1),
                "attributes": [
                    {
                        "trait_type": "BASE",
                        "value": str(rank_index + 1)  # Using rank index for base
                    },
                    {
                        "trait_type": "BADGE",
                        "value": f"badge_rank_{num_nfts_per_rank - idx + 1}"  
                    },
                    {
                        "trait_type": "RANK",
                        "value": f"rank_{rank_index + 1}_{num_nfts_per_rank - idx + 1}"  
                    }
                ]
            }
            metadata.append(metadata_entry)

            # Save individual JSON for the NFT
            individual_json_path = os.path.join(json_output_dir, f'KINGNADS_{rank}_{idx}.json')
            with open(individual_json_path, 'w') as json_file:
                json.dump(metadata_entry, json_file, indent=4)

        else:
            # Debugging output for missing files
            print(f"Missing files for NFT {rank_index * num_nfts_per_rank + (num_nfts_per_rank - idx + 1)}:")
            if not os.path.exists(base_layer_path):
                print(f"  Base Layer Missing: {base_layer_path}")
            if not os.path.exists(badge_layer_path):
                print(f"  Badge Layer Missing: {badge_layer_path}")
            if not os.path.exists(rank_layer_path):
                print(f"  Rank Layer Missing: {rank_layer_path}")

# Export combined metadata to JSON file
metadata_file_path = os.path.join(output_dir, 'nft_metadata.json')
with open(metadata_file_path, 'w') as f:
    json.dump(metadata, f, indent=4)

# Function to update all JSON files with the new URI
def update_json_uris():
    # Update individual NFT JSON files
    for rank in ranks:
        for idx in range(num_nfts_per_rank, 0, -1):
            individual_json_path = os.path.join(json_output_dir, f'KINGNADS_{rank}_{idx}.json')
            if os.path.exists(individual_json_path):
                with open(individual_json_path, 'r+') as json_file:
                    data = json.load(json_file)
                    # Update the high_res_img_url
                    data['high_res_img_url'] = data['high_res_img_url'].replace("NewUriToReplace", new_uri)
                    json_file.seek(0)
                    json.dump(data, json_file, indent=4)
                    json_file.truncate()

    # Update the combined metadata JSON file
    if os.path.exists(metadata_file_path):
        with open(metadata_file_path, 'r+') as json_file:
            data = json.load(json_file)
            for entry in data:
                entry['high_res_img_url'] = entry['high_res_img_url'].replace("NewUriToReplace", new_uri)
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()

# Call the update function
update_json_uris()

print(f"NFT generation complete! {len(metadata)} NFTs created and JSON URIs updated.")