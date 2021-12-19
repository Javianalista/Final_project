CREATE SCHEMA `final_project`;

USE final_project;

DROP TABLE movies;

CREATE TABLE movies(
	movieId INT,
    title VARCHAR(255),
    genres VARCHAR(255)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/copy.csv' 
INTO TABLE movies 
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


DROP TABLE ratings;

CREATE TABLE ratings(
	userId INT,
    movieId INT,
    rating FLOAT,
    timestamp INT
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ratings.csv' 
INTO TABLE ratings 
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;