"""
Testing Script — PRChain Healthcare Blockchain

This script executes test cases step-by-step for the blockchain
that i created, printing clear evidence of each test's input, expected
outcome, and actual result.

Test Categories:
    TC-01 to TC-03: Genesis Block & Block Structure
    TC-04 to TC-06: Patient Record Management
    TC-07 to TC-09: Proof-of-Work Mechanism
    TC-10 to TC-13: Chain Integrity & Tamper Detection
    TC-14 to TC-17: Consensus Mechanism
    TC-18 to TC-20: Edge Cases
"""

import time
import copy
from BlockChain import Block, Blockchain


def print_header(test_id, title):
    """Print a formatted test case header."""
    print("\n" + "=" * 70)
    print(f"  {test_id}: {title}")
    print("=" * 70)


def print_result(passed):
    """Print pass/fail result."""
    status = "PASSED" if passed else "FAILED"
    print(f"\n  Result: [{status}]")


# GENESIS BLOCK & BLOCK STRUCTURE TESTS

print("\n" + "#" * 70)
print("  SECTION 1: GENESIS BLOCK & BLOCK STRUCTURE")
print("#" * 70)

print_header("TC-01", "Genesis Block Creation")
print("  Description: Verify the blockchain initialises with a genesis block")
print("  Expected: Chain length = 1, genesis index = 0, previous_hash = '0'")

bc = Blockchain(difficulty=4)
genesis = bc.chain[0]

print(f"\n  Chain length     : {len(bc.chain)}")
print(f"  Genesis index    : {genesis.index}")
print(f"  Previous hash    : {genesis.previous_hash}")
print(f"  Genesis hash     : {genesis.hash}")
print(f"  Genesis nonce    : {genesis.nonce}")
print(f"  Genesis data     : {genesis.data}")

passed = (len(bc.chain) == 1 and genesis.index == 0
          and genesis.previous_hash == "0")
print_result(passed)


print_header("TC-02", "Block Structure Verification")
print("  Description: Verify each block contains required fields")
print("  Expected: index, previous_hash, timestamp, data, nonce, hash")

bc.add_patient_record("P001", "Alice Green", "Flu", "Dr. Patel")
block = bc.mine_pending_records()

print(f"\n  index         : {block.index}")
print(f"  previous_hash : {block.previous_hash[:40]}...")
print(f"  timestamp     : {block.timestamp} ({time.ctime(block.timestamp)})")
print(f"  data          : {block.data}")
print(f"  nonce         : {block.nonce}")
print(f"  hash          : {block.hash}")

has_all = all([
    hasattr(block, 'index'),
    hasattr(block, 'previous_hash'),
    hasattr(block, 'timestamp'),
    hasattr(block, 'data'),
    hasattr(block, 'nonce'),
    hasattr(block, 'hash')
])
print_result(has_all)


print_header("TC-03", "Hash Determinism")
print("  Description: Same block data must produce the same hash every time")
print("  Expected: Two compute_hash() calls return identical results")

hash_1 = block.compute_hash()
hash_2 = block.compute_hash()

print(f"\n  Hash attempt 1 : {hash_1}")
print(f"  Hash attempt 2 : {hash_2}")
print(f"  Hashes match   : {hash_1 == hash_2}")

print_result(hash_1 == hash_2)


# PATIENT RECORD MANAGEMENT TESTS

print("\n" + "#" * 70)
print("  SECTION 2: PATIENT RECORD MANAGEMENT")
print("#" * 70)

# Fresh blockchain for this section
bc = Blockchain(difficulty=4)

print_header("TC-04", "Adding and Mining Patient Records")
print("  Description: Add multiple patient records and mine them into a block")
print("  Expected: Block mined with 2 records, totalRecords = 2")

bc.add_patient_record("P001", "John Smith", "Type 2 Diabetes", "Dr. Patel")
bc.add_patient_record("P002", "Sarah Johnson", "Hypertension", "Dr. Williams")
mined = bc.mine_pending_records()

