# Rack-Root - The Home Lab Inventory Project
This is my first modern web app (ever) and I'm using it to help me learn how to put this kind of project together. This will be for tracking the inventory in my home lab with a persistent back end database. I'm writing this primarily for my own usage and portfolio.

I'm keeping the scope small for now, at least to make this manageable. We'll see where this ends up going.

# Documentation
I gathered some notes on how I initialized this project over in the [docs](docs.md) file.

I also started to put together a [design document](design.md) to help me stay on track.

# Front End
Frontend - Vue and Vuetify with package management from npm.

# Back End
Backend - FastAPI project with testing for all REST endpoints.

Database - local SQLite file.

# Features
* Track the inventory and relationships of hardware/VMs in your home lab. Everything from racks to servers to NAS devices to the hard drives inside are intended to be in scope. Of course, that's not a complete list of object types.
* For your network(s)/VLANs, track the networks you're using, what they're for, and IPAM allocations. For example, my home network only has 50 IPs in the DHCP scope and all the other IPs are available for static assignment.
* Full text search of any field in order to locate resources quickly. Get an alert for a hard drive with serial `B4T9X2H8J6` having problems? Find out where it is quickly and identify your warranty status.
* And speaking of warranty status, this can track when you bought hardware and when the warranty runs out.

# Future ideas
*This is pretty much a wish list*
* Add custom object types (easy, needs flexible code)
* IPAM visualization (easy-ish, depends on what I can use for visualization)
* Rack visualization (easy-ish, same as IPAM viz)
* Network device relationship mapping

# Out of scope
*I'm not planning to go after these things at this time*
* External database support, doesn't make sense if SQLite can do everything I need
* Automatic device discovery/mapping - It would be really cool to just point at an IP with credentials and slurp up all the data, but that seems too complicated for this project.
