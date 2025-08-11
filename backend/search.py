from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy_searchable import search

from .database import getDb, Item

def searchItems(itemSearch: str, db: Session = Depends(getDb)):
    tsQuery = func.plainto_tsquery('english', itemSearch)

    query = (
        select(Item)
        .where(Item.item_search_vector.op('@@')(tsQuery))
        .order_by(func.ts_rank_cd(Item.item_search_vector, tsQuery).desc())
    )

    results = db.execute(query).scalars().unique().all()
    return results

# find all items that match the search term
# def searchItems(itemSearch: str, db: Session = Depends(getDb)):

    # searchQuery = func.to_tsquery(itemSearch)
    # searchVector = func.to_tsvector("english",
    #         func.concat_ws(
    #         ' ',
    #         Item.name,
    #         Item.description,
    #         Item.serialNumber,
    #         Item.notes
    #     )
    # )

    # itemArray = db.query(Item).filter(Item.itemSearchVector.op("@@")(searchQuery)).all()
    # Article.query.search("Finland").limit(5).all()
    # results = Videos.query.filter(Video.description.match(term)).all()
    # itemArray = db.query(Item).filter(Item.itemSearchVector.op("@@")(itemSearch)).all()

    # query = search(select(Item), itemSearch)
    # itemArray = db.scalars(query).all()

    # return itemArray

# find all networks that match the search term
# def searchNetworks():
#     return 0

# find all dhcp ranges that match the search term
# def searchDhcpRanges():
#     return 0



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
