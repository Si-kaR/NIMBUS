-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 07, 2024 at 05:28 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nimbus`
--

-- --------------------------------------------------------

--
-- Table structure for table `educationalcontent`
--

CREATE TABLE `educationalcontent` (
  `ContentID` int(11) NOT NULL,
  `Title` varchar(255) DEFAULT NULL,
  `ContentType` enum('Article','Video','Quiz') DEFAULT NULL,
  `Content` text DEFAULT NULL,
  `Topic` enum('PersonalFinance','Budgeting','Investing') DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `educationalcontent`
--

INSERT INTO `educationalcontent` (`ContentID`, `Title`, `ContentType`, `Content`, `Topic`, `CreatedAt`) VALUES
(1, 'Investing 101', 'Article', 'This is content about investing.', 'Investing', '2024-08-07 03:27:18');

-- --------------------------------------------------------

--
-- Table structure for table `financialdata`
--

CREATE TABLE `financialdata` (
  `AssetID` int(11) NOT NULL,
  `AssetName` varchar(255) DEFAULT NULL,
  `AssetType` enum('Stock','Bond','RealEstate','Commodity','Cryptocurrency') DEFAULT NULL,
  `CurrentValue` decimal(10,2) DEFAULT NULL,
  `LastUpdated` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `financialdata`
--

INSERT INTO `financialdata` (`AssetID`, `AssetName`, `AssetType`, `CurrentValue`, `LastUpdated`) VALUES
(1, 'Gold', 'Commodity', 1800.00, '2024-08-07 03:27:18');

-- --------------------------------------------------------

--
-- Table structure for table `investmentpreferences`
--

CREATE TABLE `investmentpreferences` (
  `PreferenceID` int(11) NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `RiskTolerance` enum('Low','Medium','High') DEFAULT 'Medium',
  `DiversificationLevel` enum('Conservative','Balanced','Aggressive') DEFAULT 'Balanced'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `investmentpreferences`
--

INSERT INTO `investmentpreferences` (`PreferenceID`, `UserID`, `RiskTolerance`, `DiversificationLevel`) VALUES
(1, 1, 'Medium', 'Conservative');

-- --------------------------------------------------------

--
-- Table structure for table `portfolioassets`
--

CREATE TABLE `portfolioassets` (
  `PortfolioAssetID` int(11) NOT NULL,
  `PortfolioID` int(11) DEFAULT NULL,
  `AssetID` int(11) DEFAULT NULL,
  `AllocationPercentage` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `portfolioassets`
--

INSERT INTO `portfolioassets` (`PortfolioAssetID`, `PortfolioID`, `AssetID`, `AllocationPercentage`) VALUES
(1, 1, 1, 50.00);

-- --------------------------------------------------------

--
-- Table structure for table `portfolios`
--

CREATE TABLE `portfolios` (
  `PortfolioID` int(11) NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `PortfolioName` varchar(255) DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `portfolios`
--

INSERT INTO `portfolios` (`PortfolioID`, `UserID`, `PortfolioName`, `CreatedAt`) VALUES
(1, 1, 'Retirement Fund', '2024-08-07 03:27:18');

-- --------------------------------------------------------

--
-- Table structure for table `usercontentprogress`
--

CREATE TABLE `usercontentprogress` (
  `ProgressID` int(11) NOT NULL,
  `UserID` int(11) DEFAULT NULL,
  `ContentID` int(11) DEFAULT NULL,
  `Progress` enum('NotStarted','InProgress','Completed') DEFAULT 'NotStarted',
  `LastAccessed` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usercontentprogress`
--

INSERT INTO `usercontentprogress` (`ProgressID`, `UserID`, `ContentID`, `Progress`, `LastAccessed`) VALUES
(1, 1, 1, 'InProgress', '2024-08-07 03:27:18');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `UserID` int(11) NOT NULL,
  `Username` varchar(255) NOT NULL,
  `PasswordHash` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `RiskTolerance` enum('Low','Medium','High') DEFAULT 'Medium',
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`UserID`, `Username`, `PasswordHash`, `Email`, `RiskTolerance`, `CreatedAt`) VALUES
(1, 'john_doe', 'hashed_password', 'john@example.com', 'High', '2024-08-07 03:27:18');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `educationalcontent`
--
ALTER TABLE `educationalcontent`
  ADD PRIMARY KEY (`ContentID`);

--
-- Indexes for table `financialdata`
--
ALTER TABLE `financialdata`
  ADD PRIMARY KEY (`AssetID`);

--
-- Indexes for table `investmentpreferences`
--
ALTER TABLE `investmentpreferences`
  ADD PRIMARY KEY (`PreferenceID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `portfolioassets`
--
ALTER TABLE `portfolioassets`
  ADD PRIMARY KEY (`PortfolioAssetID`),
  ADD KEY `PortfolioID` (`PortfolioID`),
  ADD KEY `AssetID` (`AssetID`);

--
-- Indexes for table `portfolios`
--
ALTER TABLE `portfolios`
  ADD PRIMARY KEY (`PortfolioID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `usercontentprogress`
--
ALTER TABLE `usercontentprogress`
  ADD PRIMARY KEY (`ProgressID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `ContentID` (`ContentID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`),
  ADD UNIQUE KEY `Username` (`Username`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `educationalcontent`
--
ALTER TABLE `educationalcontent`
  MODIFY `ContentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `financialdata`
--
ALTER TABLE `financialdata`
  MODIFY `AssetID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `investmentpreferences`
--
ALTER TABLE `investmentpreferences`
  MODIFY `PreferenceID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `portfolioassets`
--
ALTER TABLE `portfolioassets`
  MODIFY `PortfolioAssetID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `portfolios`
--
ALTER TABLE `portfolios`
  MODIFY `PortfolioID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `usercontentprogress`
--
ALTER TABLE `usercontentprogress`
  MODIFY `ProgressID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `investmentpreferences`
--
ALTER TABLE `investmentpreferences`
  ADD CONSTRAINT `investmentpreferences_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`);

--
-- Constraints for table `portfolioassets`
--
ALTER TABLE `portfolioassets`
  ADD CONSTRAINT `portfolioassets_ibfk_1` FOREIGN KEY (`PortfolioID`) REFERENCES `portfolios` (`PortfolioID`),
  ADD CONSTRAINT `portfolioassets_ibfk_2` FOREIGN KEY (`AssetID`) REFERENCES `financialdata` (`AssetID`);

--
-- Constraints for table `portfolios`
--
ALTER TABLE `portfolios`
  ADD CONSTRAINT `portfolios_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`);

--
-- Constraints for table `usercontentprogress`
--
ALTER TABLE `usercontentprogress`
  ADD CONSTRAINT `usercontentprogress_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`),
  ADD CONSTRAINT `usercontentprogress_ibfk_2` FOREIGN KEY (`ContentID`) REFERENCES `educationalcontent` (`ContentID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
