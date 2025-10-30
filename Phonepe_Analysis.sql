create database phonepe_db;
use phonepe_db;


CREATE TABLE aggregated_transaction (
  year INT,
  quarter INT,
  category TEXT,
  type TEXT,
  count BIGINT,
  amount DOUBLE PRECISION
);

CREATE TABLE aggregated_user (
  year INT,
  quarter INT,
  brand TEXT,
  count BIGINT,
  percentage DOUBLE PRECISION,
  registered_users BIGINT,
  app_opens BIGINT
);

CREATE TABLE aggregated_insurance (
  year INT,
  quarter INT,
  name TEXT,
  count BIGINT,
  amount DOUBLE PRECISION
);

CREATE TABLE map_transaction (
  year INT,
  quarter INT,
  state TEXT,
  count BIGINT,
  amount DOUBLE PRECISION
);

CREATE TABLE map_user (
  year INT,
  quarter INT,
  state TEXT,
  registered_users BIGINT,
  app_opens BIGINT
);

CREATE TABLE map_insurance (
  year INT,
  quarter INT,
  state TEXT,
  count BIGINT,
  amount DOUBLE PRECISION
);

CREATE TABLE top_transaction (
  year INT,
  quarter INT,
  level TEXT,
  entity TEXT,
  count BIGINT,
  amount DOUBLE PRECISION
);

CREATE TABLE top_user (
  year INT,
  quarter INT,
  level TEXT,
  entity TEXT,
  registered_users BIGINT
);

CREATE TABLE top_insurance (
  year INT,
  quarter INT,
  level TEXT,
  entity TEXT,
  count BIGINT,
  amount DOUBLE PRECISION
);

show tables;

SET GLOBAL local_infile = 1;

SHOW VARIABLES LIKE 'local_infile';

LOAD DATA LOCAL INFILE 'C:/Users/prash/Downloads/phonepe_project/parsed_output/aggregated_transaction.csv'
INTO TABLE aggregated_transaction
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/prash/Downloads/phonepe_project/parsed_output/aggregated_user.csv'
INTO TABLE aggregated_user
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/prash/Downloads/phonepe_project/parsed_output/aggregated_insurance.csv'
INTO TABLE aggregated_insurance
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/prash/Downloads/phonepe_project/parsed_output/map_transaction.csv'
INTO TABLE map_transaction
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/prash/Downloads/phonepe_project/parsed_output/map_user.csv'
INTO TABLE map_user
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/prash/Downloads/phonepe_project/parsed_output/map_insurance.csv'
INTO TABLE map_insurance
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/prash/Downloads/phonepe_project/parsed_output/top_transaction.csv'
INTO TABLE top_transaction
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/prash/Downloads/phonepe_project/parsed_output/top_user.csv'
INTO TABLE top_user
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/prash/Downloads/phonepe_project/parsed_output/top_insurance.csv'
INTO TABLE top_insurance
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


select * from aggregated_transaction;


USE phonepe_pulse;

-- CASE STUDY 1: Decoding Transaction Dynamics on PhonePe

-- Scenario:
-- Analyze transaction behavior across years, quarters, and states to identify growth or stagnation patterns.

SELECT 
    year,
    quarter,
    state,
    ROUND(SUM(amount)/10000000, 2) AS total_amount_crores,
    ROUND(SUM(count)/1000000, 2) AS total_txn_millions
FROM map_transaction
GROUP BY year, quarter, state
ORDER BY year, quarter, total_amount_crores DESC;

-- Insight :
-- Transaction value surged in 2022–2023, with Karnataka, Maharashtra, and Tamil Nadu leading.
-- Seasonal patterns (Q4 peaks) may suggest festival-based spending spikes.


--  CASE STUDY 2: Device Dominance and User Engagement Analysis
-- Scenario:
-- Understand which mobile brands drive user registrations and engagement (app opens).

SELECT 
    brand,
    SUM(registered_users) AS total_registered_users,
    SUM(app_opens) AS total_app_opens,
    ROUND(SUM(app_opens) / SUM(registered_users), 2) AS engagement_ratio
FROM aggregated_user
GROUP BY brand
ORDER BY total_registered_users DESC
LIMIT 10;

-- Insight:
-- Xiaomi and Samsung dominate registrations.
-- Apple shows higher app engagement ratio, even with fewer registrations.


-- CASE STUDY 3: Insurance Penetration and Growth Potential
-- Scenario:
-- Analyze insurance transaction performance to identify states with untapped growth potential.

SELECT 
    year,
    state,
    ROUND(SUM(count)/1000, 2) AS total_policies_in_thousands,
    ROUND(SUM(amount)/10000000, 2) AS total_premium_crores
FROM map_insurance
GROUP BY year, state
ORDER BY total_premium_crores DESC
LIMIT 10;

-- Insight:
--  Maharashtra and Karnataka dominate insurance transactions.
-- Eastern and North-Eastern states show growth potential (low current adoption).


-- CASE STUDY 4: Transaction Analysis for Market Expansion
-- Scenario:
-- Identify the top states/districts where PhonePe should focus expansion.

SELECT 
    state,
    ROUND(SUM(amount)/10000000, 2) AS total_amount_crores,
    ROUND(SUM(count)/1000000, 2) AS total_transactions_millions
FROM map_transaction
GROUP BY state
ORDER BY total_amount_crores DESC
LIMIT 10;

-- Insight:
-- Tier-1 states lead the charge, but emerging growth is seen in Telangana and karnataka.
-- Strategic investment in underperforming high-population states can increase share.



-- CASE STUDY 5: User Registration Analysis
-- Scenario:
-- Find where most users registered from, by district and state, to identify strong and weak regions.

select *from top_user;

SELECT 
    entity AS district,
    SUM(registered_users) AS total_registered_users
FROM top_user
WHERE level = 'districts'
GROUP BY entity
ORDER BY total_registered_users DESC
LIMIT 10;

-- Insight:
-- Districts like Bengaluru Urban, Pune, and thane dominate user base.
-- These regions are strongholds for digital payment adoption.






DESCRIBE aggregated_insurance;
DESCRIBE aggregated_transaction;
DESCRIBE aggregated_user;
DESCRIBE map_insurance;
DESCRIBE map_transaction;
DESCRIBE map_user;
DESCRIBE top_insurance;
DESCRIBE top_transaction;
DESCRIBE top_user;
