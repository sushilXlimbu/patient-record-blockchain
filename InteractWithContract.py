"""
Python Interaction Script for PatientRecordContract
=====================================================
PRChain Solutions Ltd. — HealthCare Innovations Ltd.

This script connects to the deployed PatientRecordContract on the Sepolia
test network and demonstrates programmatic interaction with the smart
contract using the web3.py library.

Prerequisites
-------------
    pip install web3

References
----------
    Web3.py Documentation: https://web3py.readthedocs.io/
    Ethereum Foundation (2024) 'Interacting with Smart Contracts'.
"""

from web3 import Web3
import json
import time


# ==========================================================================
# Configuration — UPDATE THESE VALUES WITH YOUR OWN
# ==========================================================================

INFURA_URL = "https://sepolia.infura.io/v3/324d9d36417c46989e7632b8a0c2****"

CONTRACT_ADDRESS = "0x8825ac40E6d2F634724F6bD1C2B3bf4825832186"

OWNER_PRIVATE_KEY = "f0465fcb5fa4df20330e8fa16e5d8550c71b1fa8bd84a302ff4fe684eb307***"

PROVIDER_PRIVATE_KEY = "8a7b1256e97a16dcaa4d1fae63a14583f71e0d3214360c5b746801f8b69fe***"

# ABI from Remix compiler output
CONTRACT_ABI = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "patientId",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "diagnosis",
				"type": "string"
			}
		],
		"name": "addRecord",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "providerAddress",
				"type": "address"
			}
		],
		"name": "authorizeProvider",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "patientId",
				"type": "string"
			}
		],
		"name": "deactivateRecord",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "provider",
				"type": "address"
			}
		],
		"name": "ProviderAuthorized",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "provider",
				"type": "address"
			}
		],
		"name": "ProviderRevoked",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "string",
				"name": "patientId",
				"type": "string"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "provider",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "RecordAdded",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "string",
				"name": "patientId",
				"type": "string"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "fromProvider",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "toProvider",
				"type": "address"
			}
		],
		"name": "RecordTransferred",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "providerAddress",
				"type": "address"
			}
		],
		"name": "revokeProvider",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "patientId",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "newProvider",
				"type": "address"
			}
		],
		"name": "transferRecord",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "authorizedProviders",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "patientId",
				"type": "string"
			}
		],
		"name": "getRecord",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "patientId",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "diagnosis",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "provider",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					},
					{
						"internalType": "bool",
						"name": "isActive",
						"type": "bool"
					}
				],
				"internalType": "struct PatientRecordContract.PatientRecord",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "providerAddress",
				"type": "address"
			}
		],
		"name": "isAuthorized",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalRecords",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]


# ==========================================================================
# Helper Functions
# ==========================================================================

def connect_to_network():
    """
    Establish a connection to the Sepolia test network via Infura.

    Returns
    -------
    Web3
        A connected Web3 instance.
    """
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

    if w3.is_connected():
        print(f"Connected to Sepolia network")
        print(f"  Chain ID    : {w3.eth.chain_id}")
        print(f"  Block number: {w3.eth.block_number}")
    else:
        print("ERROR: Failed to connect to Sepolia.")
        exit(1)

    return w3


def get_contract(w3):
    """
    Create a contract instance from the ABI and deployed address.

    Parameters
    ----------
    w3 : Web3
        Connected Web3 instance.

    Returns
    -------
    Contract
        A web3 Contract object for interaction.
    """
    contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
    print(f"  Contract    : {contract_address}")
    return contract


def send_transaction(w3, contract_function, private_key):
    """
    Build, sign, and send a transaction for a contract function call.

    This function handles the full transaction lifecycle:
    1. Build the transaction with gas estimation and current nonce.
    2. Sign it with the caller's private key.
    3. Send the signed transaction to the network.
    4. Wait for the transaction receipt (confirmation).

    Parameters
    ----------
    w3 : Web3
        Connected Web3 instance.
    contract_function : ContractFunction
        The contract function call to execute.
    private_key : str
        Private key of the account sending the transaction.

    Returns
    -------
    TxReceipt
        The transaction receipt after confirmation.
    """
    account = w3.eth.account.from_key(private_key)
    
    latest_block = w3.eth.get_block('latest')
    base_fee = latest_block['baseFeePerGas']
    
    tx = contract_function.build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 500000,
        'maxFeePerGas': base_fee * 3,
        'maxPriorityFeePerGas': w3.to_wei(2, 'gwei'),
        'chainId': w3.eth.chain_id
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"  Tx sent     : {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    print(f"  Tx confirmed: Block #{receipt['blockNumber']} | "
          f"Gas used: {receipt['gasUsed']}")

    return receipt


# ==========================================================================
# Interaction Demonstrations
# ==========================================================================

def demo_read_contract_state(contract):
    """Read and display the current contract state."""
    print("\n" + "=" * 60)
    print("READING CONTRACT STATE")
    print("=" * 60)

    owner = contract.functions.owner().call()
    total = contract.functions.totalRecords().call()

    print(f"  Owner address  : {owner}")
    print(f"  Total records  : {total}")

    return total


