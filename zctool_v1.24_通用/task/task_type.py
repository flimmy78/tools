#!/usr/bin/python

##task type, id from 2
load_service = 9
load_config = 10
query_server_room = 11
create_server_room = 12
modify_server_room = 13
delete_server_room = 14

query_server_rack = 15
create_server_rack = 16
modify_server_rack = 17
delete_server_rack = 18

query_server = 19
add_server = 20
modify_server = 21
remove_server = 22

query_service_type = 23
query_service_group = 24
query_service = 25
modify_service = 26

create_host = 27
delete_host = 28
modify_host = 29
start_host = 30
stop_host = 31
halt_host = 32
restart_host=33

query_iso_image = 35
upload_iso_image = 36
modify_iso_image = 37
delete_iso_image = 38

query_disk_image = 39
create_disk_image = 40
delete_disk_image = 41
modify_disk_image = 42
read_disk_image = 43

insert_media = 44
change_media = 45
eject_media = 46

query_address_pool = 110
create_address_pool = 111
delete_address_pool = 112
add_address_resource = 113
remove_address_resource = 114
query_address_resource = 115

query_port_pool = 116
create_port_pool = 117
delete_port_pool = 118
add_port_resource = 119
remove_port_resource = 120
query_port_resource = 121

query_compute_pool = 122
create_compute_pool = 123
delete_compute_pool = 124
add_compute_resource = 125
remove_compute_resource = 126
query_compute_resource = 127

#storage pool
query_storage_pool = 128
create_storage_pool = 129
delete_storage_pool = 130
add_storage_resource = 131
remove_storage_resource = 132
query_storage_resource = 133

query_resource_pool = 134

query_host = 135
query_host_info = 136

#port pool
query_port_pool = 137
create_port_pool = 138
delete_port_pool = 139
add_port_resource = 140
remove_port_resource = 141
query_port_resource = 142

create_compute_resource = 143

query_forwarder_summary = 144
query_forwarder = 145
set_forwarder_status = 146
get_forwarder = 147

#address pool
query_address_pool=148
create_address_pool=149
delete_address_pool=150
add_address_resource=151
remove_address_resource=152
query_address_resource=153


#domain bind
bind_domain = 154
unbind_domain = 155
query_domain_summary = 156
query_domain_name = 157
get_bound_domain = 158

#balancer
query_balancer_detail = 159
query_load_balancer = 160
query_balancer_summary = 161

delete_compute_pool = 162
modify_compute_pool = 163

add_forwarder = 164
remove_forwarder = 165

modify_storage_pool = 166

disable_load_balancer = 167
delete_load_balancer = 168
attach_address = 169
detach_address = 170
get_load_balancer = 171

create_load_balancer = 172
add_balancer_node = 173
remove_balancer_node = 174
modify_balancer_node = 175
enable_load_balancer = 176
#disk
attach_disk = 177
detach_disk = 178

#device
query_device = 179
create_device = 180
delete_device =181
modify_device =182

#storage pool
start_monitor = 183
stop_monitor = 184
monitor_heart_beat = 185
monitor_data = 186

#snapshot_pool
create_snapshot_pool=187
delete_snapshot_pool=188
add_snapshot_node=189
remove_snapshot_node=190
query_snapshot_node=191
modify_snapshot_pool=192
query_snapshot_pool=193
#snapshot
create_snapshot = 194
delete_snapshot = 195
resume_snapshot = 196
query_snapshot = 197

#back up host
flush_disk_image = 198
query_host_backup = 199
backup_host = 200
resume_host = 201

#rule
query_rule = 202
add_rule = 203
remove_rule = 204

#VPC
query_network = 205
create_network = 206
modify_network = 207
query_network_detail = 208
start_network = 209
stop_network = 210
delete_network = 211
query_network_host = 212
attach_host = 213
detach_host = 214
network_attach_address = 215
network_detach_address = 216
network_bind_port = 217
network_unbind_port = 218
query_operate_detail = 219
query_service_detail = 220
query_service_summary = 221
query_operate_summary = 222

reset_host = 223
query_compute_pool_detail = 224

#Server
query_storage_device = 225
add_storage_device = 226
remove_storage_device = 227
enable_storage_device = 228
disable_storage_device = 229
modify_service = 230

enable_service = 231
disable_service =232

migrate_forwarder = 233
detach_forwarder = 234
attach_forwarder = 235
delete_forwarder = 236
create_forwarder = 237
delete_forwarder_group = 238
create_forwarder_group = 239
query_forwarder_group = 240
migrate_host = 241

query_whisper = 242
