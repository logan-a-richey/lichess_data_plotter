-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: lichess_games
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.24.04.1

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
-- Table structure for table `my_games`
--

DROP TABLE IF EXISTS `my_games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `my_games` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `event` varchar(255) NOT NULL DEFAULT '',
  `site` varchar(255) NOT NULL DEFAULT '',
  `my_date` datetime NOT NULL,
  `white` varchar(20) NOT NULL DEFAULT '',
  `black` varchar(20) NOT NULL DEFAULT '',
  `result` varchar(8) NOT NULL DEFAULT '1/2-1/2',
  `gameid` varchar(20) NOT NULL DEFAULT '',
  `whiteelo` int unsigned NOT NULL DEFAULT '1200',
  `blackelo` int unsigned NOT NULL DEFAULT '1200',
  `whitetitle` varchar(8) NOT NULL DEFAULT '',
  `blacktitle` varchar(8) NOT NULL DEFAULT '',
  `whiteratingdiff` varchar(8) NOT NULL DEFAULT '',
  `blackratingdiff` varchar(8) NOT NULL DEFAULT '',
  `variant` varchar(20) NOT NULL DEFAULT 'Standard',
  `timecontrol` varchar(20) NOT NULL DEFAULT '',
  `eco` varchar(20) NOT NULL DEFAULT '',
  `opening` varchar(255) NOT NULL DEFAULT '',
  `short_opening` varchar(255) NOT NULL DEFAULT '',
  `termination` varchar(20) NOT NULL DEFAULT '',
  `move_times` varchar(5000) NOT NULL DEFAULT '',
  `pgn` varchar(5000) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `gameid` (`gameid`),
  KEY `my_date` (`my_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-06 16:35:11