print(f"\n  Block index       : {mined.index}")
print(f"  Records in block  : {len(mined.data)}")
print(f"  Chain length      : {len(bc.chain)}")
print(f"  Pending records   : {len(bc.pending_records)}")
for rec in mined.data:
    print(f"    - {rec['patient_id']}: {rec['patient_name']} | {rec['diagnosis']}")

passed = (len(mined.data) == 2 and len(bc.pending_records) == 0
          and len(bc.chain) == 2)
print_result(passed)


print_header("TC-05", "Mining With No Pending Records")
print("  Description: Attempt to mine when no records are pending")
print("  Expected: Returns None, no new block added")

chain_len_before = len(bc.chain)
result = bc.mine_pending_records()

print(f"\n  Return value       : {result}")
print(f"  Chain length before: {chain_len_before}")
print(f"  Chain length after : {len(bc.chain)}")

print_result(result is None and len(bc.chain) == chain_len_before)


print_header("TC-06", "Patient Record Retrieval Across Blocks")
print("  Description: Retrieve all records for a patient across multiple blocks")
print("  Expected: Patient P001 appears in 2 blocks with different diagnoses")

bc.add_patient_record("P001", "John Smith", "Follow-up: HbA1c 6.8%", "Dr. Khan")
bc.add_patient_record("P003", "David Brown", "Bronchitis", "Dr. Patel")
bc.mine_pending_records()

records = bc.get_records_for_patient("P001")
print(f"\n  Records found for P001: {len(records)}")
for rec in records:
    print(f"    Block #{rec['block_index']}: {rec['diagnosis']} "
          f"(Provider: {rec['provider']})")

# Also test non-existent patient
empty = bc.get_records_for_patient("P999")
print(f"\n  Records for non-existent P999: {len(empty)}")

print_result(len(records) == 2 and len(empty) == 0)


# PROOF-OF-WORK MECHANISM TESTS

print("\n" + "#" * 70)
print("  SECTION 3: PROOF-OF-WORK MECHANISM")
print("#" * 70)

print_header("TC-07", "Hash Meets Difficulty Requirement")
print("  Description: All mined block hashes must start with '0000' (difficulty=4)")
print("  Expected: Every block hash begins with 4 leading zeros")

all_valid = True
for block in bc.chain:
    meets = block.hash.startswith("0" * bc.difficulty)
    status = "PASS" if meets else "FAIL"
    print(f"\n  Block #{block.index}: {block.hash[:20]}... [{status}]")
    print(f"    Nonce: {block.nonce}")
    if not meets:
        all_valid = False

print_result(all_valid)


print_header("TC-08", "Proof-of-Work Computational Effort")
print("  Description: Demonstrate that PoW requires significant nonce iterations")
print("  Expected: Nonce > 0 for mined blocks (non-trivial computation)")

bc_test = Blockchain(difficulty=4)
bc_test.add_patient_record("TEST", "Test Patient", "Test Diagnosis", "Dr. Test")
test_block = bc_test.mine_pending_records()

print(f"\n  Difficulty    : {bc_test.difficulty}")
print(f"  Nonce found   : {test_block.nonce}")
print(f"  Hash produced : {test_block.hash}")
print(f"  Starts with '0000': {test_block.hash.startswith('0000')}")
print(f"  Iterations needed : {test_block.nonce} attempts")

print_result(test_block.nonce > 0 and test_block.hash.startswith("0000"))


print_header("TC-09", "Different Difficulty Levels")
print("  Description: Higher difficulty requires more leading zeros")
print("  Expected: Difficulty 2 → '00', Difficulty 3 → '000'")

bc_d2 = Blockchain(difficulty=2)
bc_d2.add_patient_record("T1", "Test", "Test", "Dr.")
block_d2 = bc_d2.mine_pending_records()

bc_d3 = Blockchain(difficulty=3)
bc_d3.add_patient_record("T1", "Test", "Test", "Dr.")
block_d3 = bc_d3.mine_pending_records()

print(f"\n  Difficulty 2:")
print(f"    Hash  : {block_d2.hash[:20]}...")
print(f"    Nonce : {block_d2.nonce}")
print(f"    Valid : {block_d2.hash.startswith('00')}")

