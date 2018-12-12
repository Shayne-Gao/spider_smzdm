/*
Navicat MySQL Data Transfer

Source Server         : baiye.website
Source Server Version : 50714
Source Host           : 139.162.29.252:3306
Source Database       : smzdm

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2016-12-22 10:38:20
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for smzdm_record
-- ----------------------------
DROP TABLE IF EXISTS `smzdm_record`;
CREATE TABLE `smzdm_record` (
  `title` VARCHAR(512) DEFAULT NULL,
  `price` VARCHAR(256) DEFAULT NULL,
  `link` VARCHAR(512) DEFAULT NULL,
  `page_url` VARCHAR(512) DEFAULT NULL,
  `md5` VARCHAR(128) NOT NULL,
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `pic_url` VARCHAR(128) DEFAULT NULL,
  `source` VARCHAR(32) DEFAULT NULL,
  PRIMARY KEY (`md5`),
  KEY `md5_index` (`md5`) USING BTREE
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4
