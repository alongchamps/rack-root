-- Create "ItemDevTypeAssoc" table
CREATE TABLE `ItemDevTypeAssoc` (`id` integer NOT NULL, `itemId` integer NULL, `deviceTypeId` integer NULL, PRIMARY KEY (`id`), CONSTRAINT `0` FOREIGN KEY (`deviceTypeId`) REFERENCES `deviceTypes` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT `1` FOREIGN KEY (`itemId`) REFERENCES `items` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION);
-- Create "deviceTypes" table
CREATE TABLE `deviceTypes` (`id` integer NOT NULL, `name` varchar NULL, PRIMARY KEY (`id`));
-- Create index "ix_deviceTypes_id" to table: "deviceTypes"
CREATE INDEX `ix_deviceTypes_id` ON `deviceTypes` (`id`);
-- Create index "ix_deviceTypes_name" to table: "deviceTypes"
CREATE INDEX `ix_deviceTypes_name` ON `deviceTypes` (`name`);
-- Create "subnets" table
CREATE TABLE `subnets` (`id` integer NOT NULL, `name` varchar NULL, `vlan` integer NULL, `classification` varchar NULL, `network` varchar NULL, `subnetMaskBits` integer NULL, `gateway` varchar NULL, PRIMARY KEY (`id`));
-- Create index "ix_subnets_name" to table: "subnets"
CREATE INDEX `ix_subnets_name` ON `subnets` (`name`);
-- Create index "ix_subnets_id" to table: "subnets"
CREATE INDEX `ix_subnets_id` ON `subnets` (`id`);
-- Create "items" table
CREATE TABLE `items` (`id` integer NOT NULL, `name` varchar NULL, `description` varchar NULL, `serialNumber` varchar NULL, `purchaseDate` datetime NULL, `warrantyExpiration` datetime NULL, `notes` varchar NULL, `deviceTypeId` integer NULL, PRIMARY KEY (`id`), CONSTRAINT `0` FOREIGN KEY (`deviceTypeId`) REFERENCES `deviceTypes` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION);
-- Create index "ix_items_name" to table: "items"
CREATE INDEX `ix_items_name` ON `items` (`name`);
-- Create index "ix_items_id" to table: "items"
CREATE INDEX `ix_items_id` ON `items` (`id`);
