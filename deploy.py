"""
Script to deploy the Digital Marketplace contract to Algorand Lora testnet.
"""
import os
from algosdk import account, mnemonic
from algosdk.v2client import algod
from digital_marketplace.contract import DigitalMarketplace

def main():
    # Get environment variables
    github_handle = os.getenv("GITHUB_HANDLE")
    if not github_handle:
        raise ValueError("GITHUB_HANDLE environment variable is required")

    # Connect to Algorand node
    algod_address = os.getenv("ALGORAND_NODE", "https://testnet-api.algonode.cloud")
    algod_token = ""  # Not required for public nodes
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Create new account for contract deployment
    private_key, address = account.generate_account()
    print(f"Created new account: {address}")
    print(f"Save this mnemonic safely: {mnemonic.from_private_key(private_key)}")

    # Initialize contract
    contract = DigitalMarketplace(
        algod_client=algod_client,
        creator_address=address,
        creator_private_key=private_key,
        github_handle=github_handle
    )

    # Create token
    try:
        asset_id = contract.create_token()
        print(f"Token created successfully with Asset ID: {asset_id}")
        
        # Save Application ID to workshop-submission.txt
        with open("workshop-submission.txt", "w") as f:
            f.write(str(asset_id))
        
        print("Deployment complete! Application ID saved to workshop-submission.txt")
        
    except Exception as e:
        print(f"Error deploying contract: {e}")

if __name__ == "__main__":
    main()