def demo_authorise_provider(w3, contract, provider_address):
    """Authorise a new healthcare provider."""
    print("\n" + "=" * 60)
    print(f"AUTHORISING PROVIDER: {provider_address}")
    print("=" * 60)

    is_auth = contract.functions.isAuthorized(provider_address).call()
    if is_auth:
        print(f"  Provider is already authorised. Skipping.")
        return

    tx_func = contract.functions.authorizeProvider(provider_address)
    receipt = send_transaction(w3, tx_func, OWNER_PRIVATE_KEY)
    print(f"  Status: {'Success' if receipt['status'] == 1 else 'Failed'}")


def demo_add_record(w3, contract, patient_id, patient_name, diagnosis, private_key):
    """Add a new patient record."""
    print("\n" + "=" * 60)
    print(f"ADDING PATIENT RECORD: {patient_name} (ID: {patient_id})")
    print("=" * 60)

    tx_func = contract.functions.addRecord(patient_id, patient_name, diagnosis)
    receipt = send_transaction(w3, tx_func, private_key)
    print(f"  Status: {'Success' if receipt['status'] == 1 else 'Failed'}")

    total = contract.functions.totalRecords().call()
    print(f"  Total records now: {total}")

    return total


def demo_get_record(contract, patient_id):
    """Retrieve and display a patient record."""
    print("\n" + "=" * 60)
    print(f"RETRIEVING RECORD: {patient_id}")
    print("=" * 60)

    result = contract.functions.getRecord(patient_id).call({
    'from': Web3.to_checksum_address("0x6AbB16E9e972CBb0ec27d53AEbfd12Fdf543563B")
    })

    print(f"  Patient ID   : {result[0]}")
    print(f"  Name         : {result[1]}")
    print(f"  Diagnosis    : {result[2]}")
    print(f"  Provider     : {result[3]}")
    print(f"  Timestamp    : {result[4]}")
    print(f"  Active       : {result[5]}")

    return result


def demo_transfer_record(w3, contract, patient_id, to_address, private_key):
    """Transfer a patient record to another provider."""
    print("\n" + "=" * 60)
    print(f"TRANSFERRING RECORD: {patient_id}")
    print("=" * 60)

    to_checksum = Web3.to_checksum_address(to_address)
    tx_func = contract.functions.transferRecord(patient_id, to_checksum)
    receipt = send_transaction(w3, tx_func, private_key)
    print(f"  Status       : {'Success' if receipt['status'] == 1 else 'Failed'}")
    print(f"  Transferred to: {to_checksum}")


def demo_deactivate_record(w3, contract, patient_id, private_key):
    """Deactivate a patient record."""
    print("\n" + "=" * 60)
    print(f"DEACTIVATING RECORD: {patient_id}")
    print("=" * 60)

    tx_func = contract.functions.deactivateRecord(patient_id)
    receipt = send_transaction(w3, tx_func, private_key)
    print(f"  Status: {'Success' if receipt['status'] == 1 else 'Failed'}")


# ==========================================================================
# Main Execution
# ==========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PRChain — Smart Contract Interaction Script")
    print("=" * 60)

    # --- Step 1: Connect to Sepolia ---
    w3 = connect_to_network()
    contract = get_contract(w3)

    # Derive addresses from private keys
    owner_account = w3.eth.account.from_key(OWNER_PRIVATE_KEY)
    provider_account = w3.eth.account.from_key(PROVIDER_PRIVATE_KEY)
    print(f"  Owner account   : {owner_account.address}")
    print(f"  Provider account: {provider_account.address}")

    # --- Step 2: Read initial state ---
    demo_read_contract_state(contract)

    # --- Step 3: Authorise second provider ---
    demo_authorise_provider(
        w3, contract,
        provider_address=provider_account.address
    )

    # Verify authorisation
    is_auth = contract.functions.isAuthorized(provider_account.address).call()
    print(f"  Provider authorised: {is_auth}")

    # --- Step 4: Add patient records (as owner) ---
    demo_add_record(
        w3, contract,
        patient_id="P001",
        patient_name="John Smith",
        diagnosis="Type 2 Diabetes Mellitus",
        private_key=OWNER_PRIVATE_KEY
    )

    demo_add_record(
        w3, contract,
        patient_id="P002",
        patient_name="Sarah Johnson",
        diagnosis="Hypertension Stage 1",
        private_key=OWNER_PRIVATE_KEY
    )

    # --- Step 5: Add a record as the second provider ---
    demo_add_record(
        w3, contract,
        patient_id="P003",
        patient_name="David Brown",
        diagnosis="Acute Bronchitis",
        private_key=PROVIDER_PRIVATE_KEY
    )

    # --- Step 6: Retrieve all records ---
    demo_get_record(contract, "P001")
    demo_get_record(contract, "P002")
    demo_get_record(contract, "P003")

    # --- Step 7: Transfer record P001 to second provider ---
    demo_transfer_record(
        w3, contract,
        patient_id="P001",
        to_address=provider_account.address,
        private_key=OWNER_PRIVATE_KEY
    )

    # Verify the transfer — provider address should have changed
    print("\nVerifying transfer...")
    demo_get_record(contract, "P001")

    # --- Step 8: Final state ---
    demo_read_contract_state(contract)

    print("\n" + "=" * 60)
    print("All interactions completed successfully.")
    print("=" * 60)