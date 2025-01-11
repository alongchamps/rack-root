from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .database import get_db, Subnet
from .validation_subnet import SubnetCreate, SubnetUpdateGateway
from ipaddress import ip_network,ip_address

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

# create a new subnet and make sure we don't overlap with any existing ranges already saved
def create_subnet(subnet: SubnetCreate, db: Session = Depends(get_db)):
    db_subnet = Subnet(**subnet.model_dump())

    # 2 data validations before we save the network details to the database

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
    try:
        db.add(db_subnet)
        db.commit()
        db.refresh(db_subnet)
    except:
        raise HTTPException(status_code=500, detail="Issue saving the record to the database.")

    return db_subnet

# delete a single subnet
def delete_subnet(subnet_id: int, db: Session = Depends(get_db)):
    db_subnet_delete = db.query(Subnet).filter(Subnet.id == subnet_id).delete(synchronize_session="auto")
    db.commit()

    if db_subnet_delete == 0:
        raise HTTPException(status_code=404, detail="A subnet with that ID was not found")

    return 0

# configure the gateway on a given network. This method can be used to clear a gateway, set a gateway,
# or update a gateway - all in one function
def set_gateway(subnet_id: int, subnet: SubnetUpdateGateway, db: Session = Depends(get_db)):

    # look for our database record
    db_subnet = db.query(Subnet).filter(Subnet.id == subnet_id).first()

    if db_subnet is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # if a gateway is provided, check that provided gateway is actually in this network
    if len(subnet.gateway) > 0:
        
        valid_gateway = gateway_in_subnet(subnet.gateway, db_subnet.network, db_subnet.subnetMaskBits)

        if valid_gateway == False:
            raise HTTPException(status_code=500, detail="Provided gateway is not in that subnet range.")

    # there is no else here because if the gateway is empty, the code/database will accept it and clear the record

    # update the record
    try:
        items_affected = db.query(Subnet).filter(Subnet.id == subnet_id).update(dict(**subnet.model_dump()))
        db.commit()
    except:
        raise HTTPException(status_code=500, detail="Issue setting the gateway")

    return 0

# returns true or false if the gateway is in the provided network
def gateway_in_subnet(gateway: str, subnet: str, subnet_mask: int):

    # error handling here makes sure we can cast the provided inputs
    # to the actual ip_address and ip_network types
    try:
        gateway_object = ip_address(gateway)
    except:
        raise HTTPException(status_code=500, detail="Issue converting provided input to an IP address")

    try:
        network_object = ip_network("{0}/{1}".format(subnet, subnet_mask))
    except:
        raise HTTPException(status_code=500, detail="Issue converting provided input details to a network")
    
    return gateway_object in network_object.hosts()
