CREATE TABLE test_user (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(30) NOT NULL,
    age INT NOT NULL,
    household INT NOT NULL,
    password VARCHAR(128) NOT NULL,
    PRIMARY KEY (id)
);