import numpy as np
from queue import Queue
import random
import matplotlib.pyplot as plt
import copy
random.seed(3)
np.random.seed(3)
 
class pkt:
    def __init__(self,src,dst,generate_time):
        self.id = -1
        self.src = src
        self.dst = dst
        self.current_node = src
        self.time = 0  #time for transmission
        self.hop = 0
        self.terminate_flag = 0
        self.route = [src]
        self.generate_time = generate_time
        self.loss = False

    def __str__(self):
        content = 'id:'+ str(self.id)+ ' src:'+str(self.src)+' dst:' + str(self.dst) + ' generate_time:'+ str(self.generate_time)+' transmission_time:'+ str(self.time) +' hop:'+ str(self.hop)+' terminate_state:' + str(self.terminate_flag) + ' route:' + str(self.route)
        return content

def set_link(nt_topology,value):
    l = copy.deepcopy(nt_topology)
    for i in range(len(l)):
        for j in range(len(l[i])):
            l[i][j] = value
    return l



# network_topology = [[1,6],[0,2,7],[1,8],[4,9],[3,5,10],[4,11],[0,7,12],[1,6,8,13],[2,7,14],[3,10,15],[4,9,11,16],[5,10,17],[6,13,18],[7,12,14,19],[8,13,20],[9,16,21],[10,15,17,22],[11,16,23],[12,19,24],[13,18,20,25],[14,19,21,26],[15,20,22,27],[16,21,23,28],[17,22,29],[18,30],[19,26],[20,25],[21,28],[22,27],[23,35],[24,31],[30,32],[31,33],[32,34],[33,35],[29,34]]
# print(len(network_topology))
# network_topology = [[1,2],[0,3],[0,3],[1,2]]
network_topology = [[1,6],[0,2,7],[1,3,8],[2,4,9],[3,5,10],[4,11],[0,7,12],[1,6,8,13],[2,7,14],[3,10,15],[4,9,11,16],[5,10,17],[6,13],[7,12,14],[8,13,15],[9,14,16],[10,15,17],[11,16],[18]]
network_topology2 = [[1,6],[0,2,7],[1,3,8],[18],[3,5,10],[4,11],[0,7,12],[1,6,8,13],[2,7,14],[3,10,15],[4,9,11,16],[5,10,17],[6,13],[7,12,14],[8,13,15],[9,14,16],[10,15,17],[11,16],[18]]
initial_nt_topology = copy.deepcopy(network_topology)
# link = [[2,2],[2,2],[2,2],[2,2]]

# print(link)
link = set_link(network_topology,2)
initial_link = copy.deepcopy(link)
print(link)
# print(network_topology)
nodes_num = len(network_topology)
packet_list = [] #存储所有的数据包信息
node_list = [] #存储每个节点的数据包，用队列
Q_table = []
livePacketList = [] #还没有到大目的地数据包的index
fail_node = -1

time_per_hop = []
avgCount = 0
time_count = 0

fail = False
lamda = 4
max_time = 20000
node_capacity = 3
print_info = False
poisson_list = np.random.poisson(lam=lamda,size=max_time)
print(poisson_list)
 
