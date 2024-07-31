-- Adding a new column for chassis number
ALTER TABLE `car_data`
ADD COLUMN `chassis_number` VARCHAR(17);

-- Updating the table with guessed chassis numbers
UPDATE `car_data` SET `chassis_number` = 'VF1BB3FZ9EZ000001' WHERE `id` = 1;
UPDATE `car_data` SET `chassis_number` = 'ZAM57RTA4E1112345' WHERE `id` = 2;
UPDATE `car_data` SET `chassis_number` = 'W0L0ZCF6841123456' WHERE `id` = 3;
UPDATE `car_data` SET `chassis_number` = 'JT2BG22K8T1000001' WHERE `id` = 4;
UPDATE `car_data` SET `chassis_number` = '3N1AB7AP5FL000001' WHERE `id` = 5;
UPDATE `car_data` SET `chassis_number` = 'W0L0XCF6852112345' WHERE `id` = 6;
UPDATE `car_data` SET `chassis_number` = 'WBA4C9C50FG000001' WHERE `id` = 7;
UPDATE `car_data` SET `chassis_number` = 'WDDGF8ABXDF000001' WHERE `id` = 8;
UPDATE `car_data` SET `chassis_number` = 'WP1AA2A54CLA00001' WHERE `id` = 9;
UPDATE `car_data` SET `chassis_number` = 'SALWR2VF1FA000001' WHERE `id` = 10;



-- Adding a new column for email
ALTER TABLE `car_data`
ADD COLUMN `email` VARCHAR(255);

-- Updating the table with guessed email addresses
UPDATE `car_data` SET `email` = 'owner1@example.com' WHERE `id` = 1;
UPDATE `car_data` SET `email` = 'owner2@example.com' WHERE `id` = 2;
UPDATE `car_data` SET `email` = 'owner3@example.com' WHERE `id` = 3;
UPDATE `car_data` SET `email` = 'owner4@example.com' WHERE `id` = 4;
UPDATE `car_data` SET `email` = 'owner5@example.com' WHERE `id` = 5;
UPDATE `car_data` SET `email` = 'owner6@example.com' WHERE `id` = 6;
UPDATE `car_data` SET `email` = 'owner7@example.com' WHERE `id` = 7;
UPDATE `car_data` SET `email` = 'owner8@example.com' WHERE `id` = 8;
UPDATE `car_data` SET `email` = 'owner9@example.com' WHERE `id` = 9;
UPDATE `car_data` SET `email` = 'owner10@example.com' WHERE `id` = 10;



-- Adding new columns for irregularities and irregularities reason
ALTER TABLE `car_data`
ADD COLUMN `irregularities` BOOLEAN DEFAULT FALSE,
ADD COLUMN `irregularities_reason` TEXT;

-- Example updates with irregularities
UPDATE `car_data` SET `irregularities` = TRUE, `irregularities_reason` = 'Expired registration' WHERE `id` = 1;
UPDATE `car_data` SET `irregularities` = FALSE WHERE `id` = 2;
UPDATE `car_data` SET `irregularities` = TRUE, `irregularities_reason` = 'Outstanding fines' WHERE `id` = 3;
UPDATE `car_data` SET `irregularities` = FALSE WHERE `id` = 4;
UPDATE `car_data` SET `irregularities` = TRUE, `irregularities_reason` = 'Uninsured vehicle' WHERE `id` = 5;
