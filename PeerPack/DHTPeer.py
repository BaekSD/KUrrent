import math, random, threading, socket, time

num = 0

'''
msg code explanation

    request_111(self, ip, port, req_ip, req_port, num):     check num is usable
        ip & port : ask to this peer
        req_ip & req_port : answer to this peer
        num : ask that is this num usable

    request_222(self, ip, port, num):                       answer that the number 'num' is usable
        ip & port : req_ip & req_port at request_111
        
    request_333(self, ip, port, num):                       answer that the number 'num' is not usable
        ip & port : req_ip & req_port at request_111
    
    request_444(self, ip, port, req_ip, req_port, num):     request that who has the responsibility of num
        ip & port : ask to this peer
        req_ip & req_port : answer to this peer
        num : ask that who has the responsibility of num
    
    request_555(self, ip, port, num, req_ip, req_port, num2):   answer that this peer is responsibility for the number 'num'
    
    request_666(self, ip, port, min, max, count):           broadcast that peer that has ip&port is responsibility for min ~ max
        ip & port : my ip & port
        min & max : number min & max
        count : first peer - 0 ~ bit_len
                second peer - 0 ~ bit_len-1
                ...
                last peer - 0 ~ 0
                hard to explain by text....
'''

class Peer():
    def __init__(self, ip, port, master_ip, master_port, master_peer=False, bit_len=256):
        self.bit_len = bit_len
        self.key_range = int(math.pow(2,bit_len))
        self.master_peer = master_peer
        self.ip = ip
        self.port = port
        self.num = -1
        self.master_ip = master_ip
        self.master_port = master_port
        self.dht_table = []
        self.hash_table = {}
        self.min = 0
        self.max = self.key_range-1
        self.joining_sem = threading.Semaphore(1)
        self.req_sem = threading.Semaphore(1)
        self.init_num_finish = False
        self.init_num_trying = False
        self.num_init_table_finish = 0
        self.close_sock = False
        self.init_finished = False
        self.server_th = threading.Thread(target=self.run_sock)
        self.server_th.daemon = True
        self.server_th.start()
        self.init_peer()

    def init_peer(self):    # join in dht
        if self.master_peer:
            self.num = 0
            self.min = (self.num+1) % self.key_range
            self.max = self.num
            for i in range(self.bit_len):
                self.dht_table.append([(self.num+int(math.pow(2, i))) % self.key_range, self.num, str(self.ip)+':'+str(self.port)])
            self.init_num_finish = True
        else:
            init_th = threading.Thread(target=self.run_init)
            init_th.daemon = True
            init_th.start()

    def run_sock(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen(5)
            while True:
                try:
                    conn, addr = s.accept()
                    response_th = threading.Thread(target=self.run_response, args=(conn, addr))
                    response_th.daemon = True
                    response_th.start()
                except:
                    if self.close_sock:
                        break

    def run_response(self, conn, addr):
        msg = conn.recv(1024).decode()
        msg_ele = msg.split(sep=',')
        msg_code = msg_ele[0]
        if msg_code == '000':
            self.response_000(msg_ele)
        if msg_code == '111':
            self.response_111(msg_ele)
        elif msg_code == '222':
            self.response_222(msg_ele, conn)
        elif msg_code == '333':
            self.response_333(msg_ele)
        elif msg_code == '444':
            self.response_444(msg_ele)
        elif msg_code == '555':
            self.response_555(msg_ele)
        elif msg_code == '666':
            self.response_666(msg_ele)
        conn.close()

    def request_000(self, ip, port):
        # join finished msg send to master
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, int(port)))
            msg = "000,"
            s.send(msg.encode())

    def response_000(self, msg):
        # join finished so release the semaphore
        time.sleep(0.3)
        self.joining_sem.release()

    def request_111(self, ip, port, req_ip, req_port, num):
        # request that is the number 'num' usable
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, int(port)))
            msg = "111," + str(req_ip) + ',' + str(req_port) + ',' + str(num)
            s.send(msg.encode())

    def response_111(self, msg):
        # response that the number 'num' usability
        ip = msg[1]
        port = int(msg[2])
        num = int(msg[3])
        if self.master_peer:
            self.joining_sem.acquire()
        print('acquired : ' + str(port) + ' : ' + str(num))
        if self.min <= self.max:
            if self.min <= num and num < self.max:
                # send the number 'num' is ok
                self.request_222(ip, port, num)
                self.min = (num + 1) % self.key_range
            elif num == self.max:
                self.request_333(ip, port, num)
                # send the number 'num' is not ok
            else:
                # bypass to another peer
                for i in range(self.bit_len):
                    low = (self.num + int(math.pow(2, i))) % self.key_range
                    high = (self.num + int(math.pow(2, i + 1))) % self.key_range
                    if low <= high:
                        if low <= num and num < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_111(bypass_ip, bypass_port, ip, port, num)
                            break
                    else:
                        if low <= num and num < self.key_range:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_111(bypass_ip, bypass_port, ip, port, num)
                            break
                        elif 0 <= num and num < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_111(bypass_ip, bypass_port, ip, port, num)
                            break
        else:
            if self.min <= num and num < self.key_range:
                # send the number 'num' is ok
                self.request_222(ip, port, num)
                self.min = (num+1) % self.key_range
            elif 0 <= num and num < self.max:
                # send the number 'num' is ok
                self.request_222(ip, port, num)
                self.min = (num+1) % self.key_range
            elif num == self.max:
                self.request_333(ip, port, num)
                # send the number 'num' is not ok
            else:
                # bypass to another peer
                for i in range(self.bit_len):
                    low = (self.num + int(math.pow(2, i))) % self.key_range
                    high = (self.num + int(math.pow(2, i + 1))) % self.key_range
                    if low <= high:
                        if low <= num and num < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_111(bypass_ip, bypass_port, ip, port, num)
                            break
                    else:
                        if low <= num and num < self.key_range:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_111(bypass_ip, bypass_port, ip, port, num)
                            break
                        elif 0 <= num and num < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_111(bypass_ip, bypass_port, ip, port, num)
                            break

    def request_222(self, ip, port, num):
        # inform that the num is usable
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            res = '222,' + str(self.min) + ',' + str(num)
            s.send(res.encode())
            s.recv(1024)

            for i in self.hash_table.keys():
                if self.min <= num and self.min <= i and i <= num:
                    for j in self.hash_table[i]:
                        res = 'con,' + str(i) + ',' + str(j)
                        s.send(res.encode())
                        s.recv(1024)
                    del (self.hash_table[i])
                elif self.min > num and self.min <= i and i < self.key_range:
                    for j in self.hash_table[i]:
                        res = 'con,' + str(i) + ',' + str(j)
                        s.send(res.encode())
                        s.recv(1024)
                    del (self.hash_table[i])
                elif self.min > num and 0 < i and i <= num:
                    for j in self.hash_table[i]:
                        res = 'con,' + str(i) + ',' + str(j)
                        s.send(res.encode())
                        s.recv(1024)
                    del (self.hash_table[i])
            s.send('fin,'.encode())

    def response_222(self, msg, conn):
        if self.num == int(msg[2]):
            self.min = int(msg[1])
            self.max = self.num
            self.init_num_finish = True
            while True:
                conn.send('ack'.encode())
                m = conn.recv(1024).decode().split(sep=',')
                if m[0] == 'fin':
                    break
                elif m[0] == 'con':
                    if int(m[1]) in self.hash_table.keys():
                        self.hash_table[int(m[1])].append(m[2])
                    else:
                        self.hash_table[int(m[1])] = [m[2]]
        else:
            self.init_num_finish = False
        self.joining_sem.release()

    def request_333(self, ip, port, num):
        # inform that the num is not usable
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.send(('333,' + str(num)).encode())

    def response_333(self, msg):
        self.init_num_finish = False
        self.joining_sem.release()

    def request_444(self, ip, port, req_ip, req_port, num):
        # request that who has the responsibility of num
        self.req_sem.acquire()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, int(port)))
            msg = "444," + str(req_ip) + ',' + str(req_port) + ',' + str(num)
            s.send(msg.encode())
        self.req_sem.release()

    def response_444(self, msg):
        ip = msg[1]
        port = msg[2]
        num = int(msg[3])
        if self.min <= self.max:
            if self.min <= num and num <= self.max:
                # response that this peer has responsibility of num
                self.request_555(self.ip, self.port, self.num, ip, port, num)
            else:
                # bypass this msg to another peer
                for i in range(self.bit_len):
                    low = (self.num + int(math.pow(2,i))) % self.key_range
                    high = (self.num + int(math.pow(2,i+1))) % self.key_range
                    if low <= high:
                        if low <= num and num < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_444(bypass_ip, bypass_port, ip, port, num)
                            break
                    else:
                        if low <= num and num < self.key_range:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_444(bypass_ip, bypass_port, ip, port, num)
                            break
                        elif 0 <= num and num < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_444(bypass_ip, bypass_port, ip, port, num)
                            break
        else:
            if self.min <= num and num < self.key_range:
                # response that this peer has responsibility of num
                self.request_555(self.ip, self.port, self.num, ip, port, num)
            elif 0 <= num and num <= self.max:
                # response that this peer has responsibility of num
                self.request_555(self.ip, self.port, self.num, ip, port, num)
            else:
                # bypass this msg to another peer
                for i in range(self.bit_len):
                    low = (self.num + int(math.pow(2,i))) % self.key_range
                    high = (self.num + int(math.pow(2,i+1))) % self.key_range
                    if low <= high:
                        if low <= num and num < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_444(bypass_ip, bypass_port, ip, port, num)
                            break
                    else:
                        if low <= num and num < self.key_range:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_444(bypass_ip, bypass_port, ip, port, num)
                            break
                        elif 0 <= num and num < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_444(bypass_ip, bypass_port, ip, port, num)
                            break

    def request_555(self, ip, port, num, req_ip, req_port, num2):
        # inform the responsibility of num is on this peer
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((req_ip, int(req_port)))
            msg = "555,"+str(ip)+':'+str(port)+","+str(num)+','+str(num2)
            s.send(msg.encode())

    def response_555(self, msg):
        ipNport = msg[1]
        num = msg[2]
        num2 = msg[3]
        for i in range(len(self.dht_table)):
            if self.dht_table[i][0] == int(num2):
                self.dht_table[i][1] = int(num)
                self.dht_table[i][2] = ipNport
                self.num_init_table_finish += 1
                break

    def request_666(self, ip, port, min, max, count):
        # broadcast that this peer is responsible for min ~ max
        if count == self.bit_len+1:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.master_ip, self.master_port))
                msg = '666,' + str(ip) + ':' + str(port) + ',' + str(min) + ',' + str(max) + ',' + str(self.bit_len)
                s.send(msg.encode())
        else:
            before_send = ''
            for i in range(count):
                req_ip, req_port = self.dht_table[i][2].split(sep=':')
                if req_ip == self.ip and int(req_port) == self.port:
                    break
                elif before_send == self.dht_table[i][2]:
                    continue
                else:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((req_ip, int(req_port)))
                        msg = '666,'+str(ip)+':'+str(port)+','+str(min)+','+str(max)+','+str(i)
                        s.send(msg.encode())
                    before_send = self.dht_table[i][2]

    def response_666(self, msg):
        ip, port = msg[1].split(sep=':')
        min = msg[2]
        max = msg[3]
        count = int(msg[4])
        for i in range(len(self.dht_table)):
            if int(min) <= int(max):
                if int(min) <= self.dht_table[i][0] and self.dht_table[i][0] <= int(max):
                    self.dht_table[i][1] = int(max)
                    self.dht_table[i][2] = ip+':'+port
            else:
                if int(min) <= self.dht_table[i][0] and self.dht_table[i][0] < self.key_range:
                    self.dht_table[i][1] = int(max)
                    self.dht_table[i][2] = ip+':'+port
                elif 0 <= self.dht_table[i][0] and self.dht_table[i][0] <= int(max):
                    self.dht_table[i][1] = int(max)
                    self.dht_table[i][2] = ip+':'+port
        self.request_666(ip, port, min, max, count)

    def run_init(self):
        self.joining_sem.acquire()
        start_time = 0
        while True:
            print('init start')
            self.num = random.randrange(1, self.key_range)
            print('trying num : ' + str(self.num))
            self.request_111(self.master_ip, self.master_port, self.ip, self.port, self.num)
            self.joining_sem.acquire()
            start_time = time.time()
            print('get num : '+ str(self.init_num_finish))
            if self.init_num_finish:
                for i in range(self.bit_len):
                    pow2i = (self.num+int(math.pow(2, i))) % self.key_range
                    self.dht_table.append([pow2i, self.num, str(self.ip)+':'+str(self.port)])
                self.num_init_table_finish = 0
                print('dht table information request started')
                for i in range(self.bit_len):
                    if i%20 == 19:
                        print(str(i/self.bit_len*100) + '%')
                    pow2i = (self.num+int(math.pow(2, i))) % self.key_range
                    if self.min <= self.max:
                        if self.min <= pow2i and pow2i <= self.max:
                            self.dht_table[i] = [pow2i, self.num, str(self.ip)+':'+str(self.port)]
                            self.num_init_table_finish += 1
                        else:
                            th = threading.Thread(target=self.request_444, args=(self.master_ip, self.master_port, self.ip, self.port, pow2i))
                            th.daemon = True
                            th.start()
                    else:
                        if self.min <= pow2i and pow2i < self.key_range:
                            self.dht_table[i] = [pow2i, self.num, str(self.ip)+':'+str(self.port)]
                            self.num_init_table_finish += 1
                        elif 0 <= pow2i and pow2i <= self.max:
                            self.dht_table[i] = [pow2i, self.num, str(self.ip)+':'+str(self.port)]
                            self.num_init_table_finish += 1
                        else:
                            th = threading.Thread(target=self.request_444, args=(self.master_ip, self.master_port, self.ip, self.port, pow2i))
                            th.daemon = True
                            th.start()
                print('dht table information response waiting')
                while self.num_init_table_finish < self.bit_len:
                    pass
                print('dht table init finished')
                self.request_666(self.ip, self.port, self.min, self.max, self.bit_len+1)
                break
            else:
                self.request_000(self.master_ip, self.master_port)
        self.request_000(self.master_ip, self.master_port)
        self.init_finished = True
        print('joined as peer'+str(self.num))
        print('the time taken is ' + str(time.time()-start_time) + 's\n')

    def print_all(self):
        print("peer" + str(self.num))
        print("min : " + str(self.min))
        print("max : " + str(self.max))
        print()
        #print("dht_table of peer" + str(self.num) + " - " + str(self.ip) + ":" + str(self.port))
        #for i in self.dht_table:
        #    print(i)
        #print("hash_table of peer" + str(self.num) + " - " + str(self.ip) + ":" + str(self.port))
        #print(self.hash_table)
        #for i in self.hash_table.items():
        #    print(i)

    def close(self):
        self.close_sock = True

if __name__ == "__main__":
    master_peer = Peer(ip='127.0.0.1', port=15000 + num, master_ip='127.0.0.1', master_port=15000 + num, master_peer=True)
    peer1 = Peer(ip='127.0.0.1', port=16000 + num, master_ip='127.0.0.1', master_port=15000 + num, master_peer=False)
    peer2 = Peer(ip='127.0.0.1', port=17000 + num, master_ip='127.0.0.1', master_port=15000 + num, master_peer=False)
    peer3 = Peer(ip='127.0.0.1', port=18000 + num, master_ip='127.0.0.1', master_port=15000 + num, master_peer=False)

    while not peer3.init_finished:
        pass
    #time.sleep(1)

    print("\n-----result-----\n")
    master_peer.print_all()
    peer1.print_all()
    peer2.print_all()
    peer3.print_all()
'''
    master_peer.close()
    peer1.close()
    peer2.close()
    peer3.close()
'''