# Route_table = {0:{0:0,1:1,2:2,3:1},
#                1:{0:0,1:1,2:0,3:3},
#                2:{0:0,1:0,2:2,3:3},
#                3:{0:1,1:1,2:2,3:3}
# }
Route_table = {0:{0:0,1:1,2:1,3:1,4:1,5:1,6:6,7:1,8:1,9:1,10:1,11:1,12:6,13:1,14:1,15:1,16:1,17:1,18:18},
               1:{0:0,1:1,2:2,3:2,4:2,5:2,6:7,7:7,8:7,9:2,10:2,11:2,12:7,13:7,14:2,15:2,16:2,17:2,18:18},
               2:{0:1,1:1,2:2,3:3,4:3,5:3,6:8,7:8,8:8,9:3,10:3,11:3,12:8,13:8,14:8,15:3,16:3,17:3,18:18},
               3:{0:2,1:2,2:2,3:3,4:4,5:4,6:2,7:2,8:2,9:9,10:4,11:4,12:2,13:2,14:2,15:9,16:4,17:4,18:18},
               # 3:{0:18,1:18,2:18,3:18,4:18,5:18,6:18,7:18,8:18,9:18,10:18,11:18,12:18,13:18,14:18,15:18,16:18,17:18,18:18},
               4:{0:3,1:3,2:3,3:3,4:4,5:5,6:3,7:3,8:3,9:10,10:10,11:10,12:3,13:3,14:3,15:3,16:10,17:10,18:18},
               5:{0:4,1:4,2:4,3:4,4:4,5:5,6:4,7:4,8:4,9:4,10:4,11:11,12:4,13:4,14:4,15:4,16:4,17:11,18:18},
               6:{0:0,1:7,2:7,3:7,4:7,5:7,6:6,7:7,8:7,9:7,10:7,11:7,12:12,13:7,14:7,15:7,16:7,17:7,18:18},
               7:{0:1,1:1,2:1,3:1,4:1,5:1,6:6,7:7,8:8,9:1,10:1,11:1,12:13,13:13,14:13,15:13,16:13,17:13,18:18},
               8:{0:2,1:2,2:2,3:2,4:2,5:2,6:7,7:7,8:8,9:2,10:2,11:2,12:14,13:14,14:14,15:14,16:14,17:14,18:18},
               9:{0:3,1:3,2:3,3:3,4:3,5:3,6:3,7:3,8:3,9:9,10:10,11:10,12:15,13:15,14:15,15:15,16:15,17:15,18:18},
               10:{0:4,1:4,2:4,3:4,4:4,5:4,6:4,7:4,8:4,9:9,10:10,11:11,12:16,13:16,14:16,15:16,16:16,17:16,18:18},
               11:{0:5,1:5,2:5,3:5,4:5,5:5,6:5,7:5,8:5,9:10,10:10,11:11,12:17,13:17,14:17,15:17,16:17,17:17,18:18},
               12:{0:6,1:6,2:6,3:6,4:6,5:6,6:6,7:6,8:6,9:13,10:13,11:13,12:12,13:13,14:13,15:13,16:13,17:13,18:18},
               13:{0:7,1:7,2:7,3:7,4:7,5:7,6:7,7:7,8:14,9:14,10:14,11:14,12:12,13:13,14:14,15:14,16:14,17:14,18:18},
               14:{0:8,1:8,2:8,3:8,4:8,5:8,6:8,7:8,8:8,9:15,10:15,11:15,12:13,13:13,14:14,15:15,16:15,17:15,18:18},
               15:{0:9,1:9,2:9,3:9,4:9,5:9,6:14,7:14,8:14,9:9,10:9,11:9,12:14,13:14,14:14,15:15,16:16,17:16,18:18},
               16:{0:10,1:10,2:10,3:10,4:10,5:10,6:15,7:15,8:15,9:10,10:10,11:10,12:15,13:15,14:15,15:15,16:16,17:17,18:18},
               17:{0:11,1:11,2:11,3:11,4:11,5:11,6:16,7:16,8:16,9:11,10:11,11:11,12:16,13:16,14:16,15:16,16:16,17:16,18:18}}

