-- MySQL dump 10.11
--
-- Host: localhost    Database: gld
-- ------------------------------------------------------
-- Server version	5.0.32-Debian_7etch11

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
-- Table structure for table `greylist`
--

DROP TABLE IF EXISTS `greylist`;
CREATE TABLE `greylist` (
  `ip` char(16) NOT NULL default '',
  `sender` char(242) NOT NULL default '',
  `recipient` char(242) NOT NULL default '',
  `first` int(11) NOT NULL default '0',
  `last` int(11) NOT NULL default '0',
  `n` int(11) NOT NULL default '0',
  PRIMARY KEY  (`ip`,`sender`,`recipient`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='greylist';

--
-- Table structure for table `whitelist`
--

DROP TABLE IF EXISTS `whitelist`;
CREATE TABLE `whitelist` (
  `mail` char(242) NOT NULL default '',
  `comment` char(242) NOT NULL default '',
  PRIMARY KEY  (`mail`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-02-27 11:06:50
