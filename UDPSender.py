import json,time,socket,struct
message = {
    "msg":{
        "cmd":"scan",
        "data":{
            "account_topic":"reserve",
        }    
    }
}
import socket
group = "239.255.255.250"
port = 4001
# 2-hop restriction in network
ttl = 2
sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM,
                     socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP,
                socket.IP_MULTICAST_TTL,
                ttl)
jsonResult = json.dumps(message)
print("Sending: "+jsonResult)
sock.sendto(bytes(jsonResult, "utf-8"), (group, port))

