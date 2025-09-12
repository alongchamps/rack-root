table "devicetype" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "name" {
    null = false
    type = character_varying
  }
  primary_key {
    columns = [column.id]
  }
  index "ix_devicetype_id" {
    columns = [column.id]
  }
}
table "dhcprange" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "name" {
    null = false
    type = character_varying
  }
  column "description" {
    null = true
    type = character_varying
  }
  column "startIp" {
    null = false
    type = character_varying
  }
  column "endIp" {
    null = false
    type = character_varying
  }
  column "subnetId" {
    null = false
    type = integer
  }
  column "ipRecordId" {
    null = true
    type = integer
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "dhcprange_ipRecordId_fkey" {
    columns     = [column.ipRecordId]
    ref_columns = [table.iprecord.column.id]
    on_update   = NO_ACTION
    on_delete   = CASCADE
  }
  foreign_key "dhcprange_subnetId_fkey" {
    columns     = [column.subnetId]
    ref_columns = [table.subnet.column.id]
    on_update   = NO_ACTION
    on_delete   = CASCADE
  }
  index "ix_dhcprange_id" {
    columns = [column.id]
  }
}
table "iprecord" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "status" {
    null = false
    type = character_varying
  }
  column "ipAddress" {
    null = false
    type = character_varying
  }
  column "subnetId" {
    null = true
    type = integer
  }
  column "dhcpRangeId" {
    null = true
    type = integer
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "iprecord_dhcpRangeId_fkey" {
    columns     = [column.dhcpRangeId]
    ref_columns = [table.dhcprange.column.id]
    on_update   = NO_ACTION
    on_delete   = NO_ACTION
  }
  foreign_key "iprecord_subnetId_fkey" {
    columns     = [column.subnetId]
    ref_columns = [table.subnet.column.id]
    on_update   = NO_ACTION
    on_delete   = CASCADE
  }
  index "ix_iprecord_id" {
    columns = [column.id]
  }
}
table "item" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "name" {
    null = false
    type = character_varying
  }
  column "description" {
    null = true
    type = character_varying
  }
  column "serial_number" {
    null = true
    type = character_varying
  }
  column "notes" {
    null = true
    type = character_varying
  }
  column "purchaseDate" {
    null = true
    type = timestamp
  }
  column "warrantyExpiration" {
    null = true
    type = timestamp
  }
  column "deviceTypeId" {
    null = false
    type = integer
  }
  column "item_search_vector" {
    null = true
    type = tsvector
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "item_deviceTypeId_fkey" {
    columns     = [column.deviceTypeId]
    ref_columns = [table.devicetype.column.id]
    on_update   = NO_ACTION
    on_delete   = CASCADE
  }
  index "ix_item_id" {
    columns = [column.id]
  }
  index "ix_item_item_search_vector" {
    columns = [column.item_search_vector]
    type    = GIN
  }
  index "ix_item_search_vector" {
    columns = [column.item_search_vector]
    type    = GIN
  }
}
table "subnet" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "name" {
    null = false
    type = character_varying
  }
  column "vlan" {
    null = false
    type = integer
  }
  column "classification" {
    null = false
    type = character_varying
  }
  column "network" {
    null = false
    type = character_varying
  }
  column "subnetMaskBits" {
    null = false
    type = integer
  }
  column "dhcpRangeId" {
    null = true
    type = integer
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "subnet_dhcpRangeId_fkey" {
    columns     = [column.dhcpRangeId]
    ref_columns = [table.dhcprange.column.id]
    on_update   = NO_ACTION
    on_delete   = NO_ACTION
  }
  index "ix_subnet_id" {
    columns = [column.id]
  }
}
schema "public" {
  comment = "standard public schema"
}
