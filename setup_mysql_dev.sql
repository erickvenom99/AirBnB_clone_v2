

-- Create the database hbnb_dev_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- create the user hbnb_dev and  password hbnb_dev_pwd
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- grant all privileges to the user hbnb_dev
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- grant SELECT privilege on the performance_schema database (and only this database):
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- flush the privileges to effect changes
FLUSH PRIVILEGES;
