CREATE DATABASE  IF NOT EXISTS `stomology-dep` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `stomology-dep`;
-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: stomology-dep
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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(30) DEFAULT NULL,
  `Password` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (101,'Admin','12345'),(102,'root','12345');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `SSN` int NOT NULL,
  `FName` varchar(20) DEFAULT NULL,
  `MidName` varchar(20) DEFAULT NULL,
  `LName` varchar(20) DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `Gender` varchar(20) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL,
  `UserID` int NOT NULL,
  `DoctorID` int NOT NULL,
  `ServiceID` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `UserID` (`UserID`),
  KEY `DoctorID` (`DoctorID`),
  KEY `ServiceID` (`ServiceID`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`id`),
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`DoctorID`) REFERENCES `doctors` (`id`),
  CONSTRAINT `appointments_ibfk_3` FOREIGN KEY (`ServiceID`) REFERENCES `treatments` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (3,528976329,'Youssef','Ahmed','Farag',34,'Male',NULL,'waiting',1,1,1),(4,159648216,'Ali','Ahmed','Zaid',43,'Male',NULL,'Refused',1,1,2),(5,898777900,'Ismael','Tawfik','Ziad',20,'Male','2022-01-28','Scheduled',2,1,1),(6,94327532,'Ali','Khalid','Mohamed',32,'Male','2022-01-30','Scheduled',1,1,2),(7,3213341,'sara','Ahmed','Ahmed',32,'Female','2022-01-13','Scheduled',1,1,2),(8,144232222,'Sara','Ahmed','Farag',43,'Female','2022-01-11','Refused',1,2,2);
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `SSN` int NOT NULL,
  `FName` varchar(20) DEFAULT NULL,
  `MidName` varchar(20) DEFAULT NULL,
  `LName` varchar(20) DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Degree` varchar(50) DEFAULT NULL,
  `Password` varchar(10) DEFAULT NULL,
  `Image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,222303979,'Ahmed','Abdullah','Mahmoud',42,'Male','13136429440','ahmed.abdullah@gmail.com','Doctor of Dental Medicine (DMD)','547099615','static/img/doctorsProfile/AhmedAbdullah.jpg'),(2,7532758,'Ziad','Ahmed','Mahmoud',63,'Male','323432523','ziad.abdullah92@gmail.com','Doctor of Dental Medicine (DMD)','080416919','');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rates`
--

DROP TABLE IF EXISTS `rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rates` (
  `Rating` int DEFAULT NULL,
  `Review` varchar(500) DEFAULT NULL,
  `UserID` int DEFAULT NULL,
  KEY `UserID` (`UserID`),
  CONSTRAINT `rates_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rates`
--

LOCK TABLES `rates` WRITE;
/*!40000 ALTER TABLE `rates` DISABLE KEYS */;
INSERT INTO `rates` VALUES (4,'The staff is wonderful. I have dental anxiety and the staff made me feel very comfortable. I was numbed VERY well ♥️ My procedure was professional and efficient. Thank you and you\'re greatly appreciated.',1),(5,'Thanks for this experience, I am very happy that i went to the dental and met the kind dentists.',2),(4,'Thank you, I am very happy with this experience, I hope to try again.\r\nI expect more from you in the upcoming appointments. Thanks to the doctors, thanks to all the workers and I advise everyone to go to this clinic.',1);
/*!40000 ALTER TABLE `rates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `site_information`
--

DROP TABLE IF EXISTS `site_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `site_information` (
  `Title` varchar(100) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Short_description` varchar(500) DEFAULT NULL,
  `Long_description` varchar(1000) DEFAULT NULL,
  `Icon` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_information`
--

LOCK TABLES `site_information` WRITE;
/*!40000 ALTER TABLE `site_information` DISABLE KEYS */;
INSERT INTO `site_information` VALUES ('Dental Health','Al sharqiya, El Zagazeeg','mohamed.ahmedfrg.2002@gmail.com','+201140345493','Every tooth in a man\'s head is more valuable than a diamond.','We are a group of energetic, skilled, and empathetic dental professionals who care about what’s important to you — achieving a beautiful, healthy smile for life. \r\nCombining state-of-the-art dental technology and procedures with a friendly, attentive environment, we provide a patient experience unmatched in Midtown Atlanta and Roswell. <br>\r\n<br>\r\nEvery detail of your appointment is crafted to ensure you feel at home. Enjoy our bright, lively, and comfortable office while we work hard to make your appointment effortless. <br>\r\n<br>\r\n<h5>Our Story</h5>\r\n<br>\r\nAt Our Dental, we help you celebrate the joy of a happy, healthy smile.\r\n<br><br>\r\nWe started in 2010 with the goal of reimagining the dental experience. We believe going to the dentist should be positive and empowering for the whole family, and we’re doing our part to make that the new reality. Our office provides cutting-edge techniques, an experienced team, and a whole lot of time spent making sure you feel comfortable.','static/img/icon/icon.png');
/*!40000 ALTER TABLE `site_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `slider`
--

DROP TABLE IF EXISTS `slider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `slider` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Image` varchar(500) DEFAULT NULL,
  `Title` varchar(500) DEFAULT NULL,
  `Description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `slider`
--

LOCK TABLES `slider` WRITE;
/*!40000 ALTER TABLE `slider` DISABLE KEYS */;
INSERT INTO `slider` VALUES (1,'static/img/slider/img.jpg','Your great smile begins with a great dentist',''),(2,'static/img/slider/img2.jpg','\"The best experience I\'ve ever had at my kids\' dentist.\" ','We happily treat patients of just about any age. Whether you are looking for a new family dentist, or just have an emergency tooth ache, we will treat you with respect and address your concerns promptly with affordable treatment options.'),(3,'static/img/slider/dental_insurance_coverage_and_cost_getty_creative.jpeg','Dental Health clinic','Board Certified in Periodontology and Dental Implant Surgery.');
/*!40000 ALTER TABLE `slider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treatments`
--

DROP TABLE IF EXISTS `treatments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treatments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Image` varchar(100) DEFAULT NULL,
  `Name` varchar(200) DEFAULT NULL,
  `cost` int DEFAULT NULL,
  `Duration` int DEFAULT NULL,
  `Description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treatments`
--

LOCK TABLES `treatments` WRITE;
/*!40000 ALTER TABLE `treatments` DISABLE KEYS */;
INSERT INTO `treatments` VALUES (1,'static/img/ServicesProfile/image.jpg','Restorative dentistry',320,3,'Restorative dentistry is a branch of dentistry that focuses on replacing damaged or missing teeth.'),(2,'static/img/ServicesProfile/image2.jpg','Smile make overs',340,6,'Smiling with confidence makes you feel great. A beautiful smile is also an important social and professional asset.\r\n                    ');
/*!40000 ALTER TABLE `treatments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `FName` varchar(20) DEFAULT NULL,
  `MidName` varchar(20) DEFAULT NULL,
  `LName` varchar(20) DEFAULT NULL,
  `Image` varchar(100) DEFAULT NULL,
  `UserName` varchar(30) DEFAULT NULL,
  `Password` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Mohamed Ahmed','Abdullah','Mahmoud','static/img/UsersProfile/me.jpg','moern','01140345493','mohamed.ahmedfrg.2002@gmail.com','+201140345493'),(2,'Ismael','Tawfik','Ziad','static/img/UsersProfile/WhatsApp_Image_2022-01-07_at_2.32.31_PM.jpeg','som3a','123456','Ismael.Tawfik@gmail.com','+11588287281');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-10 15:37:45
