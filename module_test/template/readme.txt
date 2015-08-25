module_test的运行需要两份文件配合，一份是配置文件，定义了测试环境，测试配置等信息。另一份为测试用例
module_test的运行格式为
Usage: ./module_test -hv | [-f configure_file] -t test_file
 -f --config     configure file default value is "module_test.conf"
 -t --test         module test file
 -h --help       help information
 -v --version    help information
 
 -f 为指导配置文件，如果不指定，则默认使用当前路径的module_test.conf文件，如果该文件不存在将报错
 -t 为准备运行的测试脚本
 
配置文件的json格式定义如下

{	
	// 测试平台配置信息，该项必须存在，用于配置测试平台的通讯信息的
	//	"test_service_type":	测试平台内行， 必须存在于翻译表service中
	//	"ip": 测试平台的本地ip
	// 	"domain": 测试时使用的域名
	//	"group_ip":组播ip
	//	"group_port":组播端口
	"locale":{			
		"test_service_type":"control_server",	// 测试时的使用服务类型，它决定了连接到哪些平台上进行测试
		"ip":"192.168.0.100",	// 测试平台本地ip
		"domain":"syl",			// 测试域
		"group_ip":"224.9.9.6",	// 组播ip
		"group_port":5666		// 组播端口
	},
	
	 // 翻译表
	 // "trans"项 必须存在
	 // 它用于转换输入和输出的，
	 //		当使用字符串作为数字输入，并指定了适用的转换表后，平台将尝试使用该转换表将字符串翻译成数字
	 //		同样的，如果输出返回项设置了转换表，平台将尝试使用该转换表将数字转换为字符串，
	 //  如果翻译表中的数字和字符不是一一对应的关系，翻译会以找到的一项匹配项作为翻译基准（由于存储是乱序的，所以其实是随机的）
	"trans":{
		// 参数翻译表，必须存在
		"param":
		{
			"domain":0,
			"node_name":1,
			"node_type":2,
			....
		},
		// 服务翻译表，必须存在
		"service":
		{
	        "data_server" : 1,
            "control_server" : 2,
            "node_client" : 3,
            "storage_server" : 4,
			...
		},
		// 服务器状态表
		"service_mode":
		{
			"stop":0,
			"warring":1,
			"error":2,
			"running":3
		}
	},
	
	// 请求定义
	// "request_desc" 项，必须存在
	// 请求接口描述表
	// 数据类型描述 支持: uint, float, string, uint_array, float_array, string_array, uint_array_array, float_array_array, string_array_array
	// 基本结构为
	// 	"query_service_type" : 	// 请求名
	//  { "code": 93,	// 请求代码
	//	  "param_list": //  请求参数列表
	//		{  "type":		// 参数名,参数名必须在"param"翻译表中存在，
	//			{ 
	//				"data_type":"uint",		数据类型		
	//				"trans_tab":"service"	适用翻译表 可以让参数或数据更直观
	//				"optional":true			代表是否可选，如无该项，则默认为False，即为必填项
	//			}	
	//		},
	//	  "respone_list":
	//		{
	//			"type":		// 返回项名,参数名必须在"param"翻译表中存在，
	//			{ 
	//				"data_type":"uint_array",		数据类型		
	//				"trans_tab":"service"		适用翻译表 可以让参数或数据更直观
	//			}，
	//			"count":		// 返回项名,参数名必须在"param"翻译表中存在，
	//			{ 
	//				"data_type":"uint_array_array",		数据类型		
	//			}	
	//		}
	//	}
	// 如下例所示
	"request_desc":
	{
		"query_service_type":
		{
			"code": 92,
			"param_list":{},
			"respone_list":{	"type":{"data_type":"uint_array","trans_tab":"service"},	
								"count":{"data_type":"uint_array_array"} }
		},
		...
	}
}


测试脚本的配置如下
{
	// 测试任务
	// "test_task"关键字，必须存在，必须定义为数组
	// 每个成员必须为一下形式
	// {
		// "request":"query_service",		请求的命令
		// "param":{"type":"control_server", "group":"default"},	请求的参数,参数可以为变量，但如果该变量未被设值，将报错
		// "respone":{						对respone的处理
			// "server":{"set":["$abc"]}		"server" 为respone中的"server"项，见参数定义，支持以下设定
													"set"为将该项值设置为变量，变量必须为以$开头的字符串
													"include"为检查该项值是否存在于include所列出的值序列中，否则将报错，终止测试
													"except"为检查该项值是否不包含include所列出的值序列中，否则将报错，终止测试
		// }
	// },
	// 如下例所示
	"test_task":[ 
		{
			"request":"create_server_room",
			"param":{"name":"new_server_room_0", "display":"room_0_display", "description":"room_0_description!"},
			"respone":{
				"uuid":{"set":["$room"]}
			}
		},
		{
			"request":"query_server_room",
			"param":{},
			"respone":{
				"uuid":{"include":["$room"]},
				"name":{"include":["new_server_room_0"]}
			}
		},	
		{
			"request":"modify_server_room",
			"param":{"uuid":"$room", "name":"new_server_room_1", "display":"room_1_display", "description":"room_1_description"}
		},	
		{
			"request":"query_server_room",
			"param":{},
			"respone":{
				"uuid":{"include":["$room"]},
				"name":{"include":["new_server_room_1"],
						"except":["new_server_room_0"]
						}
			}
		},	
		{
			"request":"create_server_rack",
			"param":{ "name":"new_server_rack_0",
						"room":"$room" },
			"respone":{
				"uuid":{"set":["$rack"]}
			}
		},
		{
			"request":"query_server_rack",
			"param":{"room":"$room"},
			"respone":{
				"name":{"include":["new_server_rack_0"]},
				"uuid":{"include":["$rack"]}
			}
		}
	]
}


