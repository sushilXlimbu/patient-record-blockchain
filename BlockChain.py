"""
Blockchain Implementation for Patient Record Management
=========================================================
PRChain Solutions Ltd. — HealthCare Innovations Ltd.

"""

import hashlib
import json
import time
from typing import Any


class Block:

    def __init__(self, index: int, previous_hash: str, timestamp: float,
                 data: Any, nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:

        block_content = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_content.encode('utf-8')).hexdigest()

    def to_dict(self) -> dict:
        """Return a dictionary representation of the block for display."""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "nonce": self.nonce,
            "hash": self.hash
        }

    def __repr__(self) -> str:
        return (f"Block(index={self.index}, hash={self.hash[:16]}..., "
                f"nonce={self.nonce})")


class Blockchain:

    def __init__(self, difficulty: int = 4):
        self.chain: list[Block] = []
        self.difficulty = difficulty
        self.pending_records: list[dict] = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None: #Builds and mines the first block (index 0)
       
        genesis_block = Block(
            index=0,
            previous_hash="0",
            timestamp=time.time(),
            data={"message": "Genesis Block - PRChain Healthcare Blockchain"},
            nonce=0
        )
        # Mine the genesis block to satisfy difficulty requirement
        genesis_block = self._proof_of_work(genesis_block)
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        """Return the most recent block in the chain."""
        return self.chain[-1]

    def _proof_of_work(self, block: Block) -> Block: #Block Mining Mechanism
      
        target = "0" * self.difficulty
        block.nonce = 0
        block.hash = block.compute_hash()

        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.compute_hash()

        return block

    def add_patient_record(self, patient_id: str, patient_name: str, #Adds patient record into blockchain
                           diagnosis: str, provider: str) -> None:
        
        record = {
            "patient_id": patient_id,
            "patient_name": patient_name,
            "diagnosis": diagnosis,
            "provider": provider,
            "record_timestamp": time.time()
        }
        self.pending_records.append(record)

    def mine_pending_records(self) -> Block | None: #Takes all pending records, packs them into a new block, mines it (proof of work), appends it to the chain, and clears the pending list.

        if not self.pending_records:
            print("No pending records to mine.")
            return None

        new_block = Block(
            index=len(self.chain),
            previous_hash=self.last_block.hash,
            timestamp=time.time(),
            data=self.pending_records.copy()
        )

        mined_block = self._proof_of_work(new_block)
        self.chain.append(mined_block)
        self.pending_records = []

        print(f"Block #{mined_block.index} mined successfully. "
              f"Hash: {mined_block.hash[:20]}... | Nonce: {mined_block.nonce}")
        return mined_block

    def is_chain_valid(self, chain: list[Block] | None = None) -> bool: #Checks if the chain is valid or not
        """
        Validate the integrity of the entire blockchain.
        Checks two invariants for every block after the genesis:
        1. The block's stored hash matches its recomputed hash (no tampering).
        2. The block's previous_hash matches the hash of the prior block
        """
        if chain is None:
            chain = self.chain

        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]

            # Check 1: Has the block been tampered with?
            if current.hash != current.compute_hash():
                print(f"Block #{current.index}: hash mismatch — "
                      f"block has been tampered with.")
                return False

            # Check 2: Is the chain linkage intact?
            if current.previous_hash != previous.hash:
                print(f"Block #{current.index}: previous_hash does not match "
                      f"hash of block #{previous.index}.")
                return False

            # Check 3: Does the hash meet the difficulty requirement?
            if not current.hash.startswith("0" * self.difficulty):
                print(f"Block #{current.index}: hash does not meet "
                      f"difficulty requirement.")
                return False

        return True

    def resolve_conflicts(self, other_chains: list[list[Block]]) -> bool: #implements longest-chain consensus

        longest_chain = self.chain
        chain_replaced = False

        for candidate_chain in other_chains:
            # Only consider chains longer than ours
            if len(candidate_chain) <= len(longest_chain):
                continue

            # Only accept the chain if it is valid
            if not self.is_chain_valid(candidate_chain):
                print("Rejected a longer chain — failed validation.")
                continue

            longest_chain = candidate_chain
            chain_replaced = True

        if chain_replaced:
            self.chain = longest_chain
            print(f"Chain replaced. New chain length: {len(self.chain)}")
        else:
            print("Current chain retained — it is already the longest "
                  "valid chain.")

        return chain_replaced

    def get_records_for_patient(self, patient_id: str) -> list[dict]: #gets patient record from the blockchain

        results = []
        for block in self.chain[1:]:  # Skip genesis
            if isinstance(block.data, list):
                for record in block.data:
                    if record.get("patient_id") == patient_id:
                        results.append({
                            "block_index": block.index,
                            "block_hash": block.hash,
                            **record
                        })
        return results

    def display_chain(self) -> None: #displays whole chain
        """Print a formatted view of the entire blockchain."""
        print("\n" + "=" * 70)
        print("BLOCKCHAIN — PRChain Healthcare Ledger")
        print(f"Chain length: {len(self.chain)} blocks | "
              f"Difficulty: {self.difficulty} | "
              f"Valid: {self.is_chain_valid()}")
        print("=" * 70)

        for block in self.chain:
            print(f"\n--- Block #{block.index} ---")
            print(f"  Timestamp  : {time.ctime(block.timestamp)}")
            print(f"  Prev Hash  : {block.previous_hash[:32]}...")
            print(f"  Hash       : {block.hash[:32]}...")
            print(f"  Nonce      : {block.nonce}")
            if isinstance(block.data, list):
                print(f"  Records    : {len(block.data)} patient record(s)")
                for rec in block.data:
                    print(f"    - Patient {rec['patient_id']}: "
                          f"{rec['patient_name']} | {rec['diagnosis']} | "
                          f"Provider: {rec['provider']}")
            else:
                print(f"  Data       : {block.data}")

        print("\n" + "=" * 70)


