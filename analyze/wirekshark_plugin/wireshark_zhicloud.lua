do
	local zhicloud_proto = Proto.new("Zhicloud", "Zhicloud transporter protocol")
	local f_d_version = ProtoField.uint8("Version","Version", base.DEC)
	
	local datagram_types = {
		[0] = "Data",
		[1] = "Ack",
	}
	
	local f_d_type = ProtoField.uint8("Type", "Datagram Type", base.DEC, datagram_types, 0x00000003)
	local f_d_seq = ProtoField.uint16("Sequence", "Datagram Sequence",base.DEC)
	local f_d_length = ProtoField.uint16("Length", "Payload Length",base.DEC)
	local f_d_crc = ProtoField.bytes("CRC", "Datagram CRC",base.HEX)
	local f_d_payload = ProtoField.bytes("Payload", "Datagram Payload", base.HEX)
	
	-- command define
	local command_types = {
		[0] = "keep_alive",
		[1] = "connect_request",
		[2] = "connect_response",
		[3] = "disconnect_request",
		[4] = "disconnect_response",
		[5] = "message_data",
		[6] = "connect_acknowledge",
	}
	local f_c_type = ProtoField.uint32("command", "Command Type", base.DEC, command_types)
	local f_c_session = ProtoField.uint32("session", "Command Session", base.HEX)	
	local f_c_client_key = ProtoField.string("c_client_key", "Client Key")
	local f_c_server_key = ProtoField.string("c_server_key", "Server Key")
	local f_c_digest = ProtoField.string("c_digest", "Digest")
	local f_c_sender = ProtoField.uint32("c_sender", "Command Sender", base.HEX)
	local f_c_name = ProtoField.string("c_name", "Name")
	local f_c_ip = ProtoField.string("c_ip", "IP")
	local f_c_port = ProtoField.uint16("c_port", "Port" )
	local f_c_data = ProtoField.bytes("c_data", "Data", base.HEX)
	local f_c_serial = ProtoField.uint32("c_serial", "Serial" )
	local f_c_index = ProtoField.uint32("c_index", "Index" )
	local f_c_total = ProtoField.uint32("c_total", "Total" )
	local f_c_success = ProtoField.bool("c_success", "Success" )
	local f_c_need_digest = ProtoField.bool("c_need_digest", "Need Digest" )
	
	-- messsage define
	
	local message_types = {
		[0] = "Request",
		[1] = "Response",
		[2] = "Event",
	}
	local f_m_id = ProtoField.uint32("m_id", "Message ID", base.DEC)
	local f_m_type = ProtoField.uint32("m_type", "Message Type", base.DEC, message_types)
	local f_m_success = ProtoField.bool("m_success", "Success" )
	local f_m_sender = ProtoField.string("m_sender", "Sender")
	local f_m_receiver = ProtoField.string("m_receiver", "Receiver")
	local f_m_session = ProtoField.uint32("m_session", "Session", base.HEX)
	local f_m_sequence = ProtoField.uint32("m_sequence", "Sequence", base.HEX)
	local f_m_transaction = ProtoField.uint32("m_transaction", "Transaction", base.HEX)
	
	
	
	zhicloud_proto.fields = { 
		f_d_version, f_d_type, f_d_seq, f_d_length, f_d_crc, f_d_payload, 
		f_c_type, f_c_session, f_c_client_key, f_c_server_key, f_c_digest, f_c_sender, f_c_name, f_c_ip, f_c_port, f_c_data, f_c_serial, f_c_index, f_c_total, f_c_success, f_c_need_digest,
		f_m_id, f_m_type, f_m_success, f_m_sender, f_m_receiver, f_m_session, f_m_sequence, f_m_transaction,
	}
	
	function read_variant( stream, offset )
	-- return output, used_bytes, next_pos
		local result = 0
		local used_bytes = 0
		local msb = 1
		local c = 0
		local int_value = 0
		local next_pos = offset
		while 1 == msb
		do
			c = stream( next_pos, 1):uint()
			msb = bit32.rshift(c, 7 )
			int_value = bit32.band(c, 0x7F)
			result = bit32.bor(result, bit32.lshift(int_value, (7*used_bytes) ) )
			used_bytes = used_bytes + 1
			next_pos = next_pos + 1
		end
		return result, used_bytes, next_pos
	end
	
	function read_string( stream, offset )
	-- return output, used_bytes, next_pos
		local result = ""
		local byte_count, used_bytes, next_pos = read_variant( stream, offset)
		if 0 == byte_count
		then
			return stream( next_pos , 0 ), used_bytes, next_pos
		end
		result = stream( next_pos, byte_count )
		used_bytes = used_bytes + byte_count
		next_pos = next_pos + byte_count
		return result, used_bytes, next_pos	
	end	
	
	function parse_message( buf, offset, element)
			local used_bytes = 0
			local start_offset = offset
			local next_offset = 0
			local u_v = 0
			local s_v = ""
			-- id
			u_v, used_bytes, next_offset = read_variant( buf, start_offset )
			element:add( f_m_id, buf( start_offset, used_bytes), u_v)			
			
			-- type & result
			start_offset = next_offset				
			u_v, used_bytes, next_offset = read_variant( buf, start_offset )
			element:add( f_m_type, buf( start_offset, used_bytes), bit32.rshift(u_v, 1 ) )
			element:add( f_m_success, buf( start_offset, used_bytes), bit32.band(u_v, 0x01 ) )
			
			start_offset = next_offset 
			s_v, used_bytes, next_offset = read_string( buf, start_offset )
			element:add( f_m_sender, buf( start_offset, used_bytes), s_v:string())	

			start_offset = next_offset 
			s_v, used_bytes, next_offset = read_string( buf, start_offset )
			element:add( f_m_receiver, buf( start_offset, used_bytes), s_v:string())	

			start_offset = next_offset				
			u_v, used_bytes, next_offset = read_variant( buf, start_offset )
			element:add( f_m_session, buf( start_offset, used_bytes), u_v )			

			start_offset = next_offset				
			u_v, used_bytes, next_offset = read_variant( buf, start_offset )
			element:add( f_m_sequence, buf( start_offset, used_bytes), u_v )			

			start_offset = next_offset				
			u_v, used_bytes, next_offset = read_variant( buf, start_offset )
			element:add( f_m_transaction, buf( start_offset, used_bytes), u_v )			
			
	
	end
	
	function parse_command( buf, offset, element)
	-- return command, session
			local command = 0
			local session = 0
			local used_bytes = 0
			local start_offset = 9
			local next_offset = 0
			local u_v = 0
			local s_v = ""
			command, used_bytes, next_offset = read_variant( buf, start_offset )
			local command_type = command_types[ command ]
			element:add( f_c_type, buf( start_offset, used_bytes), command)
			
			start_offset = next_offset
			session, used_bytes, next_offset = read_variant( buf, start_offset )
			element:add( f_c_session, buf( start_offset, used_bytes), session)	
			
			if ( 0 == command ) or (6 == command) or  (3 == command) 
			then
				-- keep alive/connect_acknowledge/disconnect_request
				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				element:add( f_c_name, buf( start_offset, used_bytes), s_v:string())	
				
			elseif 1 == command
			then
				-- connect_request
				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				element:add( f_c_client_key, buf( start_offset, used_bytes), s_v:string())	

				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				element:add( f_c_digest, buf( start_offset, used_bytes), s_v:string())	
				
				start_offset = next_offset 
				u_v, used_bytes, next_offset = read_variant( buf, start_offset )
				element:add( f_c_sender, buf( start_offset, used_bytes), u_v)	

				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				element:add( f_c_name, buf( start_offset, used_bytes), s_v:string())	

				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				element:add( f_c_ip, buf( start_offset, used_bytes), s_v:string())	
				
				start_offset = next_offset 
				u_v, used_bytes, next_offset = read_variant( buf, start_offset )
				element:add( f_c_port, buf( start_offset, used_bytes), u_v)					
			
			elseif 2 == command
			then
				-- connect_response
				start_offset = next_offset 
				u_v, used_bytes, next_offset = read_variant( buf, start_offset )
				element:add( f_c_success, buf( start_offset, used_bytes), bit32.band(u_v, 0x02))	
				element:add( f_c_need_digest, buf( start_offset, used_bytes), bit32.band(u_v, 0x01))	
				
				
				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				element:add( f_c_client_key, buf( start_offset, used_bytes), s_v:string())	

				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				element:add( f_c_server_key, buf( start_offset, used_bytes), s_v:string())	
				
				start_offset = next_offset 
				u_v, used_bytes, next_offset = read_variant( buf, start_offset )
				element:add( f_c_sender, buf( start_offset, used_bytes), u_v)	

				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				element:add( f_c_name, buf( start_offset, used_bytes), s_v:string())	

				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				element:add( f_c_ip, buf( start_offset, used_bytes), s_v:string())	
				
				start_offset = next_offset 
				u_v, used_bytes, next_offset = read_variant( buf, start_offset )
				element:add( f_c_port, buf( start_offset, used_bytes), u_v)					

			elseif 5 == command
			then
				-- message_data
				start_offset = next_offset 
				u_v, used_bytes, next_offset = read_variant( buf, start_offset )
				element:add( f_c_serial, buf( start_offset, used_bytes), u_v)		

				start_offset = next_offset 
				u_v, used_bytes, next_offset = read_variant( buf, start_offset )
				element:add( f_c_index, buf( start_offset, used_bytes), u_v)		
				
				start_offset = next_offset 
				u_v, used_bytes, next_offset = read_variant( buf, start_offset )
				element:add( f_c_total, buf( start_offset, used_bytes), u_v)										

				start_offset = next_offset 
				s_v, used_bytes, next_offset = read_string( buf, start_offset )
				local message_element = element:add( f_c_data, buf( start_offset, used_bytes), "")
				
				parse_message(s_v, 0, message_element)
							
			end	
						
			return command_type, session
	end
	
	function zhicloud_proto.dissector(buf,pkt,root)
		pkt.cols.protocol = "Zhicloud"
		local tree = root:add( zhicloud_proto, buf)
		local header_byte = buf(0, 1):uint()
		if 0x09 ~= bit32.rshift( header_byte , 4 )
		then
			-- check header
			pkt.cols.info = "Invalid zhicloud datagram"
			return
		end
		local d_type = bit32.extract( header_byte, 0, 2)
		local d_version = bit32.extract( header_byte, 2, 2)
		local d_seq = buf(1, 2):uint()
		
		tree:add( f_d_version, buf(0, 1), d_version)
		tree:add( f_d_type, buf(0, 1), d_type)		
		tree:add( f_d_seq, buf(1, 2), d_seq)
		
		if 0 == d_type
		then			
			tree:add( f_d_length, buf(3, 2))
			tree:add( f_d_crc, buf(5, 4))
			local payload_item = tree:add( f_d_payload, buf(9, buf:len() - 9), "")
			local command, session =  parse_command( buf, 9, payload_item, pkt.cols.info )			
			pkt.cols.info = "data-" .. d_seq .. ":" .. command .. "-" .. session			
			
		else
			pkt.cols.info = "ack-" .. d_seq
		end
		
	end

	local udp_table = DissectorTable.get("udp.port")
	udp_table:add(5600-5650, zhicloud_proto)

end