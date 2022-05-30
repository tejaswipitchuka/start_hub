CREATE TABLE `innovator` (
	`first_name` varchar(50) NULL,
	`last_name` varchar(50) NULL,
	`email_id` varchar(50) NULL,
	`password` varchar(255) NULL,
	`mobile_no` varchar(15) NULL,
	`qualification` varchar(50) NULL,
	`linkedin` varchar(255) NULL
);

CREATE TABLE `investor` (
	`first_name` varchar(50) NULL,
	`last_name` varchar(50) NULL,
	`email_id` varchar(50) NULL,
	`password` varchar(255) NULL,
	`mobile_no` varchar(15) NULL,
	`company` varchar(50) NULL,
	`linkedin` varchar(255) NULL,
	`pancard` varchar(15) NULL
);

CREATE TABLE `mentor` (
	`first_name` varchar(50) NULL,
	`last_name` varchar(50) NULL,
	`email_id` varchar(50) NULL,
	`password` varchar(255) NULL,
	`mobile_no` varchar(15) NULL,
	`company` varchar(50) NULL,
	`linkedin` varchar(255) NULL,
	`qualification` varchar(50) NULL,
	`specialization` varchar(255) NULL
);

CREATE TABLE `organization` (
	`email_id` varchar(50) NULL,
	`password` varchar(255) NULL,
	`mobile_no` varchar(15) NULL,
	`company` varchar(50) NULL,
	`linkedin` varchar(255) NULL,
	`pancard` varchar(15) NULL
);

CREATE TABLE `idea_post` (
	`title` varchar(100) NULL,
	`author` varchar(100) NULL,
	`description` TEXT(600) NULL,
	`upvotes` INT(10) NULL,
	`comment` TEXT(100) NULL,
	`subtitle` TEXT(100) NULL,
	`date` DATE NULL
);

CREATE TABLE `blogs` (
	`title` varchar(100) NULL,
	`author` varchar(100) NULL,
	`description` TEXT(600) NULL,
	`likes` INT(10) NULL,
	`date` DATE NULL
);

CREATE TABLE `chatroom` (
	`sender` varchar(100) NULL,
	`receiver` varchar(100) NULL,
	`message` TEXT(600) NULL,
	`date` TIMESTAMP NULL
);








