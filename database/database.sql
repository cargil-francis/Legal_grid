/*
SQLyog Community v13.1.7 (64 bit)
MySQL - 10.4.10-MariaDB : Database - grade_upsc
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`grade_upsc` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `grade_upsc`;

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `cat_id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `category` */

/*Table structure for table `current_affairs` */

DROP TABLE IF EXISTS `current_affairs`;

CREATE TABLE `current_affairs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_affairs` varchar(255) DEFAULT NULL,
  `descriptions` varchar(255) DEFAULT NULL,
  `ca_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `current_affairs` */

/*Table structure for table `questions` */

DROP TABLE IF EXISTS `questions`;

CREATE TABLE `questions` (
  `q_id` int(11) NOT NULL AUTO_INCREMENT,
  `subcat_id` int(11) DEFAULT NULL,
  `question` varchar(255) DEFAULT NULL,
  `descriptions` varchar(255) DEFAULT NULL,
  `opt_a` varchar(255) DEFAULT NULL,
  `opt_b` varchar(255) DEFAULT NULL,
  `opt_c` varchar(255) DEFAULT NULL,
  `opt_d` varchar(255) DEFAULT NULL,
  `ans_key` varchar(255) DEFAULT NULL,
  `ques_flag` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`q_id`),
  KEY `subcat_id` (`subcat_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `questions` */

/*Table structure for table `subcategory` */

DROP TABLE IF EXISTS `subcategory`;

CREATE TABLE `subcategory` (
  `subcat_id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` int(11) DEFAULT NULL,
  `subcategory` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`subcat_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `subcategory` */

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phn_no` varchar(255) DEFAULT NULL,
  `usr_status` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `users` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
