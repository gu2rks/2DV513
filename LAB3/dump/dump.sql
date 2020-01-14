-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Host: 127.0.0.1    Database: Library
-- ------------------------------------------------------
-- Server version	8.0.18

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
-- Table structure for table `Book`
--

DROP TABLE IF EXISTS `Book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Book` (
  `bkID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `author` varchar(45) NOT NULL,
  `edition` int(11) NOT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`bkID`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book`
--

LOCK TABLES `Book` WRITE;
/*!40000 ALTER TABLE `Book` DISABLE KEYS */;
INSERT INTO `Book` VALUES (1,'The Way of Kings','Brandon Sanderson',1,'Fantasy'),(2,'The Eye of the World ','Robert Jordan',1,'Fantasy'),(3,'His Dark Materials','Philip Pullman',2,'Fantasy'),(4,'Brave New World','Aldous Huxley',2,'Science fiction'),(5,'A Wrinkle in Time (Time Qui...','Madeleine L\'Engle',1,'ETC'),(7,'The Hunger Games ','Suzanne Collins',1,'Science fiction'),(8,' Throne of Glass (Throne of ...','Throne of GlassSarah J. Maas ',1,'Romance'),(9,'The Goose Girl','Shannon Hale',2,'Romance'),(10,'Stardust','Neil Gaiman [D[D',1,'Romance'),(11,'Drama City','George Pelecanos',1,'Drama'),(12,' Tales of a Drama Queen','Lee Nichols',1,'Drama'),(13,'Baby Momma Drama','Carl Weber ',1,'Drama'),(14,'The shining','Stephen King',3,'Horror'),(15,'IT','Stephen King',3,'Horror'),(16,'The giving tree','Shel Silverstein',1,'Children'),(17,'The cat in the hat','Dr. Seuss',2,'Children'),(18,'The Wicked King','Holly Black, Kathleen Jennings',1,'Fantasy'),(19,'The Institute','Stephen King',1,'Horror'),(20,'The Girl In Red','Christina Henry',1,'Horror'),(21,'A Beautiful Day In The Neighborhood','Fred Rogers',1,'Children');
/*!40000 ALTER TABLE `Book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `bookstock`
--

DROP TABLE IF EXISTS `bookstock`;
/*!50001 DROP VIEW IF EXISTS `bookstock`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `bookstock` AS SELECT 
 1 AS `bkID`,
 1 AS `name`,
 1 AS `author`,
 1 AS `edition`,
 1 AS `type`,
 1 AS `stockID`,
 1 AS `book_id`,
 1 AS `amount`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `LoanDetails`
--

DROP TABLE IF EXISTS `LoanDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LoanDetails` (
  `book_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `expireDate` date NOT NULL,
  KEY `member_id` (`member_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `book_id` FOREIGN KEY (`book_id`) REFERENCES `book` (`bkID`),
  CONSTRAINT `member_id` FOREIGN KEY (`member_id`) REFERENCES `member` (`memID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LoanDetails`
--

LOCK TABLES `LoanDetails` WRITE;
/*!40000 ALTER TABLE `LoanDetails` DISABLE KEYS */;
INSERT INTO `LoanDetails` VALUES (1,2,'2020-01-14','2020-02-04'),(3,2,'2020-01-14','2020-02-04'),(10,2,'2020-01-14','2020-02-04'),(11,1,'2020-01-14','2020-02-04'),(12,1,'2020-01-14','2020-02-04'),(10,3,'2020-01-14','2020-02-04'),(9,3,'2020-01-14','2020-02-04'),(19,4,'2020-01-14','2020-02-04'),(21,5,'2020-01-14','2020-02-04'),(20,6,'2020-01-14','2020-02-04'),(15,7,'2020-01-14','2020-02-04'),(17,9,'2020-01-14','2020-02-04');
/*!40000 ALTER TABLE `LoanDetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Member`
--

DROP TABLE IF EXISTS `Member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Member` (
  `memID` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(45) NOT NULL,
  `lastName` varchar(45) NOT NULL,
  `gender` varchar(45) NOT NULL,
  `address` varchar(45) NOT NULL,
  `personalNum` varchar(45) NOT NULL,
  PRIMARY KEY (`memID`),
  UNIQUE KEY `id_UNIQUE` (`memID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Member`
--

LOCK TABLES `Member` WRITE;
/*!40000 ALTER TABLE `Member` DISABLE KEYS */;
INSERT INTO `Member` VALUES (1,'Amata','A.','male','idrottgatan 5','9402015432'),(2,'Fartun','A.','female','idrottgatan 5','9408215237'),(3,'Ebtisam','Mohana','female','swedland 12','12219832'),(4,'Irene','Koech','female','Paradise 1','8704280941'),(5,'Ramine','Rastafah','male','Zion 9','9006215679'),(6,'Moajat','Mohamnadi','male','Kungsgatan 3','9610308932'),(7,'Yemi','Rastafah','male','Zion 10','9201227346'),(8,'Alberto','Sinor','male','Spainor 22','2186483'),(9,'Ola','Flyg','male','Sleepyland 12','6805228592'),(10,'Marcus','Mueller','male','Zion 1','8707160473'),(11,'Maya','Andersson','female','Kalmar 23','9810083297'),(12,'Roin','Valizada','male','Vimmerby 8','9706017321'),(13,'Emil','Nycz','male','Vimmerby 26','9402217921'),(14,'Kual','maboy','male','Vimmerby 13','8501303012'),(15,'Felix','Haberhiwe','female','Vimmerby 14','9311309210'),(16,'Assa','Tu','female','Vimmerby 15','9605061232'),(17,'Felicia','Cutie','female','Hell 1.0','2102189321'),(18,'Felix','Kust','male','German 5','9610180236');
/*!40000 ALTER TABLE `Member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Stock`
--

DROP TABLE IF EXISTS `Stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Stock` (
  `stockID` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  PRIMARY KEY (`stockID`),
  KEY `Sbook_id` (`book_id`),
  CONSTRAINT `Sbook_id` FOREIGN KEY (`book_id`) REFERENCES `book` (`bkID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Stock`
--

LOCK TABLES `Stock` WRITE;
/*!40000 ALTER TABLE `Stock` DISABLE KEYS */;
INSERT INTO `Stock` VALUES (1,1,4),(2,2,4),(3,3,3),(4,4,3),(5,5,3),(7,7,2),(8,8,4),(9,9,2),(10,10,0),(11,11,1),(12,12,2),(13,13,3),(14,14,1),(15,15,3),(16,16,2),(17,17,2),(18,18,2),(19,19,0),(20,20,1),(21,21,3);
/*!40000 ALTER TABLE `Stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `bookstock`
--

/*!50001 DROP VIEW IF EXISTS `bookstock`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `bookstock` AS select `book`.`bkID` AS `bkID`,`book`.`name` AS `name`,`book`.`author` AS `author`,`book`.`edition` AS `edition`,`book`.`type` AS `type`,`stock`.`stockID` AS `stockID`,`stock`.`book_id` AS `book_id`,`stock`.`amount` AS `amount` from (`book` join `stock` on((`book`.`bkID` = `stock`.`book_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-14 17:50:25
