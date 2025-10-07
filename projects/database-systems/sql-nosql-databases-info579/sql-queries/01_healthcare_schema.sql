-- Healthcare Database Schema Creation Script
-- INFO 579 - SQL & NoSQL Databases
-- Creating normalized healthcare database structure

-- Drop existing tables if they exist
DROP TABLE IF EXISTS conditions;
DROP TABLE IF EXISTS encounters;
DROP TABLE IF EXISTS observations;
DROP TABLE IF EXISTS procedures;
DROP TABLE IF EXISTS providers;
DROP TABLE IF EXISTS patients;

-- Create Patients table
CREATE TABLE patients (
    id VARCHAR(36) PRIMARY KEY,
    birthdate DATE,
    deathdate DATE,
    ssn VARCHAR(11),
    drivers VARCHAR(10),
    passport VARCHAR(10),
    prefix VARCHAR(10),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    suffix VARCHAR(10),
    maiden VARCHAR(50),
    marital VARCHAR(1),
    race VARCHAR(20),
    ethnicity VARCHAR(20),
    gender VARCHAR(1),
    birthplace VARCHAR(100),
    address VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    county VARCHAR(50),
    zip VARCHAR(10),
    lat DECIMAL(10, 8),
    lon DECIMAL(11, 8),
    healthcare_expenses DECIMAL(12, 2),
    healthcare_coverage DECIMAL(12, 2)
);

-- Create Providers table
CREATE TABLE providers (
    id VARCHAR(36) PRIMARY KEY,
    organization VARCHAR(100),
    name VARCHAR(100),
    gender VARCHAR(1),
    specialty VARCHAR(50),
    address VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    zip VARCHAR(10),
    lat DECIMAL(10, 8),
    lon DECIMAL(11, 8),
    phone VARCHAR(20),
    utilization INTEGER
);

-- Create Encounters table
CREATE TABLE encounters (
    id VARCHAR(36) PRIMARY KEY,
    start_date DATETIME,
    stop_date DATETIME,
    patient_id VARCHAR(36),
    organization VARCHAR(36),
    provider VARCHAR(36),
    payer VARCHAR(36),
    encounter_class VARCHAR(20),
    code VARCHAR(20),
    description VARCHAR(200),
    base_encounter_cost DECIMAL(12, 2),
    total_claim_cost DECIMAL(12, 2),
    payer_coverage DECIMAL(12, 2),
    reason_code VARCHAR(20),
    reason_description VARCHAR(200),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- Create Conditions table
CREATE TABLE conditions (
    start_date DATE,
    stop_date DATE,
    patient_id VARCHAR(36),
    encounter_id VARCHAR(36),
    code VARCHAR(20),
    description VARCHAR(200),
    PRIMARY KEY (patient_id, encounter_id, code),
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(id)
);

-- Create Procedures table
CREATE TABLE procedures (
    start_date DATETIME,
    stop_date DATETIME,
    patient_id VARCHAR(36),
    encounter_id VARCHAR(36),
    code VARCHAR(20),
    description VARCHAR(200),
    base_cost DECIMAL(12, 2),
    PRIMARY KEY (patient_id, encounter_id, code),
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(id)
);

-- Create Observations table
CREATE TABLE observations (
    date_time DATETIME,
    patient_id VARCHAR(36),
    encounter_id VARCHAR(36),
    category VARCHAR(50),
    code VARCHAR(20),
    description VARCHAR(200),
    value DECIMAL(10, 3),
    units VARCHAR(20),
    type VARCHAR(20),
    PRIMARY KEY (patient_id, encounter_id, code, date_time),
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(id)
);

-- Create indexes for better query performance
CREATE INDEX idx_patient_birth ON patients(birthdate);
CREATE INDEX idx_patient_state ON patients(state);
CREATE INDEX idx_patient_gender ON patients(gender);
CREATE INDEX idx_condition_code ON conditions(code);
CREATE INDEX idx_condition_patient ON conditions(patient_id);
CREATE INDEX idx_encounter_date ON encounters(start_date);
CREATE INDEX idx_encounter_patient ON encounters(patient_id);

-- Add comments for documentation
COMMENT ON TABLE patients IS 'Patient demographic and contact information';
COMMENT ON TABLE providers IS 'Healthcare providers and organizations';
COMMENT ON TABLE encounters IS 'Medical visits and appointments';
COMMENT ON TABLE conditions IS 'Medical diagnoses and conditions';
COMMENT ON TABLE procedures IS 'Medical procedures and treatments';
COMMENT ON TABLE observations IS 'Clinical measurements and test results';