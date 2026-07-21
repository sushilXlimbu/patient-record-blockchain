// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;


contract PatientRecordContract {

    // ─────────────────────────────────────────────────────────────────
    // STATE VARIABLES
    // ─────────────────────────────────────────────────────────────────

    /// Total number of patient records ever added.
    uint256 public totalRecords;

    /// Address of the contract owner (hospital administrator).
    address public owner;

    struct PatientRecord {
        string  patientId;
        string  name;
        string  diagnosis;
        address provider;
        uint256 timestamp;
        bool    isActive;
    }
    mapping(address => bool) public authorizedProviders;

    mapping(string => PatientRecord) private records;

    // ─────────────────────────────────────────────────────────────────
    // EVENTS
    // ─────────────────────────────────────────────────────────────────

    event RecordAdded(
        string  indexed patientId,
        address indexed provider,
        uint256         timestamp
    );

    event RecordTransferred(
        string  indexed patientId,
        address indexed fromProvider,
        address indexed toProvider
    );

    /// Emitted when a provider is added to the whitelist.
    event ProviderAuthorized(address indexed provider);

    /// Emitted when a provider is removed from the whitelist.
    event ProviderRevoked(address indexed provider);

    // ─────────────────────────────────────────────────────────────────
    // MODIFIERS
    // ─────────────────────────────────────────────────────────────────

    modifier onlyOwner() {
        require(msg.sender == owner, "PatientRecordContract: caller is not owner");
        _;
    }

    modifier onlyAuthorized() {
        require(
            authorizedProviders[msg.sender],
            "PatientRecordContract: caller is not an authorized provider"
        );
        _;
    }

    modifier recordExists(string memory patientId) {
        require(
            records[patientId].isActive,
            "PatientRecordContract: record does not exist or is inactive"
        );
        _;
    }

    // ─────────────────────────────────────────────────────────────────
    // CONSTRUCTOR
    // ─────────────────────────────────────────────────────────────────

    constructor() {
        owner = msg.sender;
        authorizedProviders[msg.sender] = true;
        totalRecords = 0;
        emit ProviderAuthorized(msg.sender);
    }

    // ─────────────────────────────────────────────────────────────────
    // OWNER FUNCTIONS
    // ─────────────────────────────────────────────────────────────────

    function authorizeProvider(address providerAddress) external onlyOwner {
        require(
            providerAddress != address(0),
            "PatientRecordContract: zero address not allowed"
        );
        authorizedProviders[providerAddress] = true;
        emit ProviderAuthorized(providerAddress);
    }

    function revokeProvider(address providerAddress) external onlyOwner {
        authorizedProviders[providerAddress] = false;
        emit ProviderRevoked(providerAddress);
    }

    // ─────────────────────────────────────────────────────────────────
    // CORE FUNCTIONS
    // ─────────────────────────────────────────────────────────────────

    function addRecord(
        string memory patientId,
        string memory name,
        string memory diagnosis
    ) external onlyAuthorized {
        // Prevent duplicate records
        require(
            !records[patientId].isActive,
            "PatientRecordContract: record already exists for this patient"
        );

        // Write the new record to storage
        records[patientId] = PatientRecord({
            patientId : patientId,
            name      : name,
            diagnosis : diagnosis,
            provider  : msg.sender,
            timestamp : block.timestamp,
            isActive  : true
        });

        totalRecords++;

        emit RecordAdded(patientId, msg.sender, block.timestamp);
    }

    function transferRecord(
        string memory patientId,
        address newProvider
    ) external onlyAuthorized recordExists(patientId) {
        PatientRecord storage rec = records[patientId];

        // Only the current record holder can initiate the transfer
        require(
            rec.provider == msg.sender,
            "PatientRecordContract: only the current record holder can transfer"
        );

        // Receiving address must be a whitelisted provider
        require(
            authorizedProviders[newProvider],
            "PatientRecordContract: new provider is not authorized"
        );

        address previous = rec.provider;
        rec.provider = newProvider;

        emit RecordTransferred(patientId, previous, newProvider);
    }

    // ─────────────────────────────────────────────────────────────────
    // VIEW / QUERY FUNCTIONS
    // ─────────────────────────────────────────────────────────────────

    function getRecord(string memory patientId)
        external
        view
        onlyAuthorized
        recordExists(patientId)
        returns (PatientRecord memory)
    {
        return records[patientId];
    }

    function isAuthorized(address providerAddress) external view returns (bool) {
        return authorizedProviders[providerAddress];
    }

    function deactivateRecord(string memory patientId)
        external
        onlyOwner
        recordExists(patientId)
    {
        records[patientId].isActive = false;
    }
}
