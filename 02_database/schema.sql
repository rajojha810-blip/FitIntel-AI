DROP DATABASE IF EXISTS fitintel;

CREATE DATABASE fitintel;
USE fitintel;

-- 1. Users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20),
    height_cm DECIMAL(5,2) NOT NULL,
    initial_weight_kg DECIMAL(5,2) NOT NULL,
    goal VARCHAR(30) NOT NULL,
    activity_level VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Daily Metrics
CREATE TABLE daily_metrics (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    weight_kg DECIMAL(5,2),
    calories_consumed INT,
    protein_consumed_g DECIMAL(6,2),
    steps INT,
    water_liters DECIMAL(4,2),
    sleep_hours DECIMAL(4,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 3. Workouts
CREATE TABLE workouts (
    workout_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    workout_type VARCHAR(50),
    duration_minutes INT,
    calories_burned INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 4. Exercises
CREATE TABLE exercises (
    exercise_id INT AUTO_INCREMENT PRIMARY KEY,
    workout_id INT NOT NULL,
    exercise_name VARCHAR(100),
    sets INT,
    reps INT,
    weight_kg DECIMAL(6,2),
    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id)
);

-- 5. Goals
CREATE TABLE goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    goal_type VARCHAR(30),
    target_weight_kg DECIMAL(5,2),
    target_calories INT,
    target_protein_g DECIMAL(6,2),
    start_date DATE,
    target_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Link metrics to user
ALTER TABLE daily_metrics 
ADD COLUMN user_id INT DEFAULT 1;

USE fitintel;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);