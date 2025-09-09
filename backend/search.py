# The code in this file effectively just runs the search queries on the database
# for each of the given types: Item, Subnet, and DhcpRange. Future searches
# should be added here and called in a similar way from main.py.

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy_searchable import search

from .database import getDb, Item, Subnet, DhcpRange

# Find all Items that match our search query
def searchItems(itemSearch: str, db: Session = Depends(getDb)):
    tsQuery = func.plainto_tsquery('english', itemSearch)

    query = (
        select(Item)
        .where(Item.item_search_vector.op('@@')(tsQuery))
        .order_by(func.ts_rank_cd(Item.item_search_vector, tsQuery).desc())
    )

    results = db.execute(query).scalars().unique().all()
    return results

# Find all Networks that match our search query
def searchNetworks(networkSearch: str, db: Session = Depends(getDb)):
    tsQuery = func.plainto_tsquery('english', networkSearch)

    query = (
        select(Subnet)
        .where(Subnet.network_search_vector.op('@@')(tsQuery))
        .order_by(func.ts_rank_cd(Subnet.network_search_vector, tsQuery).desc())
    )

    results = db.execute(query).scalars().unique().all()
    return results

# Find all DHCP ranges that match our search query
def searchDhcpRanges(dhcpSearch: str, db: Session = Depends(getDb)):
    tsQuery = func.plainto_tsquery('english', dhcpSearch)

    query = (
        select(DhcpRange)
        .where(DhcpRange.dhcp_range_search_vector.op('@@')(tsQuery))
        .order_by(func.ts_rank_cd(DhcpRange.dhcp_range_search_vector, tsQuery).desc())
    )

    results = db.execute(query).scalars().unique().all()    
    return results

# TODO
# Should I have a search function for IP records? They would need to point back to the network
# details page, but being able to find out where a.b.c.d is used (if anywhere) is useful
# Side effect: 


# The notes below went into my functionality for this feature and I kept it here in case there's something I forgot

# search box functionality
# - - - - - - - - - - - - 

# purpose: allow users to find $records from the database based on matching text

# scope:
#     items
#         search in the fields ['name', 'description', 'serial number', 'notes']
#     networks
#         search in the fields ['network', 'vlan', 'classification']
#     dhcp ranges
#         search in the field ['name']
#     TBD: searching by ['IP Address'] and link to /networks/:id?

# considerations:
#     handling spaces between frontend/backend
#         Vuetify seems to put `+` in place of spaces? TBD how this looks on the backend, does something handle this automatically for me
#     I fully expect SQLAlchemy has some kind of search function where I can say something like:
#         select * from Item where name, description, serial number, notes match $inputText
#     backend API:
#         should I make one API result under "/search?q=searchTerms"?
#             if so, what do I set that response model at

# results page:
#     one table per item type
#         this would be scalable 
#         allows me to show the relevant information from all search results

#         for items, this should go to the SingleItem.vue page
#         for network results, this should go to the SingleNetwork.vue page
#         for DHCP networks, this should go to the SingleNetwork.vue page
#         for IP addresses, go to SingleNetwork.vue page or a page that renders IP address details?

# testing
# items
#   find 0 items
#   find 1 item
#   find 2+ items
# 
# networks
#   find 0 networks
#   find 1 network
#   find 2+ networks
# 
# DHCP ranges
#   find 0 DHCP ranges
#   find 1 DHCP range
#   find 2+ DHCP ranges
# 

# links:
#     items -> /items/:id
#     networks -> /networks/:id
#     dhcp ranges -> /networks/:id
