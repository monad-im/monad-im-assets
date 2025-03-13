import os
import json
from PIL import Image

# Configuration
base_input_dir = 'D:\monad import\hashlipsart\layers'  # Base folder for all layers
output_dir = 'NFTs'  # Define your output folder
json_output_dir = 'NFT_JSONs'  # Define output folder for individual JSONs
new_uri = "bafybeibdhjugr2jcj6mrmdghuyaxrk3gwxmldfrszz3avmwhsahgvgfw34"  # New URI to replace placeholder

ranks = ["A", "B", "C", "D", "E"]  # List of ranks excluding KING
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

# Starting ID and edition for KING rank
KING_id = 1  # Fixed ID for KING

# Create metadata entry for KING rank
KING_metadata_entry = {
    "id": str(KING_id),  # Fixed ID for KING
    "name": "KINGNADS_KING_1", 
    "description": "RANK KING 1", 
    "image": f"ipfs://{new_uri}/KINGNADS_KING_1.png",  # Updated URI
    "edition": KING_id,  # Fixed edition for KING
    "attributes": [
        {
            "trait_type": "RANK_LETTER",
            "value": "KING"
        },
        {
            "trait_type": "RANK_NUMBER",
            "value": "1"
        }
    ]
}
metadata.append(KING_metadata_entry)

# Save individual JSON for the KING NFT
individual_json_path = os.path.join(json_output_dir, 'KINGNADS_KING_1.json')
with open(individual_json_path, 'w') as json_file:
    json.dump(KING_metadata_entry, json_file, indent=4)

# Start generating NFTs for the ranks with ID starting at 2
nft_id_counter = 2  

# Generate NFTs for the ranks
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
                "id": str(nft_id_counter),  # Unique ID matches edition
                "name": f"KINGNADS_{rank}_{idx}", 
                "description": f"RANK {rank} {idx}", 
                "image": f"ipfs://{new_uri}/KINGNADS_{rank}_{idx}.png",  # Updated URI
                "edition": nft_id_counter,  # Edition equals ID
                "attributes": [
                    {
                        "trait_type": "RANK_LETTER",
                        "value": rank  
                    },
                    {
                        "trait_type": "RANK_NUMBER",
                        "value": str(idx)  
                    }
                ]
            }
            metadata.append(metadata_entry)

            # Save individual JSON for the NFT
            individual_json_path = os.path.join(json_output_dir, f'KINGNADS_{rank}_{idx}.json')
            with open(individual_json_path, 'w') as json_file:
                json.dump(metadata_entry, json_file, indent=4)

            # Increment the counter for the next NFT
            nft_id_counter += 1

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

print(f"NFT generation complete! {len(metadata)} NFTs created, including KING rank.")