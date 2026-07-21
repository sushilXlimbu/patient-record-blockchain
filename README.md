# Blockchain-Based Patient Record Management System

A two-part blockchain project for healthcare record management:

1. A **basic blockchain built in Python** with a proof-of-work mining mechanism and a longest-chain consensus rule.
2. A **Solidity smart contract** (`PatientRecordContract`) that tracks patient records on-chain and transfers them between authorised healthcare providers, deployed and tested on the Ethereum **Sepolia** testnet.

A Python interaction script uses `web3.py` to talk to the deployed contract, add new records, and transfer records between two Ethereum accounts.

> Built as an academic exploration of blockchain fundamentals, cryptographic hashing, and smart contract development for a healthcare use case.

## Features

**Python blockchain**
* Block structure containing index, previous hash, timestamp, data, and its own SHA-256 hash
* Genesis block creation
* Proof-of-work mining with an adjustable difficulty target
* Chain validation and a longest-chain consensus rule for resolving competing chains

**Solidity smart contract (`PatientRecordContract`)**
* `totalRecords` state variable tracking the number of records on-chain
* Function to add a new patient record
* Function to transfer a record between authorised providers
* Access control so only authorised addresses can act on records
* Events emitted on record creation and transfer for off-chain tracking

**Interaction layer**
* `web3.py` script to connect to Sepolia, call contract functions, and read state
* Demonstrates a full add-then-transfer flow between two accounts

## Tech Stack

| Layer | Tools |
| --- | --- |
| Blockchain prototype | Python 3, `hashlib` (SHA-256) |
| Smart contract | Solidity |
| Compile and deploy | Remix IDE (or Hardhat / Truffle) |
| Network | Ethereum Sepolia testnet |
| Contract interaction | `web3.py` |
| RPC and wallet | Infura or Alchemy endpoint, MetaMask |

## Project Structure

```
patient-record-blockchain/
├── blockchain/
│   └── blockchain.py             # Python proof-of-work blockchain
├── contracts/
│   └── PatientRecordContract.sol # Solidity smart contract
├── scripts/
│   └── interact.py               # web3.py script to call the deployed contract
├── tests/
│   └── test_blockchain.py        # Test cases for the Python blockchain
├── report/
│   └── report.pdf                # Written report and documentation
├── requirements.txt
└── README.md
```

Adjust the paths above to match how your files are actually organised.

## Prerequisites

* Python 3.9 or newer
* A funded Sepolia testnet account (get test ETH from a Sepolia faucet)
* An RPC endpoint from Infura or Alchemy
* MetaMask (optional, useful for managing test accounts)

## Installation

```bash
git clone https://github.com/<your-username>/patient-record-blockchain.git
cd patient-record-blockchain
pip install -r requirements.txt
```

Create a `.env` file for your secrets (never commit this):

```
SEPOLIA_RPC_URL=your_infura_or_alchemy_url
PRIVATE_KEY=your_test_account_private_key
CONTRACT_ADDRESS=your_deployed_contract_address
```

> Use a throwaway test account only. Do not put a private key holding real funds anywhere near this file.

## Usage

### 1. Run the Python blockchain

```bash
python blockchain/blockchain.py
```

This creates the genesis block, mines several blocks under proof-of-work, prints each block's hash, and validates the chain.

### 2. Compile and deploy the smart contract

Compile `contracts/PatientRecordContract.sol` in Remix (or with Hardhat / Truffle), then deploy it to the Sepolia testnet. Once the deployment transaction is confirmed, copy the contract address into your `.env` file.

### 3. Interact with the deployed contract

```bash
python scripts/interact.py
```

This connects to Sepolia, adds a new patient record, transfers it to a second account, and reads back `totalRecords` to confirm the state change.

## Smart Contract Overview

| Item | Purpose |
| --- | --- |
| `totalRecords` | Running count of patient records stored on-chain |
| `addRecord(...)` | Creates a new record and increments `totalRecords` |
| `transferRecord(...)` | Moves a record from one authorised provider to another |
| `onlyAuthorised` modifier | Restricts sensitive functions to approved addresses |

Fill in the exact function signatures to match your implementation.

## Testing

```bash
python -m pytest tests/
```

Tests cover block creation, hash integrity, proof-of-work correctness, tampering detection, and the longest-chain rule. Smart contract functions are tested through the interaction script and confirmed transactions on Sepolia.

## Limitations

* The Python blockchain is a learning prototype, not a production ledger: it runs in a single process with no real peer-to-peer networking.
* Proof-of-work difficulty is fixed rather than dynamically adjusted.
* Storing real patient data on a public chain raises privacy and regulatory concerns; a production system would keep sensitive data off-chain and store only references or hashes.
* Gas costs and testnet reliability can affect contract interactions.

## Future Work

* Peer-to-peer networking and node synchronisation for the Python chain
* Dynamic difficulty adjustment
* Off-chain storage with on-chain hashing for privacy
* Role-based access control and audit logging in the contract

## License

Released under the MIT License. See `LICENSE` for details.

## Author

**Your Name**
[GitHub](https://github.com/<your-username>) · [LinkedIn](https://linkedin.com/in/<your-profile>)
