create database MachineLearning;
use MachineLearning;

create table users(
id  int auto_increment primary key,
username varchar(256) not null,
password varchar(255) not null unique
);
