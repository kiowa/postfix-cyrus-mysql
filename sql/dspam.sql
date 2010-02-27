-- MySQL dump 10.11
--
-- Host: localhost    Database: dspam
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
-- Table structure for table `dspam_neural_data`
--

DROP TABLE IF EXISTS `dspam_neural_data`;
CREATE TABLE `dspam_neural_data` (
  `uid` smallint(5) unsigned default NULL,
  `node` smallint(5) unsigned default NULL,
  `total_correct` int(11) default NULL,
  `total_incorrect` int(11) default NULL,
  UNIQUE KEY `id_neural_data_02` (`uid`,`node`),
  KEY `id_neural_data_01` (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `dspam_neural_decisions`
--

DROP TABLE IF EXISTS `dspam_neural_decisions`;
CREATE TABLE `dspam_neural_decisions` (
  `uid` smallint(5) unsigned default NULL,
  `signature` varchar(128) default NULL,
  `data` blob,
  `length` smallint(6) default NULL,
  `created_on` date default NULL,
  UNIQUE KEY `id_neural_decisions_01` (`uid`,`signature`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `dspam_preferences`
--

DROP TABLE IF EXISTS `dspam_preferences`;
CREATE TABLE `dspam_preferences` (
  `uid` smallint(5) unsigned NOT NULL default '0',
  `preference` varchar(32) NOT NULL default '',
  `value` varchar(64) NOT NULL default '',
  UNIQUE KEY `id_preferences_01` (`uid`,`preference`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `dspam_signature_data`
--

DROP TABLE IF EXISTS `dspam_signature_data`;
CREATE TABLE `dspam_signature_data` (
  `uid` smallint(5) unsigned default NULL,
  `signature` varchar(128) default NULL,
  `data` blob,
  `length` smallint(6) default NULL,
  `created_on` date default NULL,
  UNIQUE KEY `id_signature_data_01` (`uid`,`signature`),
  KEY `id_signature_data_02` (`created_on`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `dspam_stats`
--

DROP TABLE IF EXISTS `dspam_stats`;
CREATE TABLE `dspam_stats` (
  `uid` smallint(5) unsigned NOT NULL default '0',
  `spam_learned` int(11) default NULL,
  `innocent_learned` int(11) default NULL,
  `spam_misclassified` int(11) default NULL,
  `innocent_misclassified` int(11) default NULL,
  `spam_corpusfed` int(11) default NULL,
  `innocent_corpusfed` int(11) default NULL,
  `spam_classified` int(11) default NULL,
  `innocent_classified` int(11) default NULL,
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `dspam_token_data`
--

DROP TABLE IF EXISTS `dspam_token_data`;
CREATE TABLE `dspam_token_data` (
  `uid` smallint(5) unsigned default NULL,
  `token` bigint(20) unsigned default NULL,
  `spam_hits` int(11) default NULL,
  `innocent_hits` int(11) default NULL,
  `last_hit` date default NULL,
  UNIQUE KEY `id_token_data_01` (`uid`,`token`),
  KEY `id_token_data_02` (`innocent_hits`),
  KEY `id_token_data_04` (`uid`),
  KEY `id_token_data_03` (`spam_hits`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 PACK_KEYS=1;

--
-- Table structure for table `dspam_virtual_uids`
--

DROP TABLE IF EXISTS `dspam_virtual_uids`;
CREATE TABLE `dspam_virtual_uids` (
  `uid` smallint(5) unsigned NOT NULL auto_increment,
  `username` varchar(128) default NULL,
  PRIMARY KEY  (`uid`),
  UNIQUE KEY `id_virtual_uids_02` (`uid`),
  UNIQUE KEY `id_virtual_uids_01` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=5859 DEFAULT CHARSET=latin1;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-02-27 11:06:29
