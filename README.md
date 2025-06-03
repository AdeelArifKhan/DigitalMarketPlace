# Digital Marketplace Smart Contract

A Python implementation of a digital marketplace smart contract on the Algorand blockchain.

""This is inprocess phase before testing"

## Features

- Fixed total supply of 100 million tokens with 8 decimal precision
- Deposit and withdrawal functionality
- Fixed transaction fee system (0.0001945 USDT per transaction) 
- Staking rewards system (5% in ALGO for holders with 10K+ USDT worth)
- Stable fee mechanism regardless of ALGO price fluctuations
- GitHub handle storage in contract box

## Project Structure

```
digital_marketplace/
├── __init__.py      # Package initialization
├── config.py        # Configuration parameters
├── contract.py      # Main contract implementation
└── utils.py         # Utility functions
```

## Requirements

- Python 3.9+
- py-algorand-sdk
- requests
- Docker and Docker Compose

## Deployment Instructions

1. Build and start the Docker container:
```bash
docker-compose build
docker-compose up
```

2. The deployment script will:
   - Create a new Algorand account
   - Deploy the contract to Lora testnet
   - Store the GitHub handle (adeelarifkhan) in a box
   - Save the Application ID to workshop-submission.txt

3. Fund your account:
   - Copy the displayed address
   - Visit the [Algorand Testnet Dispenser](https://bank.testnet.algorand.network/)
   - Request test ALGO tokens

4. After funding, the contract will be deployed automatically

## Important Notes

1. Save the mnemonic phrase displayed during deployment
2. The Application ID will be saved in workshop-submission.txt
3. Verify deployment on [Algorand Lora Testnet Explorer](https://testnet.algoexplorer.io/)

## License

MIT
