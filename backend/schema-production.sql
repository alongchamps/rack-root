-- Create "deviceTypes" table
CREATE TABLE `deviceTypes` (`id` integer NOT NULL, `name` varchar NULL, PRIMARY KEY (`id`));
-- Create index "ix_deviceTypes_name" to table: "deviceTypes"
CREATE INDEX `ix_deviceTypes_name` ON `deviceTypes` (`name`);
-- Create index "ix_deviceTypes_id" to table: "deviceTypes"
CREATE INDEX `ix_deviceTypes_id` ON `deviceTypes` (`id`);
-- Create "items" table
CREATE TABLE `items` (`id` integer NOT NULL, `name` varchar NULL, `description` varchar NULL, `serialNumber` varchar NULL, `purchaseDate` datetime NULL, `warrantyExpiration` datetime NULL, `notes` varchar NULL, `deviceTypeId` integer NULL, PRIMARY KEY (`id`), CONSTRAINT `0` FOREIGN KEY (`deviceTypeId`) REFERENCES `deviceTypes` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION);
-- Create index "ix_items_name" to table: "items"
CREATE INDEX `ix_items_name` ON `items` (`name`);
-- Create index "ix_items_id" to table: "items"
CREATE INDEX `ix_items_id` ON `items` (`id`);
-- Create "subnets" table
CREATE TABLE `subnets` (`id` integer NOT NULL, `name` varchar NOT NULL, `vlan` integer NOT NULL, `subnetMaskBits` integer NOT NULL, `classification` text NOT NULL, `network` text NOT NULL, 'gateway' varchar NULL, PRIMARY KEY (`id`));
-- Create index "ix_subnets_id" to table: "subnets"
CREATE INDEX `ix_subnets_id` ON `subnets` (`id`);
-- Create index "ix_subnets_name" to table: "subnets"
CREATE INDEX `ix_subnets_name` ON `subnets` (`name`);