print(f"\n  Difficulty 3:")
print(f"    Hash  : {block_d3.hash[:20]}...")
print(f"    Nonce : {block_d3.nonce}")
print(f"    Valid : {block_d3.hash.startswith('000')}")

print(f"\n  Higher difficulty needed more iterations: "
      f"{block_d3.nonce > block_d2.nonce}")

print_result(
    block_d2.hash.startswith("00") and block_d3.hash.startswith("000")
)


# CHAIN INTEGRITY & TAMPER DETECTION TESTS

print("\n" + "#" * 70)
print("  SECTION 4: CHAIN INTEGRITY & TAMPER DETECTION")
print("#" * 70)

# Fresh blockchain for integrity tests
bc = Blockchain(difficulty=4)
bc.add_patient_record("P001", "Alice", "Diabetes", "Dr. X")
bc.mine_pending_records()
bc.add_patient_record("P002", "Bob", "Asthma", "Dr. Y")
bc.mine_pending_records()

print_header("TC-10", "Valid Chain Passes Validation")
print("  Description: An unmodified chain should pass integrity checks")
print("  Expected: is_chain_valid() returns True")

valid = bc.is_chain_valid()
print(f"\n  Chain length : {len(bc.chain)}")
print(f"  Chain valid  : {valid}")

print_result(valid)


print_header("TC-11", "Tamper Detection — Data Modification")
print("  Description: Alter a block's patient data and check validation")
print("  Expected: is_chain_valid() returns False after tampering")

# Save original values
original_diagnosis = bc.chain[1].data[0]["diagnosis"]
original_hash = bc.chain[1].hash

print(f"\n  Original diagnosis : {original_diagnosis}")
print(f"  Original hash      : {original_hash[:40]}...")

# Tamper with the data
bc.chain[1].data[0]["diagnosis"] = "TAMPERED — False Diagnosis"
print(f"\n  Tampered diagnosis : {bc.chain[1].data[0]['diagnosis']}")
print(f"  Stored hash        : {bc.chain[1].hash[:40]}...")
print(f"  Recomputed hash    : {bc.chain[1].compute_hash()[:40]}...")
print(f"  Hashes match       : {bc.chain[1].hash == bc.chain[1].compute_hash()}")

tampered_valid = bc.is_chain_valid()
print(f"\n  Chain valid after tampering: {tampered_valid}")

print_result(not tampered_valid)

# Restore
bc.chain[1].data[0]["diagnosis"] = original_diagnosis
bc.chain[1].hash = original_hash


print_header("TC-12", "Tamper Detection — Broken Chain Link")
print("  Description: Modify a block's previous_hash to break the chain link")
print("  Expected: is_chain_valid() returns False")

original_prev = bc.chain[2].previous_hash

print(f"\n  Block #2 previous_hash : {bc.chain[2].previous_hash[:40]}...")
print(f"  Block #1 hash          : {bc.chain[1].hash[:40]}...")
print(f"  Match before tampering : {bc.chain[2].previous_hash == bc.chain[1].hash}")

# Break the link
bc.chain[2].previous_hash = "0000_BROKEN_LINK_FAKE_HASH"
print(f"\n  Tampered previous_hash : {bc.chain[2].previous_hash}")
print(f"  Match after tampering  : {bc.chain[2].previous_hash == bc.chain[1].hash}")

link_valid = bc.is_chain_valid()
print(f"  Chain valid            : {link_valid}")

print_result(not link_valid)

# Restore
bc.chain[2].previous_hash = original_prev


print_header("TC-13", "Tamper Detection — Recomputed Hash Without PoW")
print("  Description: Attacker tampers data AND recomputes hash, but")
print("               doesn't re-mine. This breaks the chain link to the")
print("               next block because the hash changes.")
print("  Expected: is_chain_valid() returns False")

print(f"\n  Block #1 original hash  : {bc.chain[1].hash[:40]}...")
print(f"  Block #2 previous_hash  : {bc.chain[2].previous_hash[:40]}...")