Route_table2 = {0:{0:0,1:1,2:1,3:1,4:1,5:1,6:6,7:1,8:1,9:1,10:1,11:1,12:6,13:1,14:1,15:1,16:1,17:1,18:18},
               1:{0:0,1:1,2:2,3:2,4:2,5:2,6:7,7:7,8:7,9:2,10:2,11:2,12:7,13:7,14:2,15:2,16:2,17:2,18:18},
               2:{0:1,1:1,2:2,3:3,4:3,5:3,6:8,7:8,8:8,9:3,10:3,11:3,12:8,13:8,14:8,15:3,16:3,17:3,18:18},
               # 3:{0:2,1:2,2:2,3:3,4:4,5:4,6:2,7:2,8:2,9:9,10:4,11:4,12:2,13:2,14:2,15:9,16:4,17:4,18:18},
               3:{0:18,1:18,2:18,3:18,4:18,5:18,6:18,7:18,8:18,9:18,10:18,11:18,12:18,13:18,14:18,15:18,16:18,17:18,18:18},
               4:{0:3,1:3,2:3,3:3,4:4,5:5,6:3,7:3,8:3,9:10,10:10,11:10,12:3,13:3,14:3,15:3,16:10,17:10,18:18},
               5:{0:4,1:4,2:4,3:4,4:4,5:5,6:4,7:4,8:4,9:4,10:4,11:11,12:4,13:4,14:4,15:4,16:4,17:11,18:18},
               6:{0:0,1:7,2:7,3:7,4:7,5:7,6:6,7:7,8:7,9:7,10:7,11:7,12:12,13:7,14:7,15:7,16:7,17:7,18:18},
               7:{0:1,1:1,2:1,3:1,4:1,5:1,6:6,7:7,8:8,9:1,10:1,11:1,12:13,13:13,14:13,15:13,16:13,17:13,18:18},
               8:{0:2,1:2,2:2,3:2,4:2,5:2,6:7,7:7,8:8,9:2,10:2,11:2,12:14,13:14,14:14,15:14,16:14,17:14,18:18},
               9:{0:3,1:3,2:3,3:3,4:3,5:3,6:3,7:3,8:3,9:9,10:10,11:10,12:15,13:15,14:15,15:15,16:15,17:15,18:18},
               10:{0:4,1:4,2:4,3:4,4:4,5:4,6:4,7:4,8:4,9:9,10:10,11:11,12:16,13:16,14:16,15:16,16:16,17:16,18:18},
               11:{0:5,1:5,2:5,3:5,4:5,5:5,6:5,7:5,8:5,9:10,10:10,11:11,12:17,13:17,14:17,15:17,16:17,17:17,18:18},
               12:{0:6,1:6,2:6,3:6,4:6,5:6,6:6,7:6,8:6,9:13,10:13,11:13,12:12,13:13,14:13,15:13,16:13,17:13,18:18},
               13:{0:7,1:7,2:7,3:7,4:7,5:7,6:7,7:7,8:14,9:14,10:14,11:14,12:12,13:13,14:14,15:14,16:14,17:14,18:18},
               14:{0:8,1:8,2:8,3:8,4:8,5:8,6:8,7:8,8:8,9:15,10:15,11:15,12:13,13:13,14:14,15:15,16:15,17:15,18:18},
               15:{0:9,1:9,2:9,3:9,4:9,5:9,6:14,7:14,8:14,9:9,10:9,11:9,12:14,13:14,14:14,15:15,16:16,17:16,18:18},
               16:{0:10,1:10,2:10,3:10,4:10,5:10,6:15,7:15,8:15,9:10,10:10,11:10,12:15,13:15,14:15,15:15,16:16,17:17,18:18},
               17:{0:11,1:11,2:11,3:11,4:11,5:11,6:16,7:16,8:16,9:11,10:11,11:11,12:16,13:16,14:16,15:16,16:16,17:16,18:18}}

 
 
for i in range(nodes_num):
    node_list.append([])
 
def choose_available_link(node):
    action_set = []
    for i in range(len(network_topology[node])):
        if link[node][i]>0:
            action_set.append(network_topology[node][i])
            
    return action_set

def caculate_time_per_hop(packet_list):
    time = 0
    hop = 0
    for p in packet_list:
        time += p.time
        hop += p.hop
    return time/hop


 
def getNewPackets(currenttime):   #每个模拟时间中产生对应的数据包
    packets_list = []
    packets_count = poisson_list[currenttime] #返回当前时间产生的数据包数量
    for x in range(packets_count):
        if fail:
            nodes = random.sample([0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17],2) #从0到36生成俩
        else:
            nodes = random.sample([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],2)

        #[src,dst,current_node,time,time,terminate_flag,route]
        new_packet = pkt(nodes[0],nodes[1],currenttime) #每个packet结构 后面4个啥意思？？？？？
        packets_list.append(new_packet)
    return packets_list
 
def getQueueTime():    #获得本次排队时间
    return 0

def cal_loss(time_count):
    # gaibian = 0
    for p in packet_list:
        if p.current_node==18 and p.loss==False:
            p.loss=True
            # gaibian+=1
    # print('gaibian',gaibian)

    avg_path_length = 0
    loss_num = 0
    sample_packet_list = packet_list[-100:]
    for p in sample_packet_list:
        if p.loss == False and p.terminate_flag==1:
            avg_path_length += p.hop
        else:
            loss_num += 1
    with open('data/SP avg and loss3.txt','a+') as f:
        f.write(str(time_count))
        f.write(',')
        f.write(str(avg_path_length/len(sample_packet_list)))
        f.write(',')
        f.write(str(loss_num/len(sample_packet_list)))
        f.write('\n')
    print(loss_num/len(sample_packet_list))
# packets = getNewPackets(0)
# for p in packets:
#     print(p)
# packets = getNewPackets(1)
# for p in packets:
#     print(p)

