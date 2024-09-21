# Rack Root Design Document

I'm writing this design doc to give me practice in such a thing and also get my thoughts on digital paper in some structured format. I'll try to keep this in line with what's actually in the code, and we'll see how good I am at that!

The goal for Rack Root is two fold - one side is teaching myself about web development and software design, the other is to actually keep track of all the devices in my home lab.

This app should be portable enough to run in a single docker container and I might add features to that layer at some point in the future. Notably, persistence of the data is in a local sqlite database file in the `/backend` directory.

# Data and relationships

Every item in the inventory has an id, name, and type. All the other fields are optional.

The types database will be pre-seeded with a number of options and more types can be added in the Settings page.

Relationship examples:

An inventory item can have 0..n IP addresses.

An IPAM network can have 0..n IP addresses.

A DHCP range has a starting IP, ending IP, and associated network.

# Database table design

I'm going to use the basic functionality of the SQLite database to auto-assign IDs and relate certain database rows to each other.

### Inventory Items

This is the central table in the database.

Table name: 
- id - auto-assigned by the database
- name - device name
- type - foreign key over to the type database
- serialNumber - string
- purchaseDate - date
- warrantyExpiration - date
- operatingSystem - string
- notes - freeform varchar, up to 500 characters

### Type database

Goes with the inventory database to track different hardware types.

Table name:
- id - auto-assigned by the database
- name - string, visual display name of the item type

Sample types:
1. access point
1. desktop
1. external hard drive
1. firewall
1. gateway
1. hard disk
1. laptop
1. modem
1. monitor
1. network switch
1. raspberry pi
1. router
1. server
1. ssd

### Relationship
Table name: 
- id - auto-assigned by the database
- oneSide - foreign key over to inventory database
- otherSide - foreign key over to inventory database
- relationshipType - string, parent/child or peer 

### IPAM Networks
Table name: 
- id - auto-assigned by the database
- name - string, a display label for the network
- network - string, the IP portion of the network, such as `192.168.12.0`
- subnetMask - int, the number of bits in the subnet mask, such as `24`
- gateway - string, the gateway address for this network

### IPAM Records
Table name: 
- id - auto-assigned by the database
- deviceId - foreign key over to the inventory table
- typeOfIP - bmc, primary, secondary, etc.
- associatedNetwork - foreign key over to the IPAM Networks table
- ipAddress - string
- dhcpReserved - bool, whether the IP is reserved in DHCP by some mechanism
- zone - type of zone such as intranet, extranet, DMZ, isolated

### DHCP Range
table name:
- id - auto-assigned
- networkId - foreign key to IPAM networks table
- start IP - string, starting IP
- end IP - string, ending IP

#### Settings page

On the settings page, you can add more device types.

# Database Functionality

todo: import/export functionality with a CSV

todo: dump all existing data (or make that an input on the import CSV page?)