# Tamper and recompute (but don't re-mine)
bc.chain[1].data[0]["diagnosis"] = "SNEAKY TAMPER"
bc.chain[1].hash = bc.chain[1].compute_hash()

print(f"\n  Block #1 tampered hash  : {bc.chain[1].hash[:40]}...")
print(f"  Block #2 previous_hash  : {bc.chain[2].previous_hash[:40]}...")
print(f"  Link intact             : {bc.chain[1].hash == bc.chain[2].previous_hash}")
print(f"  New hash meets PoW      : {bc.chain[1].hash.startswith('0000')}")

sneaky_valid = bc.is_chain_valid()
print(f"  Chain valid             : {sneaky_valid}")

print_result(not sneaky_valid)

# Restore for consensus tests
bc.chain[1].data[0]["diagnosis"] = original_diagnosis
bc.chain[1].hash = original_hash


# CONSENSUS MECHANISM TESTS

print("\n" + "#" * 70)
print("  SECTION 5: CONSENSUS MECHANISM (LONGEST CHAIN RULE)")
print("#" * 70)

print_header("TC-14", "Shorter Chain Is Rejected")
print("  Description: A competing chain shorter than ours should be rejected")
print("  Expected: Chain not replaced, original retained")

shorter = Blockchain(difficulty=4)
# shorter has only genesis (1 block) vs our 3

print(f"\n  Our chain length       : {len(bc.chain)}")
print(f"  Competing chain length : {len(shorter.chain)}")

replaced = bc.resolve_conflicts([shorter.chain])
print(f"  Chain replaced         : {replaced}")
print(f"  Our chain length after : {len(bc.chain)}")

print_result(not replaced and len(bc.chain) == 3)


print_header("TC-15", "Equal Length Chain Is Rejected")
print("  Description: A competing chain of equal length should be rejected")
print("  Expected: Chain not replaced (tie goes to current chain)")

equal = Blockchain(difficulty=4)
equal.add_patient_record("X1", "Equal1", "Test", "Dr.")
equal.mine_pending_records()
equal.add_patient_record("X2", "Equal2", "Test", "Dr.")
equal.mine_pending_records()

print(f"\n  Our chain length       : {len(bc.chain)}")
print(f"  Competing chain length : {len(equal.chain)}")

replaced = bc.resolve_conflicts([equal.chain])
print(f"  Chain replaced         : {replaced}")

print_result(not replaced)


print_header("TC-16", "Longer Valid Chain Is Accepted")
print("  Description: A longer valid chain should replace ours")
print("  Expected: Chain replaced with the longer chain")

longer = Blockchain(difficulty=4)
for i in range(5):
    longer.add_patient_record(f"L{i}", f"Patient{i}", f"Cond{i}", "Dr. Z")
    longer.mine_pending_records()

our_len = len(bc.chain)
print(f"\n  Our chain length       : {our_len}")
print(f"  Competing chain length : {len(longer.chain)}")

replaced = bc.resolve_conflicts([longer.chain])
print(f"  Chain replaced         : {replaced}")
print(f"  New chain length       : {len(bc.chain)}")

print_result(replaced and len(bc.chain) == 6)


print_header("TC-17", "Longer INVALID Chain Is Rejected")
print("  Description: A longer chain that has been tampered with should")
print("               be rejected, even though it is longer")
print("  Expected: Chain not replaced")

# Reset bc to a known state
bc = Blockchain(difficulty=4)
bc.add_patient_record("P001", "Test", "Test", "Dr.")
bc.mine_pending_records()

# Create a longer but tampered chain
invalid_longer = Blockchain(difficulty=4)
for i in range(4):
    invalid_longer.add_patient_record(f"X{i}", f"P{i}", f"C{i}", "Dr.")
    invalid_longer.mine_pending_records()

# Tamper with it
invalid_longer.chain[2].data = [{"tampered": True}]

our_len = len(bc.chain)
print(f"\n  Our chain length            : {our_len}")
print(f"  Invalid competing length    : {len(invalid_longer.chain)}")
print(f"  Competing chain valid       : {invalid_longer.is_chain_valid()}")

