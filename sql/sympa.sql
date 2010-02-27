-- MySQL dump 10.11
--
-- Host: localhost    Database: sympa
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
-- Table structure for table `subscriber_table`
--

DROP TABLE IF EXISTS `subscriber_table`;
CREATE TABLE `subscriber_table` (
  `list_subscriber` varchar(50) NOT NULL default '',
  `user_subscriber` varchar(100) NOT NULL default '',
  `date_subscriber` datetime NOT NULL default '0000-00-00 00:00:00',
  `update_subscriber` datetime default NULL,
  `visibility_subscriber` varchar(20) default NULL,
  `reception_subscriber` varchar(20) default NULL,
  `bounce_subscriber` varchar(35) default NULL,
  `comment_subscriber` varchar(150) default NULL,
  `include_sources_subscriber` varchar(50) default NULL,
  `subscribed_subscriber` enum('0','1') default NULL,
  `included_subscriber` enum('0','1') default NULL,
  PRIMARY KEY  (`list_subscriber`,`user_subscriber`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `user_table`
--

DROP TABLE IF EXISTS `user_table`;
CREATE TABLE `user_table` (
  `email_user` varchar(100) NOT NULL default '',
  `gecos_user` varchar(150) default NULL,
  `password_user` varchar(40) default NULL,
  `cookie_delay_user` int(11) default NULL,
  `lang_user` varchar(10) default NULL,
  PRIMARY KEY  (`email_user`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-02-27 11:07:16
