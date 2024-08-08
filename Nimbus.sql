-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 08, 2024 at 08:01 PM
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
-- Table structure for table `context_window`
--

CREATE TABLE `context_window` (
  `context_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `last_response` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `frequent_terms`
--

CREATE TABLE `frequent_terms` (
  `search_term` varchar(255) NOT NULL,
  `frequency` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `risk_levels`
--

CREATE TABLE `risk_levels` (
  `risk_id` int(11) NOT NULL,
  `risk_type` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `risk_levels`
--

INSERT INTO `risk_levels` (`risk_id`, `risk_type`) VALUES
(1, 'High'),
(2, 'Low'),
(3, 'Medium');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `risk_id` int(11) DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `context_window`
--
ALTER TABLE `context_window`
  ADD PRIMARY KEY (`context_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `frequent_terms`
--
ALTER TABLE `frequent_terms`
  ADD PRIMARY KEY (`search_term`);

--
-- Indexes for table `risk_levels`
--
ALTER TABLE `risk_levels`
  ADD PRIMARY KEY (`risk_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `risk_id` (`risk_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `context_window`
--
ALTER TABLE `context_window`
  MODIFY `context_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `risk_levels`
--
ALTER TABLE `risk_levels`
  MODIFY `risk_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `context_window`
--
ALTER TABLE `context_window`
  ADD CONSTRAINT `context_window_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`risk_id`) REFERENCES `risk_levels` (`risk_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
