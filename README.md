# Rack Root - The Home Lab inventory project
*Just so I can learn some web development*

This is my first modern web app (ever) and I'm using it to help me learn how to put this kind of project together. My use case for this is tracking the inventory in my home lab, including basic IPAM features.

I'm writing this primarily for my own usage and portfolio, so I plan to keep this to a pretty small scope. If you end up using this at home to keep track of your stuff, let me know!

# Documentation
I gathered some notes on how I initialized this project over in the [docs](docs.md) file.

I also started to put together a [design document](design.md) to help me stay on track.

# Front End
Frontend - Vue and Vuetify with package management from npm.

# Back End
Backend - FastAPI project with testing for all REST endpoints.

Database - postgres container

# Features
* Track the inventory and relationships of hardware/VMs in your home lab. Everything from racks to servers to NAS devices to the hard drives inside are intended to be in scope. Of course, that's not a complete list of object types.
* For your network(s)/VLANs, track the networks you're using, what they're for, and IPAM allocations. For example, my home network only has 50 IPs in the DHCP scope and all the other IPs are available for static assignment or Kubernetes ingress DHCP ranges.
* Full text search of any field in order to locate resources quickly. Get an alert for a hard drive with serial `B4T9X2H8J6` having problems? Find out where it is quickly and identify your warranty status.
* And speaking of warranty status, this can track when you bought hardware and when the warranty runs out.

# Future ideas
*This is pretty much a wish list*
* IPAM visualization (easy-ish, depends on what I can use for visualization)
* Device to network visualizations

# Out of scope
*I'm not planning to go after these things at this time*
* Automatic device discovery/mapping - It would be really cool to just point at an IP with credentials and slurp up all the data, but that's beyond the scope of this project
