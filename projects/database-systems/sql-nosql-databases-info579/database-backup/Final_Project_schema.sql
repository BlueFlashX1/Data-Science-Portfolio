-- MySQL dump 10.13  Distrib 8.0.36, for Linux (aarch64)
--
-- Host: localhost    Database: Final_Project
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `diagnosis`
--

DROP TABLE IF EXISTS `diagnosis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diagnosis` (
  `patient_id` varchar(36) NOT NULL,
  `condition_id` bigint NOT NULL,
  PRIMARY KEY (`patient_id`,`condition_id`),
  KEY `condition_id` (`condition_id`),
  CONSTRAINT `diagnosis_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `diagnosis_ibfk_2` FOREIGN KEY (`condition_id`) REFERENCES `medical_condition` (`condition_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `encounter`
--

DROP TABLE IF EXISTS `encounter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `encounter` (
  `encounter_id` varchar(36) NOT NULL,
  `patient_id` varchar(36) NOT NULL,
  `provider_id` varchar(36) DEFAULT NULL,
  `organization_id` varchar(36) DEFAULT NULL,
  `encounter_start_date` datetime NOT NULL,
  `encounter_end_date` datetime DEFAULT NULL,
  `payer_uuid` varchar(36) DEFAULT NULL,
  `encounter_class` varchar(50) NOT NULL,
  `encounter_code` varchar(36) NOT NULL,
  `encounter_description` varchar(255) NOT NULL,
  `base_encounter_cost` decimal(12,2) NOT NULL,
  `total_claim_cost` decimal(12,2) NOT NULL,
  `payer_coverage` decimal(12,2) NOT NULL,
  `encounter_reason_code` varchar(36) DEFAULT NULL,
  `encounter_reason_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`encounter_id`),
  KEY `fk_encounter_patient` (`patient_id`),
  KEY `fk_encounter_provider_org` (`provider_id`,`organization_id`),
  CONSTRAINT `fk_encounter_patient` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_encounter_provider_org` FOREIGN KEY (`provider_id`, `organization_id`) REFERENCES `provider` (`provider_id`, `organization_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `medical_condition`
--

DROP TABLE IF EXISTS `medical_condition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_condition` (
  `condition_id` bigint NOT NULL AUTO_INCREMENT,
  `condition_start_date` date NOT NULL,
  `condition_end_date` date DEFAULT NULL,
  `patient_id` varchar(36) NOT NULL,
  `encounter_id` varchar(36) DEFAULT NULL,
  `condition_code` varchar(36) NOT NULL,
  `condition_description` varchar(255) NOT NULL,
  PRIMARY KEY (`condition_id`),
  KEY `patient_id` (`patient_id`),
  KEY `encounter_id` (`encounter_id`),
  CONSTRAINT `medical_condition_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `medical_condition_ibfk_2` FOREIGN KEY (`encounter_id`) REFERENCES `encounter` (`encounter_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8377 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `observation`
--

DROP TABLE IF EXISTS `observation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `observation` (
  `observation_id` bigint NOT NULL AUTO_INCREMENT,
  `observation_date` datetime NOT NULL,
  `patient_id` varchar(36) NOT NULL,
  `encounter_id` varchar(36) DEFAULT NULL,
  `observation_code` varchar(36) NOT NULL,
  `observation_desc` varchar(255) NOT NULL,
  `observation_value` varchar(255) DEFAULT NULL,
  `observation_units` varchar(50) DEFAULT NULL,
  `observation_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`observation_id`),
  KEY `patient_id` (`patient_id`),
  KEY `encounter_id` (`encounter_id`),
  CONSTRAINT `observation_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `observation_ibfk_2` FOREIGN KEY (`encounter_id`) REFERENCES `encounter` (`encounter_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=299698 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `patient_id` varchar(36) NOT NULL,
  `birth_date` date NOT NULL,
  `death_date` date DEFAULT NULL,
  `ssn` varchar(11) NOT NULL,
  `driver_license_number` varchar(10) DEFAULT NULL,
  `passport_number` varchar(10) DEFAULT NULL,
  `prefix` varchar(5) DEFAULT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `suffix` varchar(3) DEFAULT NULL,
  `maiden_name` varchar(20) DEFAULT NULL,
  `marital_status` varchar(3) DEFAULT NULL,
  `patient_race` varchar(10) NOT NULL,
  `patient_ethnicity` varchar(15) NOT NULL,
  `patient_gender` varchar(1) NOT NULL,
  `birth_place` varchar(100) NOT NULL,
  `patient_address` varchar(100) NOT NULL,
  `patient_city` varchar(30) NOT NULL,
  `patient_state` varchar(20) NOT NULL,
  `patient_county` varchar(30) NOT NULL,
  `patient_zip_code` varchar(10) DEFAULT NULL,
  `patient_latitude` decimal(9,6) NOT NULL,
  `patient_longitude` decimal(9,6) NOT NULL,
  `healthcare_expenses` decimal(12,2) NOT NULL,
  `healthcare_coverage` decimal(12,2) NOT NULL,
  PRIMARY KEY (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `procedures`
--

DROP TABLE IF EXISTS `procedures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `procedures` (
  `procedure_id` bigint NOT NULL AUTO_INCREMENT,
  `procedure_date` datetime NOT NULL,
  `patient_id` varchar(36) NOT NULL,
  `encounter_id` varchar(36) DEFAULT NULL,
  `procedure_code` varchar(36) NOT NULL,
  `procedure_description` varchar(255) NOT NULL,
  `procedure_base_cost` decimal(12,2) NOT NULL,
  `procedure_reason_code` varchar(36) DEFAULT NULL,
  `procedure_reason_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`procedure_id`),
  KEY `patient_id` (`patient_id`),
  KEY `encounter_id` (`encounter_id`),
  CONSTRAINT `procedures_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `procedures_ibfk_2` FOREIGN KEY (`encounter_id`) REFERENCES `encounter` (`encounter_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34982 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `provider`
