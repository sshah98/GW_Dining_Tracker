CREATE TABLE user (
  id INTEGER NOT NULL, 
  fname VARCHAR(100), 
  lname VARCHAR(100), 
  email VARCHAR(100), 
  password VARCHAR(100), 
  PRIMARY KEY (id), 
  UNIQUE (email)
);


CREATE TABLE history(
  count INTEGER PRIMARY KEY AUTOINCREMENT, 
  date INTEGER, 
  account TEXT, 
  time INTEGER, 
  vendor TEXT, 
  price REAL,
  email VARCHAR(100),
  FOREIGN KEY (email) REFERENCES user(email)
);

-- link history and user with the email