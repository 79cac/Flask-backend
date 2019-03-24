-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: attack_flow
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--
LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Dumping data for table `userinfo`
--

DROP TABLE IF EXISTS `userinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userinfo` (
  `username` varchar(20) NOT NULL,
  `logInTime` bigint(20) DEFAULT NULL,
  `logOutTime` bigint(20) DEFAULT NULL,
  CONSTRAINT `username` FOREIGN KEY (`username`) REFERENCES `user` (`username`)  
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userinfo`
--
LOCK TABLES `userinfo` WRITE;
/*!40000 ALTER TABLE `userinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `userinfo` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Dumping data for table `taskindex`
--

DROP TABLE IF EXISTS `taskindex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taskindex` (
  `username` varchar(20) NOT NULL,
  `task_name` varchar(20) NOT NULL,
  `attack_name` varchar(60) NOT NULL,
  `times` int(11) NOT NULL,
  `feedback` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taskindex`
--
LOCK TABLES `taskindex` WRITE;
/*!40000 ALTER TABLE `taskindex` DISABLE KEYS */;
/*!40000 ALTER TABLE `taskindex` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Dumping data for table `taskinfo`
--

DROP TABLE IF EXISTS `taskinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taskinfo` (
  `task_id` int(11) NOT NULL,
  `task_name` varchar(60) NOT NULL,
  `srcIP` varchar(20) NOT NULL,
  `dstIP` varchar(20) NOT NULL,
  `starttime` bigint(20) NOT NULL,
  `endtime` bigint(20) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taskinfo`
--
LOCK TABLES `taskinfo` WRITE;
/*!40000 ALTER TABLE `taskinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `taskinfo` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `taskprogress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taskprogress` (
  `task_id` int(11) NOT NULL,
  `attack_name` varchar(60) NOT NULL,
  `times` int(11) NOT NULL,
  `feedback` int(11) NOT NULL,
  `status` int(11) DEFAULT NULL,
  CONSTRAINT `task_id` FOREIGN KEY (`task_id`) REFERENCES `taskinfo` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taskprogress`
--
LOCK TABLES `taskprogress` WRITE;
/*!40000 ALTER TABLE `taskprogress` DISABLE KEYS */;
/*!40000 ALTER TABLE `taskprogress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `icmphdr`
--

DROP TABLE IF EXISTS `icmphdr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `icmphdr` (
  `attack_id` int(11) DEFAULT NULL,
  `pkt_num` int(11) DEFAULT NULL,
  `icmp_type` varchar(20) DEFAULT NULL,
  `code` int(11) DEFAULT NULL,
  `seq` int(11) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  KEY `attack_id` (`attack_id`),
  CONSTRAINT `icmphdr_ibfk_1` FOREIGN KEY (`attack_id`) REFERENCES `index` (`attack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `icmphdr`
--

LOCK TABLES `icmphdr` WRITE;
/*!40000 ALTER TABLE `icmphdr` DISABLE KEYS */;
/*!40000 ALTER TABLE `icmphdr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `index`
--

DROP TABLE IF EXISTS `index`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `index` (
  `attack_id` int(11) NOT NULL AUTO_INCREMENT,
  `attack_name` varchar(60) NOT NULL UNIQUE,
  `plat_info` varchar(20) DEFAULT NULL,
  `target_info` varchar(20) DEFAULT NULL,
  `proto` varchar(20) DEFAULT NULL,
  `src_ip` varchar(20) DEFAULT NULL,
  `dst_ip` varchar(20) DEFAULT NULL,
  `ts_type` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`attack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `index`
--

LOCK TABLES `index` WRITE;
/*!40000 ALTER TABLE `index` DISABLE KEYS */;
/*!40000 ALTER TABLE `index` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iphdr`
--

DROP TABLE IF EXISTS `iphdr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iphdr` (
  `attack_id` int(11) DEFAULT NULL,
  `pkt_num` int(11) DEFAULT NULL,
  `ip_version` int(11) DEFAULT NULL,
  `ip_src` varchar(16) DEFAULT NULL,
  `ip_dst` varchar(16) DEFAULT NULL,
  `ip_tos` int(11) DEFAULT NULL,
  `ip_id` int(11) DEFAULT NULL,
  `ip_flags` varchar(4) DEFAULT NULL,
  `ip_frag` int(11) DEFAULT NULL,
  `ip_ttl` int(11) DEFAULT NULL,
  `ip_proto` int(11) DEFAULT NULL,
  KEY `attack_id` (`attack_id`),
  CONSTRAINT `iphdr_ibfk_1` FOREIGN KEY (`attack_id`) REFERENCES `index` (`attack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iphdr`
--

LOCK TABLES `iphdr` WRITE;
/*!40000 ALTER TABLE `iphdr` DISABLE KEYS */;
/*!40000 ALTER TABLE `iphdr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payload`
--

DROP TABLE IF EXISTS `payload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payload` (
  `attack_id` int(11) DEFAULT NULL,
  `pkt_num` int(11) DEFAULT NULL,
  `data_len` mediumtext,
  `data` varchar(2000) DEFAULT NULL,
  KEY `attack_id` (`attack_id`),
  CONSTRAINT `payload_ibfk_1` FOREIGN KEY (`attack_id`) REFERENCES `index` (`attack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payload`
--

LOCK TABLES `payload` WRITE;
/*!40000 ALTER TABLE `payload` DISABLE KEYS */;
/*!40000 ALTER TABLE `payload` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `state`
--

DROP TABLE IF EXISTS `state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `state` (
  `attack_id` int(11) DEFAULT NULL,
  `pkt_num` int(11) DEFAULT NULL,
  `op_code` int(11) DEFAULT NULL,
  `proto` varchar(10) DEFAULT NULL,
  `next_1` int(11) DEFAULT NULL,
  `next_2` int(11) DEFAULT NULL,
  KEY `attack_id` (`attack_id`),
  CONSTRAINT `state_ibfk_1` FOREIGN KEY (`attack_id`) REFERENCES `index` (`attack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `state`
--

LOCK TABLES `state` WRITE;
/*!40000 ALTER TABLE `state` DISABLE KEYS */;
/*!40000 ALTER TABLE `state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tcphdr`
--

DROP TABLE IF EXISTS `tcphdr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tcphdr` (
  `attack_id` int(11) DEFAULT NULL,
  `pkt_num` int(11) DEFAULT NULL,
  `tcp_sport` int(11) DEFAULT NULL,
  `tcp_dport` int(11) DEFAULT NULL,
  `tcp_seq` bigint(20) DEFAULT NULL,
  `tcp_ack` bigint(20) DEFAULT NULL,
  `tcp_flags` varchar(4) DEFAULT NULL,
  `tcp_win` int(11) DEFAULT NULL,
  `dataofs` int(11) DEFAULT NULL,
  `reserved` int(11) DEFAULT NULL,
  `urgptr` int(11) DEFAULT NULL,
  `options` varchar(200) DEFAULT NULL,
  KEY `attack_id` (`attack_id`),
  CONSTRAINT `tcphdr_ibfk_1` FOREIGN KEY (`attack_id`) REFERENCES `index` (`attack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tcphdr`
--

LOCK TABLES `tcphdr` WRITE;
/*!40000 ALTER TABLE `tcphdr` DISABLE KEYS */;
/*!40000 ALTER TABLE `tcphdr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tshdr`
--

DROP TABLE IF EXISTS `timestamp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timestamp` (
  `attack_id` int(11) DEFAULT NULL,
  `pkt_num` int(11) DEFAULT NULL,
  `delta_sec` int(11) DEFAULT NULL,
  `delta_usec` int(11) DEFAULT NULL,
  KEY `attack_id` (`attack_id`),
  CONSTRAINT `timestamp_ibfk_1` FOREIGN KEY (`attack_id`) REFERENCES `index` (`attack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timestamp`
--

LOCK TABLES `timestamp` WRITE;
/*!40000 ALTER TABLE `timestamp` DISABLE KEYS */;
/*!40000 ALTER TABLE `timestamp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `udphdr`
--

DROP TABLE IF EXISTS `udphdr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `udphdr` (
  `attack_id` int(11) DEFAULT NULL,
  `pkt_num` int(11) DEFAULT NULL,
  `udp_sport` int(11) DEFAULT NULL,
  `udp_dport` int(11) DEFAULT NULL,
  `udp_len` mediumtext,
  KEY `attack_id` (`attack_id`),
  CONSTRAINT `udphdr_ibfk_1` FOREIGN KEY (`attack_id`) REFERENCES `index` (`attack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `udphdr`
--

LOCK TABLES `udphdr` WRITE;
/*!40000 ALTER TABLE `udphdr` DISABLE KEYS */;
/*!40000 ALTER TABLE `udphdr` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

insert into `user` (username, password) VALUES ('admin', 'password');