--

DROP TABLE IF EXISTS `provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `provider` (
  `provider_id` varchar(36) NOT NULL,
  `organization_id` varchar(36) NOT NULL,
  `provider_name` varchar(30) NOT NULL,
  `provider_gender` varchar(1) NOT NULL,
  `provider_specialty` varchar(50) NOT NULL,
  `provider_address` varchar(100) NOT NULL,
  `provider_city` varchar(30) NOT NULL,
  `provider_state` varchar(20) NOT NULL,
  `provider_zip_code` varchar(10) NOT NULL,
  `provider_latitude` decimal(9,6) NOT NULL,
  `provider_longitude` decimal(9,6) NOT NULL,
  `utilization` int NOT NULL,
  PRIMARY KEY (`provider_id`),
  UNIQUE KEY `uq_provider_org` (`provider_id`,`organization_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_condition_prevalence`
--

DROP TABLE IF EXISTS `rpt_condition_prevalence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_condition_prevalence` (
  `condition_code` varchar(36) NOT NULL,
  `condition_description` varchar(255) NOT NULL,
  `n_patients` bigint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_diagnosis_patient_condition`
--

DROP TABLE IF EXISTS `rpt_diagnosis_patient_condition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_diagnosis_patient_condition` (
  `patient_id` varchar(36) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `condition_id` bigint NOT NULL DEFAULT '0',
  `condition_code` varchar(36) NOT NULL,
  `condition_description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_encounter_activity`
--

DROP TABLE IF EXISTS `rpt_encounter_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_encounter_activity` (
  `encounter_id` varchar(36) NOT NULL,
  `patient_id` varchar(36) NOT NULL,
  `encounter_start_date` datetime NOT NULL,
  `encounter_class` varchar(50) NOT NULL,
  `provider_id` varchar(36),
  `organization_id` varchar(36),
  `provider_name` varchar(30),
  `n_procedures` bigint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_er_frequenters`
--

DROP TABLE IF EXISTS `rpt_er_frequenters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_er_frequenters` (
  `patient_id` varchar(36) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `er_visits` bigint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_followup_14d_by_proc_code`
--

DROP TABLE IF EXISTS `rpt_followup_14d_by_proc_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_followup_14d_by_proc_code` (
  `procedure_code` varchar(36) NOT NULL,
  `procedure_description` varchar(255) NOT NULL,
  `n_procedures` bigint NOT NULL DEFAULT '0',
  `n_with_followup_14d` decimal(32,0) DEFAULT NULL,
  `pct_with_followup_14d` decimal(38,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_inactive_providers_by_specialty`
--

DROP TABLE IF EXISTS `rpt_inactive_providers_by_specialty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_inactive_providers_by_specialty` (
  `provider_specialty` varchar(50) NOT NULL,
  `n_inactive_providers` bigint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_inner_encounter_provider`
--

DROP TABLE IF EXISTS `rpt_inner_encounter_provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_inner_encounter_provider` (
  `encounter_id` varchar(36) NOT NULL,
  `patient_id` varchar(36) NOT NULL,
  `provider_id` varchar(36) DEFAULT NULL,
  `organization_id` varchar(36) DEFAULT NULL,
  `provider_name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_inpatient_los_provider`
--

DROP TABLE IF EXISTS `rpt_inpatient_los_provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_inpatient_los_provider` (
  `provider_id` varchar(36) NOT NULL,
  `organization_id` varchar(36) NOT NULL,
  `provider_name` varchar(30) NOT NULL,
  `avg_los_days` decimal(23,2) DEFAULT NULL,
  `n_inpatient_encounters` bigint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_proc_readmit_30d`
--

DROP TABLE IF EXISTS `rpt_proc_readmit_30d`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_proc_readmit_30d` (
  `procedure_code` varchar(36) NOT NULL,
  `procedure_description` varchar(255) NOT NULL,
  `n_procedures` bigint NOT NULL DEFAULT '0',
  `n_with_revisit_30d` decimal(32,0) DEFAULT NULL,
  `pct_with_revisit_30d` decimal(38,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_procedure_costs`
--

DROP TABLE IF EXISTS `rpt_procedure_costs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_procedure_costs` (
  `procedure_code` varchar(36) NOT NULL,
  `procedure_description` varchar(255) NOT NULL,
  `n_procedures` bigint NOT NULL DEFAULT '0',
  `avg_base_cost` decimal(13,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_provider_readmit_30d`
--

DROP TABLE IF EXISTS `rpt_provider_readmit_30d`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_provider_readmit_30d` (
  `provider_id` varchar(36) NOT NULL,
  `organization_id` varchar(36) NOT NULL,
  `provider_name` varchar(30) NOT NULL,
  `n_revisits_30d` decimal(23,0) DEFAULT NULL,
  `n_index_encounters` bigint NOT NULL DEFAULT '0',
  `pct_revisit_30d` decimal(29,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_provider_utilization`
--

DROP TABLE IF EXISTS `rpt_provider_utilization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_provider_utilization` (
  `provider_id` varchar(36) NOT NULL,
  `organization_id` varchar(36) NOT NULL,
  `provider_name` varchar(30) NOT NULL,
  `provider_specialty` varchar(50) NOT NULL,
  `n_encounters` bigint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_providers_highrisk_er`
--

DROP TABLE IF EXISTS `rpt_providers_highrisk_er`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_providers_highrisk_er` (
  `provider_id` varchar(36) NOT NULL,
  `organization_id` varchar(36) NOT NULL,
  `provider_name` varchar(30) NOT NULL,
  `provider_specialty` varchar(50) NOT NULL,
  `n_highrisk_patients` bigint NOT NULL DEFAULT '0',
  `n_highrisk_encounters` bigint NOT NULL DEFAULT '0',
  `total_encounters` bigint NOT NULL DEFAULT '0',
  `pct_of_provider_encounters` decimal(26,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpt_readmissions_30d`
--

DROP TABLE IF EXISTS `rpt_readmissions_30d`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rpt_readmissions_30d` (
  `patient_id` varchar(36) NOT NULL,
  `encounter_id` varchar(36) NOT NULL,
  `encounter_start_date` datetime NOT NULL,
  `prev_start` datetime DEFAULT NULL,
  `days_since_prior` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `treatment`
--

DROP TABLE IF EXISTS `treatment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treatment` (
  `patient_id` varchar(36) NOT NULL,
  `procedure_id` bigint NOT NULL,
  PRIMARY KEY (`patient_id`,`procedure_id`),
  KEY `procedure_id` (`procedure_id`),
  CONSTRAINT `treatment_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `treatment_ibfk_2` FOREIGN KEY (`procedure_id`) REFERENCES `procedures` (`procedure_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'Final_Project'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-07  5:33:40
