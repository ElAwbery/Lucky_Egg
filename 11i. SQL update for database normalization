-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Feb 21, 2019 at 10:24 PM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `Pokemon`
--

-- --------------------------------------------------------

--
-- Table structure for table `pokemon_family`
--

CREATE TABLE `pokemon_family` (
  `UID` int(11) NOT NULL,
  `candies` int(11) NOT NULL DEFAULT '0',
  `baby` int(11) DEFAULT NULL,
  `first_stage` int(11) DEFAULT NULL,
  `second_stage` int(11) DEFAULT NULL,
  `third_stage` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pokemon_family`
--

INSERT INTO `pokemon_family` (`UID`, `candies`, `baby`, `first_stage`, `second_stage`, `third_stage`) VALUES
(1, 34, NULL, 7, 8, 9),
(2, 0, 172, 25, 26, NULL),
(3, 0, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `pokemon_species`
--

CREATE TABLE `pokemon_species` (
  `UID` int(11) NOT NULL,
  `family` int(11) NOT NULL COMMENT 'Must be a family UID from Families table',
  `name` text NOT NULL,
  `count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pokemon_species`
--

INSERT INTO `pokemon_species` (`UID`, `family`, `name`, `count`) VALUES
(7, 1, 'Squirtle', 5),
(8, 1, 'Wortortle', 2),
(9, 1, 'Blastoise', 1),
(25, 2, 'Pikachu', 0),
(26, 2, 'Raichu', 0),
(172, 2, 'Pichu', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pokemon_family`
--
ALTER TABLE `pokemon_family`
  ADD PRIMARY KEY (`UID`),
  ADD KEY `first_stage` (`first_stage`) USING BTREE,
  ADD KEY `second_stage` (`second_stage`) USING BTREE,
  ADD KEY `third_stage` (`third_stage`) USING BTREE,
  ADD KEY `baby` (`baby`) USING BTREE;

--
-- Indexes for table `pokemon_species`
--
ALTER TABLE `pokemon_species`
  ADD PRIMARY KEY (`UID`),
  ADD KEY `family` (`family`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pokemon_family`
--
ALTER TABLE `pokemon_family`
  MODIFY `UID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pokemon_family`
--
ALTER TABLE `pokemon_family`
  ADD CONSTRAINT `pokemon_family_ibfk_1` FOREIGN KEY (`baby`) REFERENCES `pokemon_species` (`UID`),
  ADD CONSTRAINT `pokemon_family_ibfk_2` FOREIGN KEY (`first_stage`) REFERENCES `pokemon_species` (`UID`),
  ADD CONSTRAINT `pokemon_family_ibfk_3` FOREIGN KEY (`second_stage`) REFERENCES `pokemon_species` (`UID`),
  ADD CONSTRAINT `pokemon_family_ibfk_4` FOREIGN KEY (`third_stage`) REFERENCES `pokemon_species` (`UID`);

--
-- Constraints for table `pokemon_species`
--
ALTER TABLE `pokemon_species`
  ADD CONSTRAINT `pokemon_species_ibfk_1` FOREIGN KEY (`family`) REFERENCES `pokemon_family` (`UID`);
