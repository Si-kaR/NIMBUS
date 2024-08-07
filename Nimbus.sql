CREATE DATABASE nimbus;

USE nimbus;

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    RiskTolerance ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE InvestmentPreferences (
    PreferenceID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    RiskTolerance ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    DiversificationLevel ENUM('Conservative', 'Balanced', 'Aggressive') DEFAULT 'Balanced',
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE FinancialData (
    AssetID INT AUTO_INCREMENT PRIMARY KEY,
    AssetName VARCHAR(255),
    AssetType ENUM('Stock', 'Bond', 'RealEstate', 'Commodity', 'Cryptocurrency'),
    CurrentValue DECIMAL(10, 2),
    LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Portfolios (
    PortfolioID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    PortfolioName VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE PortfolioAssets (
    PortfolioAssetID INT AUTO_INCREMENT PRIMARY KEY,
    PortfolioID INT,
    AssetID INT,
    AllocationPercentage DECIMAL(5, 2),
    FOREIGN KEY (PortfolioID) REFERENCES Portfolios(PortfolioID),
    FOREIGN KEY (AssetID) REFERENCES FinancialData(AssetID)
);

CREATE TABLE EducationalContent (
    ContentID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    ContentType ENUM('Article', 'Video', 'Quiz'),
    Content TEXT,
    Topic ENUM('PersonalFinance', 'Budgeting', 'Investing'),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE UserContentProgress (
    ProgressID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    ContentID INT,
    Progress ENUM('NotStarted', 'InProgress', 'Completed') DEFAULT 'NotStarted',
    LastAccessed TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ContentID) REFERENCES EducationalContent(ContentID)
);
