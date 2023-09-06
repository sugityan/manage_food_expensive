CREATE TABLE user (
    userID INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(128) NOT NULL,
    age INT NOT NULL,
    household INT NOT NULL,
    pass_word VARCHAR(128) NOT NULL,
    PRIMARY KEY (userID)
);

CREATE TABLE cost (
    costID INT NOT NULL AUTO_INCREMENT,
    buy_date VARCHAR(128) NOT NULL,
    uses INT NOT NULL,
    price INT NOT NULL,
    userID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES user(userID),
    PRIMARY KEY (costID)
);

CREATE TABLE food (
    foodID INT NOT NULL AUTO_INCREMENT,
    food_name VARCHAR(128) NOT NULL,
    category INT NOT NULL,
    price INT NOT NULL,
    limit_date INT NOT NULL,
    buy_date INT NOT NULL,
    amount INT NOT NULL,
    unit INT NOT NULL,
    memo VARCHAR(256) NOT NULL,
    remain_ratio INT NOT NULL,
    userID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES user(userID),
    PRIMARY KEY (foodID)
);