while(time_count < max_time):
# time_count = 1
# 
    # print('****time start:',time_count)
    if time_count>=5000:
        fail = True
        network_topology = network_topology2
        Route_table = Route_table2
    packets = getNewPackets(time_count) #生成当前时间数据包列表

    next_time_packets = []
    for i in range(nodes_num):
        next_time_packets.append([])



    if len(packets) > 0:    
        
        for packet in packets:
            packet.id = len(packet_list)
            # print('pkt length:',len(packet_list))
            livePacketList.append(packet.id)
            node_list[packet.src].append(packet.id) #发包的路由器放入包序号？
            packet_list.append(packet)
        # for p in livePacketList:
        #     packet_list[p].time += 1
        if print_info:
            print('time:',time_count)
            print('livePacketList:',livePacketList)
            # print('node_list',node_list)
            print('new packets at time',time_count)
            for p in packets:
                print(p)
            print()
    # else:


    for node_index in range(len(node_list)-1):  #遍历每个node

        if print_info:
            print('for node',node_index,'*'*9)
        node_work_quantity = len(node_list[node_index])
        while (node_list[node_index] != []) and (node_work_quantity-len(node_list[node_index])<=node_capacity):       #如果它有包要发
            packet_index = node_list[node_index].pop(0)   #把这个node的第一个包的序号拿出来  只发一个包！
            packet = packet_list[packet_index]

            # if packet.id == 151:
            #     print('currenttime',time_count)
            #     print(packet.time)

            pnode = packet.current_node        #包所在当前节点
            ptime = packet.time        #标记包上次时间？
            dst = packet.dst          #标记包的目标
            ptable = Route_table[pnode]  #包的所在节点的qtable
            
            
            # print('at time',time_count,'for node',pnode,'action set is',available_action)
            
            
            
                # print('jin ru!','packet id=',packet.id)

                # if packet.id == 1:
                #     print('at time',time_count,'the hop of id 1 is',packet.hop)
            packet_list[packet_index].hop += 1
                # if packet.id == 1:
                #     print('id 1:',packet.hop)




            next_node = ptable[packet.dst]
            if link[pnode][network_topology[pnode].index(next_node)]>0:
                link[pnode][network_topology[pnode].index(next_node)] -= 1
            else:
                packet_list[packet_index].loss = True
                packet_list[packet_index].time += 1
                livePacketList.remove(packet_index)
                continue

            # print(link)
            if print_info:
                print('packet.id:',packet.id,' from time start:',time_count,'link',pnode,'->',next_node,'-1')
            packet.route.append(next_node)
                

            

            if next_node == dst or next_node== 18:                     #修改相关包的信息，将数据包入队列---改包信息
                if next_node==18:
                    packet_list[packet_index].current_node = 18
                else:
                    packet_list[packet_index].current_node = dst      #包的当前位置设置为dst
                packet_list[packet_index].time += 1
                # packet_list[packet_index].hop += 1
                packet_list[packet_index].terminate_flag = 1        #到达标志位设为1

                livePacketList.remove(packet_index)
                if print_info:
                    print('packet.id:',packet.id,' from time end:',time_count,'link',pnode,'->',next_node,'+1')
            else:
                packet_list[packet_index].current_node = next_node
                # packet_list[packet_index].time += 1
                # packet_list[packet_index].hop += 1
                # node_list[next_node].append(packet_index)#---------
                next_time_packets[next_node].append(packet_index)
                    
    link = copy.deepcopy(initial_link)
    for p in livePacketList:
        packet_list[p].time += 1
                
                
    
    # print('packet list:--------------')
    # for p in packet_list:
    #     print(p)
    # print('packet list:--------------')
    time_count += 1
    
    for i in range(len(node_list)):
        for j in next_time_packets[i]:
            node_list[i].append(j)

    
    time_per_hop.append(caculate_time_per_hop(packet_list))
    # print('****time finish:',time_count)
    if time_count%100==0:
        print(time_count)
        cal_loss(time_count)

count = 0
for p in packet_list:
    if p.time > p.hop:
        count += 1
print('the packet num of (time>hop) is',count)

# gaibian = 0
# for p in packet_list:
#     if p.current_node==18 and p.loss==False:
#         p.loss=True
#         gaibian+=1
# print('gaibian',gaibian)

# avg_path_length = 0
# loss_num = 0
# sample_packet_list = packet_list[-100:]
# for p in sample_packet_list:
#     if p.loss == False and p.terminate_flag==1:
#         avg_path_length += p.hop
#     else:
#         loss_num += 1




# print('average path length:',avg_path_length/(len(sample_packet_list)-loss_num))
# print('packet loss rate:',loss_num/len(sample_packet_list))

# with open(f'data/shortest path lamda={lamda} max_time={max_time} 5000 drop node 3.txt','w') as f:
#     f.write('average path length:'+ str(avg_path_length/(len(sample_packet_list)-loss_num)))
#     f.write('\n')
#     f.write('packet loss rate:'+ str(loss_num/len(sample_packet_list)))


print()
plt.plot(range(max_time),time_per_hop)
plt.xlabel('time')
plt.ylabel('time per hop')

plt.show()
