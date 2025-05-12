# Rack Root - The Home Lab inventory project
*aka, what happens when Aaron decides to learn full stack web development and needs a project*

Rack Root is my first modern web app, put together with Vue/Vuetify for the frontend, FastAPI for the backend, and a postgres contianer for the database. The primary goal of this project is to track the inventory of devices and networks in my home lab, so all of the functionality of Rack Root is based on that. As a side effect, this project is also an exercise for me to learn full stack web development and have that in my portfolio.

# Documentation
I gathered some notes on how I initialized this project over in [docs](docs.md).

# Features
* Track the inventory and relationships of hardware/VMs in your home lab. Everything from racks to servers to NAS devices to the hard drives inside are intended to be in scope. Of course, that's not a complete list of object types and you can add as many device types as you want.
* For your network(s)/VLANs, track the networks you're using, what they're for, and IPAM allocations. For example, my home network only has 50 IPs in the DHCP scope and all the other IPs are available for static assignment or Kubernetes ingress DHCP ranges
* And speaking of warranty status, this can track when you bought hardware and when the warranty runs out

# Future ideas
*This is pretty much a wish list*
* Text search to the database that will look in all available fields for the search terms
* IPAM visualization (easy-ish, depends on what I can use for visualization)
* Device to network visualizations

# Out of scope
*I'm not planning to go after these things at this time*
* Automatic device discovery/mapping - It would be really cool to just point at an IP with credentials and slurp up all the data, but that's beyond the scope of this project