# ==========================================================================
# Demonstration
# ==========================================================================

if __name__ == "__main__":
    print("Initialising PRChain Healthcare Blockchain...")
    print("Mining difficulty: 4 (hash must start with '0000')\n")

    # --- Create the blockchain ---
    bc = Blockchain(difficulty=4)
    print(f"Genesis block created. Hash: {bc.chain[0].hash[:20]}...\n")

    # --- Add patient records ---
    print("Adding patient records...\n")

    bc.add_patient_record(
        patient_id="P001",
        patient_name="John Smith",
        diagnosis="Type 2 Diabetes",
        provider="Dr. Patel — City Hospital"
    )
    bc.add_patient_record(
        patient_id="P002",
        patient_name="Sarah Johnson",
        diagnosis="Hypertension Stage 1",
        provider="Dr. Williams — Royal Clinic"
    )

    # Mine the first batch
    bc.mine_pending_records()

    # Add more records
    bc.add_patient_record(
        patient_id="P003",
        patient_name="David Brown",
        diagnosis="Acute Bronchitis",
        provider="Dr. Patel — City Hospital"
    )
    bc.add_patient_record(
        patient_id="P001",
        patient_name="John Smith",
        diagnosis="Follow-up: HbA1c 6.8%",
        provider="Dr. Khan — Diabetes Centre"
    )

    # Mine the second batch
    bc.mine_pending_records()

    # --- Display the full chain ---
    bc.display_chain()

    # --- Demonstrate patient record retrieval ---
    print("\nSearching for all records for patient P001...")
    p001_records = bc.get_records_for_patient("P001")
    for rec in p001_records:
        print(f"  Block #{rec['block_index']}: {rec['diagnosis']} "
              f"(Provider: {rec['provider']})")

    # --- Validate chain integrity ---
    print(f"\nChain valid: {bc.is_chain_valid()}")

    # --- Demonstrate tamper detection ---
    print("\n--- Tamper Detection Demo ---")
    print("Attempting to alter Block #1 data...")
    bc.chain[1].data[0]["diagnosis"] = "TAMPERED DATA"
    print(f"Chain valid after tampering: {bc.is_chain_valid()}")

    # Restore for consensus demo
    bc.chain[1].data[0]["diagnosis"] = "Type 2 Diabetes"
    bc.chain[1].hash = bc.chain[1].compute_hash()

    # --- Demonstrate consensus mechanism ---
    print("\n--- Consensus Mechanism Demo ---")
    print("Simulating a competing chain from another node...\n")

    # Create a competing (shorter) chain
    competing_node = Blockchain(difficulty=4)
    competing_node.add_patient_record(
        patient_id="P010",
        patient_name="Competitor Record",
        diagnosis="Test",
        provider="Other Hospital"
    )
    competing_node.mine_pending_records()

    print(f"Our chain length: {len(bc.chain)}")
    print(f"Competing chain length: {len(competing_node.chain)}")

    # Our chain is longer, so it should be retained
    replaced = bc.resolve_conflicts([competing_node.chain])
    print(f"Chain replaced: {replaced}")

    # Now simulate a longer competing chain
    print("\nSimulating a LONGER competing chain...")
    longer_node = Blockchain(difficulty=4)
    for i in range(5):
        longer_node.add_patient_record(
            patient_id=f"PX{i}",
            patient_name=f"Patient {i}",
            diagnosis=f"Condition {i}",
            provider="Remote Hospital"
        )
        longer_node.mine_pending_records()

    print(f"Our chain length: {len(bc.chain)}")
    print(f"Longer chain length: {len(longer_node.chain)}")

    replaced = bc.resolve_conflicts([longer_node.chain])
    print(f"Chain replaced: {replaced}")
    print(f"New chain length: {len(bc.chain)}")