replaced = bc.resolve_conflicts([invalid_longer.chain])
print(f"  Chain replaced              : {replaced}")
print(f"  Our chain length after      : {len(bc.chain)}")

print_result(not replaced and len(bc.chain) == our_len)


# EDGE CASES

print("\n" + "#" * 70)
print("  SECTION 6: EDGE CASES")
print("#" * 70)

print_header("TC-18", "Special Characters in Patient Data")
print("  Description: Patient data with unicode and special characters")
print("  Expected: Block mines and chain remains valid")

bc_edge = Blockchain(difficulty=2)  # Lower difficulty for speed
bc_edge.add_patient_record(
    "P100", "José García-López", "Ménière's disease", "Dr. Müller"
)
block = bc_edge.mine_pending_records()

print(f"\n  Patient name  : {block.data[0]['patient_name']}")
print(f"  Diagnosis     : {block.data[0]['diagnosis']}")
print(f"  Provider      : {block.data[0]['provider']}")
print(f"  Block mined   : {block is not None}")
print(f"  Chain valid   : {bc_edge.is_chain_valid()}")

print_result(block is not None and bc_edge.is_chain_valid())


print_header("TC-19", "Large Data Payload")
print("  Description: Mine a block with many records")
print("  Expected: Block mines successfully with all records intact")

bc_large = Blockchain(difficulty=2)
for i in range(10):
    bc_large.add_patient_record(
        f"P{i:03d}", f"Patient {i}", f"Condition {i}", f"Dr. {i}"
    )
block = bc_large.mine_pending_records()

print(f"\n  Records added  : 10")
print(f"  Records in block: {len(block.data)}")
print(f"  Chain valid    : {bc_large.is_chain_valid()}")

print_result(len(block.data) == 10 and bc_large.is_chain_valid())


print_header("TC-20", "Sequential Block Indices")
print("  Description: Block indices must be sequential (0, 1, 2, 3...)")
print("  Expected: Each block's index equals its position in the chain")

bc_seq = Blockchain(difficulty=2)
for i in range(4):
    bc_seq.add_patient_record(f"P{i}", f"Patient{i}", f"C{i}", "Dr.")
    bc_seq.mine_pending_records()

all_sequential = True
for i, block in enumerate(bc_seq.chain):
    match = block.index == i
    print(f"  Block position {i} → index {block.index} : "
          f"{'MATCH' if match else 'MISMATCH'}")
    if not match:
        all_sequential = False

print_result(all_sequential)


# SUMMARY

print("\n" + "=" * 70)
print("  TEST SUMMARY")
print("=" * 70)
print("""
  TC-01: Genesis Block Creation              — Tests blockchain initialisation
  TC-02: Block Structure Verification        — Tests required block fields
  TC-03: Hash Determinism                    — Tests SHA-256 consistency
  TC-04: Adding and Mining Records           — Tests core record workflow
  TC-05: Mining With No Pending Records      — Tests empty mine handling
  TC-06: Patient Record Retrieval            — Tests cross-block search
  TC-07: Hash Meets Difficulty               — Tests PoW hash validation
  TC-08: Proof-of-Work Computational Effort  — Tests nonce iteration
  TC-09: Different Difficulty Levels         — Tests scalable difficulty
  TC-10: Valid Chain Passes Validation       — Tests integrity baseline
  TC-11: Tamper Detection (Data)             — Tests data modification catch
  TC-12: Tamper Detection (Chain Link)       — Tests broken link catch
  TC-13: Tamper Detection (Recomputed Hash)  — Tests sophisticated attack
  TC-14: Shorter Chain Rejected              — Tests consensus rule
  TC-15: Equal Length Chain Rejected         — Tests tie-breaking
  TC-16: Longer Valid Chain Accepted         — Tests chain replacement
  TC-17: Longer Invalid Chain Rejected       — Tests validation + consensus
  TC-18: Special Characters                  — Tests unicode handling
  TC-19: Large Data Payload                  — Tests scalability
  TC-20: Sequential Block Indices            — Tests chain ordering

  Total: 20 test cases
""")
print("=" * 70)