-- MySQL dump 10.11
--
-- Host: localhost    Database: mail
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
-- Table structure for table `access`
--

DROP TABLE IF EXISTS `access`;
CREATE TABLE `access` (
  `uname` varchar(255) default NULL,
  `type` varchar(255) default NULL,
  KEY `uname` (`uname`),
  KEY `type` (`type`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `accountuser`
--

DROP TABLE IF EXISTS `accountuser`;
CREATE TABLE `accountuser` (
  `username` varchar(255) default NULL,
  `firstname` varchar(32) default NULL,
  `lastname` varchar(255) default NULL,
  `password` varchar(34) default NULL,
  `domain_name` varchar(255) NOT NULL default '',
  `company` int(32) default '0',
  `status` int(1) default '1',
  `quota` int(20) default NULL,
  `virus_lover` char(1) default NULL,
  `spam_lover` char(1) default NULL,
  `banned_files_lover` char(1) default NULL,
  `bad_header_lover` char(1) default NULL,
  `bypass_virus_checks` char(1) default NULL,
  `bypass_spam_checks` char(1) default NULL,
  `bypass_banned_checks` char(1) default NULL,
  `bypass_header_checks` char(1) default NULL,
  `spam_modifies_subj` char(1) default NULL,
  `spam_quarantine_to` varchar(64) default NULL,
  `spam_tag_level` float default NULL,
  `spam_tag2_level` float default NULL,
  `spam_kill_level` float default NULL,
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `alias`
--

DROP TABLE IF EXISTS `alias`;
CREATE TABLE `alias` (
  `id` bigint(20) NOT NULL auto_increment,
  `alias` varchar(255) NOT NULL default '',
  `dest` longtext,
  `status` int(1) NOT NULL default '1',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=211 DEFAULT CHARSET=latin1;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
CREATE TABLE `companies` (
  `id` int(20) NOT NULL auto_increment,
  `name` varchar(255) NOT NULL default '',
  `prefix` varchar(5) default NULL,
  `telephone` varchar(20) default NULL,
  `fax` varchar(20) default NULL,
  `email` varchar(255) default NULL,
  `street` varchar(255) default NULL,
  `zip` int(4) default NULL,
  `city` varchar(255) default NULL,
  `busaddr` longtext,
  `county` varchar(64) default NULL,
  `postaddr` longtext,
  `webpage` varchar(64) default NULL,
  `cellphone` varchar(64) default NULL,
  `contact` varchar(64) default NULL,
  `orgnr` int(20) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=142 DEFAULT CHARSET=latin1;

--
-- Table structure for table `company_access`
--

DROP TABLE IF EXISTS `company_access`;
CREATE TABLE `company_access` (
  `uname` varchar(255) NOT NULL default '',
  `company` bigint(20) NOT NULL default '0',
  KEY `uname` (`uname`),
  KEY `company` (`company`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `recipient`
--

DROP TABLE IF EXISTS `recipient`;
CREATE TABLE `recipient` (
  `id` int(32) NOT NULL auto_increment,
  `address` varchar(32) NOT NULL default '',
  `action` varchar(32) NOT NULL default '',
  `status` int(1) NOT NULL default '1',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Table structure for table `spamassassin`
--

DROP TABLE IF EXISTS `spamassassin`;
CREATE TABLE `spamassassin` (
  `username` varchar(8) NOT NULL default '',
  `preference` varchar(30) NOT NULL default '',
  `value` varchar(100) NOT NULL default '',
  `prefid` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`prefid`),
  KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sympa`
--

DROP TABLE IF EXISTS `sympa`;
CREATE TABLE `sympa` (
  `id` bigint(20) NOT NULL auto_increment,
  `virtual` varchar(255) NOT NULL default '',
  `alias` varchar(255) NOT NULL default '',
  `dest` longtext NOT NULL,
  `status` int(1) NOT NULL default '1',
  `domain` longtext NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=469 DEFAULT CHARSET=latin1;

--
-- Table structure for table `virtual`
--

DROP TABLE IF EXISTS `virtual`;
CREATE TABLE `virtual` (
  `id` bigint(20) NOT NULL auto_increment,
  `alias` varchar(255) NOT NULL default '',
  `dest` longtext,
  `username` varchar(30) NOT NULL default '',
  `status` int(11) NOT NULL default '1',
  `domain` longtext,
  `greylist` char(1) NOT NULL default 'Y',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1331 DEFAULT CHARSET=latin1;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-02-27 11:07:02
