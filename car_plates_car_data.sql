-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: car_plates
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `car_data`
--

DROP TABLE IF EXISTS `car_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plate_number` varchar(15) NOT NULL,
  `plate_letters` varchar(10) NOT NULL,
  `car_type` varchar(50) NOT NULL,
  `car_owner` varchar(100) NOT NULL,
  `governorate` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_data`
--

LOCK TABLES `car_data` WRITE;
/*!40000 ALTER TABLE `car_data` DISABLE KEYS */;
INSERT INTO `car_data` VALUES (1,'7126','سطن','fiat 126','salem fathy','Alexandria'),(2,'1','وطن','mesarati','ahmed elswidy','beni suef'),(3,'8432','طسم','opel vectra','islam samy','suez'),(4,'748','نقق','toyota','youssef mourad','menya'),(5,'4851','روى','nissan sunny','saad marei','sharkia'),(6,'5498','سوف','opel corsa','omar tolba','alexandria'),(7,'1111','قوى','bmw','omar amr','kalyoubeia'),(8,'1','عربـ','mercedes','yahia zahran','gharbia'),(9,'1111','هدى','porche cayenne','huda elmasry','suhag'),(10,'444','دلع','range rouver','ezz sabry','dakahleia');
/*!40000 ALTER TABLE `car_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-04 22:51:52
