from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .database import get_db, Subnet
from .validation_subnet import SubnetCreate
from ipaddress import ip_network

# get all subnets from the database
def read_all_subnets(request: Request, db: Session = Depends(get_db)):
    db_subnets = db.query(Subnet)
    return db_subnets

# get data for one subnet
def read_single_subnet(subnet_id: int, db: Session = Depends(get_db)):
    db_subnet = db.query(Subnet).filter(Subnet.id == subnet_id).first()
    if db_subnet is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_subnet

# create a new subnet
def create_subnet(subnet: SubnetCreate, db: Session = Depends(get_db)):
    db_subnet = Subnet(**subnet.model_dump())

    # data validation before we save the network details to the database

    # make sure we got an IP network, if any exception is thrown, we probably have bad data
    # for example, host bits are set (if network = 192.168.12.10 and subnet mask is /24, the network input really should be 192.168.12.0)
    try:
        validate_network = ip_network(db_subnet.network + "/" + str(db_subnet.subnetMaskBits))
    except:
        raise HTTPException(status_code=400, detail="Invalid network provided")

    # make sure the new range doesn't overlap with anything we already have
    all_networks = db.query(Subnet)
    for n in all_networks:
        tmp_network = ip_network(str(n.network) + "/" + str(n.subnetMaskBits))
        if tmp_network.overlaps(validate_network):
            raise HTTPException(status_code=400, detail="Networks must be unique.")

    # if we get down here, actually save the data
    db.add(db_subnet)
    db.commit()
    db.refresh(db_subnet)
    return db_subnet

# delete a single subnet
def delete_subnet(subnet_id: int, db: Session = Depends(get_db)):
    db_subnet_delete = db.query(Subnet).filter(Subnet.id == subnet_id).delete(synchronize_session="auto")
    db.commit()

    if db_subnet_delete == 0:
        raise HTTPException(status_code=404, detail="A subnet with that ID was not found")

    return 0
