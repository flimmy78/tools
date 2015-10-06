说明：

Wireshark致云协议解析插件，用于解析wireshark抓到的udp 5600-5650端口的致云通讯协议报文内容


使用方式
1、将lua脚本放置在wireshark的plugin目录下
2、启动wireshark
3、打开抓包文件或者实时进行抓包，在报文清单中，右键菜单选择“Decode As”，在Transport右侧清单中选择"ZHICLOUD"，点击"OK"确认解析
4、符合条件的报文Protocol显示为"Zhicloud"，点击报文详情就可以在"Zhicloud transporter protocol"下查看报文解析结果

