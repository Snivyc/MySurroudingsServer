/*
 Navicat SQLite Data Transfer

 Source Server         : date
 Source Server Type    : SQLite
 Source Server Version : 3021000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3021000
 File Encoding         : 65001

 Date: 09/05/2018 17:01:24
*/

--PRAGMA foreign_keys = true;

-- ----------------------------
-- Table structure for USER
-- ----------------------------
DROP TABLE IF EXISTS POINT;
DROP TABLE IF EXISTS USER;

CREATE TABLE USER (
  AccountID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  Account TEXT NOT NULL UNIQUE,
  Password TEXT NOT NULL
);

INSERT INTO "USER" (Account, Password) VALUES ('admin', '123456');

INSERT INTO "USER" (Account, Password) VALUES ('cthcth', '000000');


CREATE TABLE POINT (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  X DOUBLE ,
  Y DOUBLE ,
  Information TEXT ,
  author_id INTEGER ,
  FOREIGN KEY (author_id) REFERENCES USER (AccountID)
);



-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
--DROP TABLE IF EXISTS "sqlite_sequence";
--CREATE TABLE "sqlite_sequence" (
--  "name",
--  "seq"
--);
--
---- ----------------------------
---- Auto increment value for USER
---- ----------------------------
--UPDATE "sqlite_sequence" SET seq = 1 WHERE name = 'USER';

