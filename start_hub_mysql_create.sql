CREATE TABLE `innovator` (
	`first_name` varchar(50) NOT NULL,
	`last_name` varchar(50) NOT NULL,
	`email_id` varchar(50) NOT NULL,
	`password` varchar(255) NOT NULL,
	`mobile_no` varchar(15) NOT NULL,
	`qualification` varchar(50) NOT NULL,
	`linkedin` varchar(255) NOT NULL
);

CREATE TABLE `investor` (
	`first_name` varchar(50) NOT NULL,
	`last_name` varchar(50) NOT NULL,
	`email_id` varchar(50) NOT NULL,
	`password` varchar(255) NOT NULL,
	`mobile_no` varchar(15) NOT NULL,
	`company` varchar(50) NOT NULL,
	`linkedin` varchar(255) NOT NULL,
	`pancard` varchar(15) NOT NULL
);

CREATE TABLE `mentor` (
	`first_name` varchar(50) NOT NULL,
	`last_name` varchar(50) NOT NULL,
	`email_id` varchar(50) NOT NULL,
	`password` varchar(255) NOT NULL,
	`mobile_no` varchar(15) NOT NULL,
	`company` varchar(50) NOT NULL,
	`linkedin` varchar(255) NOT NULL,
	`qualification` varchar(50) NOT NULL,
	`specialization` varchar(255) NOT NULL
);

CREATE TABLE `organization` (
	`email_id` varchar(50) NOT NULL,
	`password` varchar(255) NOT NULL,
	`mobile_no` varchar(15) NOT NULL,
	`company` varchar(50) NOT NULL,
	`linkedin` varchar(255) NOT NULL,
	`pancard` varchar(15) NOT NULL
);

CREATE TABLE `idea_post` (
	`title` varchar(100) NOT NULL,
	`author` varchar(100) NOT NULL,
	`description` TEXT(600) NOT NULL,
	`upvotes` INT(10) NOT NULL,
	`comment` TEXT(100) NOT NULL,
	`sub_title` TEXT(100) NOT NULL,
	`date` DATE(3) NOT NULL
);

CREATE TABLE `blogs` (
	`title` varchar(100) NOT NULL,
	`author` varchar(100) NOT NULL,
	`description` TEXT(600) NOT NULL,
	`likes` INT(10) NOT NULL,
	`date` DATE(3) NOT NULL
);

CREATE TABLE `chatroom` (
	`sender` varchar(100) NOT NULL,
	`receiver` varchar(100) NOT NULL,
	`message` TEXT(600) NOT NULL,
	`date` TIMESTAMP NOT NULL
);








