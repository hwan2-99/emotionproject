-- MySQL dump 10.13  Distrib 8.0.27, for macos11 (x86_64)
--
-- Host: localhost    Database: emotion
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
-- Table structure for table `result`
--

DROP TABLE IF EXISTS `result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `result` (
                          `id` int NOT NULL AUTO_INCREMENT,
                          `user` varchar(45) DEFAULT NULL,
                          `voice` double DEFAULT NULL,
                          `face` double DEFAULT NULL,
                          `brain` double DEFAULT NULL,
                          `create_at` datetime DEFAULT CURRENT_TIMESTAMP,
                          PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result`
--

LOCK TABLES `result` WRITE;
/*!40000 ALTER TABLE `result` DISABLE KEYS */;
INSERT INTO `result` VALUES (1,'admin',0.812,0.222,0.753,'2022-02-03 10:00:00'),(2,'admin',0.132,0.134,0.122,'2022-02-03 10:02:00'),(3,'admin',0.614,0.762,0.751,'2022-02-03 10:04:00'),(4,'admin',0.115,0.342,0.754,'2022-02-03 10:06:00'),(5,'admin',0.845,0.788,0.982,'2022-02-03 10:08:00'),(6,'admin',0.115,0.121,0.755,'2022-02-03 10:10:00'),(7,'admin',0.812,0.712,0.872,'2022-02-03 10:12:00'),(8,'admin',0.999,0.999,0.999,'2022-02-03 10:14:00'),(9,'admin',0.132,0.211,0.735,'2022-02-03 10:16:00'),(10,'admin',0.812,0.132,0.175,'2022-02-03 10:18:00'),(11,'admin',0.132,0.922,0.755,'2022-02-03 10:20:00'),(12,'admin',0.111,0.132,0.374,'2022-02-03 10:22:00'),(13,'admin',0.212,0.211,0.123,'2022-02-03 10:24:00'),(14,'admin',0.812,0.342,0.425,'2022-02-03 10:26:00'),(15,'admin',0.812,0.442,0.751,'2022-02-03 10:28:00'),(16,'admin',0.132,0.242,0.122,'2022-02-03 10:30:00'),(17,'admin',0.812,0.442,0.755,'2022-02-03 10:32:00'),(18,'admin',0.111,0.222,0.122,'2022-02-03 10:34:00'),(19,'admin',0.132,0.342,0.175,'2022-02-03 10:36:00'),(20,'admin',0.812,0.222,0.175,'2022-02-03 10:38:00'),(21,'admin',0.132,0.222,0.123,'2022-02-03 10:40:00'),(22,'admin',0.812,0.342,0.755,'2022-02-03 10:42:00'),(23,'admin',0.111,0.222,0.122,'2022-02-03 10:44:00'),(24,'admin',0.812,0.142,0.755,'2022-02-03 10:46:00'),(25,'admin',0.132,0.222,0.751,'2022-02-03 10:48:00'),(26,'admin',0.812,0.342,0.175,'2022-02-03 10:50:00'),(27,'admin',0.132,0.142,0.755,'2022-02-03 10:52:00'),(28,'admin',0.111,0.142,0.123,'2022-02-03 10:54:00'),(29,'admin',0.812,0.222,0.122,'2022-02-03 10:56:00'),(30,'admin',0.132,0.142,0.123,'2022-02-03 10:58:00'),(31,'admin',0.812,0.222,0.821,'2022-02-03 11:00:00');
/*!40000 ALTER TABLE `result` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-13 15:33:48
