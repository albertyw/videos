-- phpMyAdmin SQL Dump
-- version 4.0.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 09, 2013 at 05:19 PM
-- Server version: 5.5.31-0ubuntu0.12.04.2
-- PHP Version: 5.3.10-1ubuntu3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `videos`
--
CREATE DATABASE IF NOT EXISTS `videos` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `videos`;

-- --------------------------------------------------------

--
-- Table structure for table `accesslog`
--

CREATE TABLE IF NOT EXISTS `accesslog` (
  `id` int(11) NOT NULL,
  `accesstime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ip` varchar(20) NOT NULL,
  `reversedns` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `directories`
--

CREATE TABLE IF NOT EXISTS `directories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `directory` varchar(100) NOT NULL,
  `server` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=33 ;

-- --------------------------------------------------------

--
-- Table structure for table `downloads`
--

CREATE TABLE IF NOT EXISTS `downloads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `directory` int(11) NOT NULL,
  `file` int(11) NOT NULL,
  `downloadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ip` varchar(20) NOT NULL,
  `reversedns` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2196 ;

-- --------------------------------------------------------

--
-- Table structure for table `localfiles`
--

CREATE TABLE IF NOT EXISTS `localfiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(100) NOT NULL,
  `filedirectory` varchar(100) NOT NULL,
  `size` bigint(20) NOT NULL,
  `modtime` int(11) NOT NULL,
  `downloads` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1175 ;

-- --------------------------------------------------------

--
-- Table structure for table `moviepooper`
--

CREATE TABLE IF NOT EXISTS `moviepooper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(100) NOT NULL,
  `filedirectory` varchar(100) NOT NULL,
  `size` int(11) NOT NULL,
  `downloads` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1927 ;

-- --------------------------------------------------------

--
-- Table structure for table `tversity`
--

CREATE TABLE IF NOT EXISTS `tversity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(100) NOT NULL,
  `filelocation` varchar(500) NOT NULL,
  `size` int(11) NOT NULL,
  `downloads` int(11) NOT NULL,
  `filedirectory` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1759 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
