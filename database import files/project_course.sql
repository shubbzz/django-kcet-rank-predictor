-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `course_name` varchar(255) NOT NULL,
  `course_id` varchar(255) NOT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES ('Artificial\nIntel, Data Sc','AD '),('Aeronaut.Engg','AE '),('Artificial\nIntelligence','AI '),('Automotive\nEngg.','AT '),('Automobile','AU '),('Computer Tech.','BC '),('CS- Big Data','BD '),('Bio-Electronics\nEngg.','BE '),('Information\nTech.','BI '),('Bio Medical','BM '),('Bio Technology','BT '),('Comp. Sc. and\nBus Sys.','CB '),('Computer and\nComm. Engg.','CC '),('Civil','CE '),('Chemical','CH '),('Computer and\nInformation','CI '),('Computer\nEngineering','CO '),('Ceramics','CR '),('Computers','CS '),('Const. Tech.\nMgmt.','CT '),('CS- Cyber\nSecurity','CY '),('Comp. Sc. Engg-\nData Sc.','DS '),('Electronics','EC '),('Electrical','EE '),('Elec. Inst.\nEngg','EI '),('Environmental','EN '),('Electrical and\nComputer','ER '),('Electronics and\nComputer','ES '),('Elec.\nTelecommn.','ET '),('IoT, Cyber\nSecurity','IC '),('Info.Science','IE '),('EC -Industrial\nIntegrated','II '),('Ind. Engg.\nMgmt.','IM '),('CS- Internet of\nThings','IO '),('Ind.Prodn.','IP '),('Inst.Tech.','IT '),('CS- Block Chain','LC '),('Mathamatics and\nComputing','MC '),('Med.Elect.','MD '),('Mechanical','ME '),('Mechanical,\nSmart Manf.','MM '),('Marine\nEngineering','MR '),('Mechatronics','MT '),('Comp. Sc. Engg-\nDev Ops','OP '),('Petroleum\nEngineering','PL '),('Polymer Tech.','PT '),('Auto. And\nRobot.','RO '),('Aero Space\nEngg.','SE '),('CS and System\nEngg','SS '),('Silk Tech.','ST '),('Telecommn.','TC '),('Textiles','TX '),('Planning','UP ');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-14 12:05:35
