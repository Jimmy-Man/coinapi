CREATE USER 'huobi'@'localhost' IDENTIFIED BY 'huobi123';
CREATE DATABASE `huobi`;
grant all privileges on huobi.* to 'huobi'@'localhost';
