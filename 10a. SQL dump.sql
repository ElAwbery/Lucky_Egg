-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Feb 03, 2019 at 09:11 PM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `Pokemon`
--

-- --------------------------------------------------------

--
-- Table structure for table `Pokemon`
--

CREATE TABLE `Pokemon` (
  `Name` text NOT NULL,
  `First stage` text NOT NULL,
  `Second stage` text NOT NULL,
  `Third stage` text NOT NULL,
  `Count` int(11) NOT NULL,
  `Candies` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Pokemon`
--

INSERT INTO `Pokemon` (`Name`, `First stage`, `Second stage`, `Third stage`, `Count`, `Candies`) VALUES
('Blastoise', 'Squirtle', 'Wortortle', 'Blastoise', 6, 5),
('Pichu', 'Pichu', 'Pikachu', 'Raichu', 0, 0),
('Pikachu', 'Pichu', 'Pikachu', 'Raichu', 0, 0),
('Raichu', 'Pichu', 'Pikachu', 'Raichu', 0, 0),
('Squirtle', 'Squirtle', 'Wortortle', 'Blastoise', 2, 5),
('Wortortle', 'Squirtle', 'Wortortle', 'Blastoise', 6, 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Pokemon`
--
ALTER TABLE `Pokemon`
  ADD PRIMARY KEY (`Name`(255));
