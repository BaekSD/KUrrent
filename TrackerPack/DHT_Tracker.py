import math, random, threading, socket, time, json, sys

num = 0

'''
msg code explanation

    request_111(self, ip, port, req_ip, req_port, num):     check num is usable
        ip & port : ask to this tracker
        req_ip & req_port : answer to this tracker
        num : ask that is this num usable

    request_222(self, ip, port, num):                       answer that the number 'num' is usable
        ip & port : req_ip & req_port at request_111
        
    request_333(self, ip, port, num):                       answer that the number 'num' is not usable
        ip & port : req_ip & req_port at request_111
    
    request_444(self, ip, port, req_ip, req_port, num):     request that who has the responsibility of num
        ip & port : ask to this tracker
        req_ip & req_port : answer to this tracker
        num : ask that who has the responsibility of num
    
    request_555(self, ip, port, num, req_ip, req_port, num2):   answer that this tracker is responsibility for the number 'num'
    
    request_666(self, ip, port, min, max, count):           broadcast that tracker that has ip&port is responsibility for min ~ max
        ip & port : my ip & port
        min & max : number min & max
        count : first tracker - 0 ~ bit_len
                second tracker - 0 ~ bit_len-1
                ...
                last tracker - 0 ~ 0
                hard to explain by text....
'''

class Tracker():
    def __init__(self, ip, port, master_ip, master_port, master_tracker=False, bit_len=256):
        self.bit_len = bit_len
        self.key_range = int(math.pow(2,bit_len))
        self.master_tracker = master_tracker
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
        self.init_tracker()

    def init_tracker(self):    # join in dht
        if self.master_tracker:
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
        elif msg_code == 'get_peers':
            self.response_get_peers(msg_ele)
        elif msg_code == 'add_peer':
            self.response_add_peer(msg_ele)
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
        if self.master_tracker:
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
                # bypass to another tracker
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
                # bypass to another tracker
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
                # response that this tracker has responsibility of num
                self.request_555(self.ip, self.port, self.num, ip, port, num)
            else:
                # bypass this msg to another tracker
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
                # response that this tracker has responsibility of num
                self.request_555(self.ip, self.port, self.num, ip, port, num)
            elif 0 <= num and num <= self.max:
                # response that this tracker has responsibility of num
                self.request_555(self.ip, self.port, self.num, ip, port, num)
            else:
                # bypass this msg to another tracker
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
        # inform the responsibility of num is on this tracker
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
        # broadcast that this tracker is responsible for min ~ max
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

    def send_peers(self, ip, port, hash):
        # send the peers to ip & port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, int(port)))
            peer_dict = {
                'HEAD': 'DHT',
                'BODY': {}
            }
            peer_list = []
            if hash in self.hash_table.keys():
                for i in self.hash_table[hash]:
                    if i == ip+':'+str(port):
                        continue
                    peer_list.append(i)
            peer_dict['BODY'] = {hash: peer_list}
            msg = json.dumps(peer_dict)
            msg = msg.encode('utf-8')
            s.send(msg)
            print('sended')

    def request_get_peers(self, bypass_ip, bypass_port, ip, port, hash):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((bypass_ip, int(bypass_port)))
            bypass_msg = 'get_peers,' + hash + ',' + ip + ',' + port
            s.send(bypass_msg.encode())
            print('bypassed')

    def response_get_peers(self, msg):
        hash = int(msg[1], 16)
        ip = msg[2]
        port = msg[3]

        print(msg)

        if self.min <= self.max:
            if self.min <= hash and hash <= self.max:
                self.send_peers(ip, port, hash)
            else:
                # bypass this msg to another tracker
                for i in range(self.bit_len):
                    low = (self.num + int(math.pow(2,i))) % self.key_range
                    high = (self.num + int(math.pow(2,i+1))) % self.key_range
                    if low <= high:
                        if low <= hash and hash < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_get_peers(bypass_ip, bypass_port, ip, port, msg[1])
                            break
                    else:
                        if low <= hash and hash < self.key_range:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_get_peers(bypass_ip, bypass_port, ip, port, msg[1])
                            break
                        elif 0 <= hash and hash < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_get_peers(bypass_ip, bypass_port, ip, port, msg[1])
                            break
        else:
            if self.min <= hash and hash < self.key_range:
                self.send_peers(ip, port, hash)
            elif 0 <= hash and hash <= self.max:
                self.send_peers(ip, port, hash)
            else:
                # bypass this msg to another tracker
                for i in range(self.bit_len):
                    low = (self.num + int(math.pow(2,i))) % self.key_range
                    high = (self.num + int(math.pow(2,i+1))) % self.key_range
                    if low <= high:
                        if low <= hash and hash < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_get_peers(bypass_ip, bypass_port, ip, port, msg[1])
                            break
                    else:
                        if low <= hash and hash < self.key_range:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_get_peers(bypass_ip, bypass_port, ip, port, msg[1])
                            break
                        elif 0 <= hash and hash < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_get_peers(bypass_ip, bypass_port, ip, port, msg[1])
                            break

    def request_add_peer(self, bypass_ip, bypass_port, ip, port, hash):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((bypass_ip, int(bypass_port)))
            bypass_msg = 'add_peer,' + hash + ',' + ip + ',' + port
            s.send(bypass_msg.encode())
        print('bypassed')

    def response_add_peer(self, msg):
        hash = int(msg[1], 16)
        ip = msg[2]
        port = msg[3]

        print(msg)
        print(hash)

        if self.min <= self.max:
            if self.min <= hash and hash <= self.max:
                print("added")
                # add the peer
                if hash in self.hash_table.keys():
                    self.hash_table[hash].append(ip+':'+port)
                else:
                    self.hash_table[hash] = [ip+':'+port]
            else:
                # bypass this msg to another tracker
                for i in range(self.bit_len):
                    low = (self.num + int(math.pow(2,i))) % self.key_range
                    high = (self.num + int(math.pow(2,i+1))) % self.key_range
                    if low <= high:
                        if low <= hash and hash < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_add_peer(bypass_ip, bypass_port, ip, port, msg[1])
                            break
                    else:
                        if low <= hash and hash < self.key_range:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_add_peer(bypass_ip, bypass_port, ip, port, msg[1])
                            break
                        elif 0 <= hash and hash < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_add_peer(bypass_ip, bypass_port, ip, port, msg[1])
                            break
        else:
            if self.min <= hash and hash < self.key_range:
                print("added")
                # add the peer
                if hash in self.hash_table.keys():
                    self.hash_table[hash].append(ip+':'+port)
                else:
                    self.hash_table[hash] = [ip+':'+port]
            elif 0 <= hash and hash <= self.max:
                print("added")
                # add the peer
                if hash in self.hash_table.keys():
                    self.hash_table[hash].append(ip+':'+port)
                else:
                    self.hash_table[hash] = [ip+':'+port]
            else:
                # bypass this msg to another tracker
                for i in range(self.bit_len):
                    low = (self.num + int(math.pow(2,i))) % self.key_range
                    high = (self.num + int(math.pow(2,i+1))) % self.key_range
                    if low <= high:
                        if low <= hash and hash < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_add_peer(bypass_ip, bypass_port, ip, port, msg[1])
                            break
                    else:
                        if low <= hash and hash < self.key_range:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_add_peer(bypass_ip, bypass_port, ip, port, msg[1])
                            break
                        elif 0 <= hash and hash < high:
                            bypass_ip, bypass_port = self.dht_table[i][2].split(sep=':')
                            self.request_add_peer(bypass_ip, bypass_port, ip, port, msg[1])
                            break

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
        print('joined as tracker'+str(self.num))
        print('the time taken is ' + str(time.time()-start_time) + 's\n')

    def print_all(self):
        print("tracker" + str(self.num))
        print("min : " + str(self.min))
        print("max : " + str(self.max))
        print()
        #print("dht_table of tracker" + str(self.num) + " - " + str(self.ip) + ":" + str(self.port))
        #for i in self.dht_table:
        #    print(i)
        #print("hash_table of tracker" + str(self.num) + " - " + str(self.ip) + ":" + str(self.port))
        #print(self.hash_table)
        #for i in self.hash_table.items():
        #    print(i)

    def close(self):
        self.close_sock = True

if __name__ == "__main__":
    ip = '192.168.43.242'
    #ip = str(socket.gethostbyname(socket.getfqdn()))
    #print(ip)
    master_tracker = Tracker(ip=ip, port=15000 + num, master_ip=ip, master_port=15000 + num, master_tracker=True)
    tracker1 = Tracker(ip=ip, port=16000 + num, master_ip=ip, master_port=15000 + num, master_tracker=False)
    tracker2 = Tracker(ip=ip, port=17000 + num, master_ip=ip, master_port=15000 + num, master_tracker=False)
    tracker3 = Tracker(ip=ip, port=18000 + num, master_ip=ip, master_port=15000 + num, master_tracker=False)
    tracker4 = Tracker(ip=ip, port=19000 + num, master_ip=ip, master_port=15000 + num, master_tracker=False)
    tracker5 = Tracker(ip=ip, port=20000 + num, master_ip=ip, master_port=15000 + num, master_tracker=False)
    tracker6 = Tracker(ip=ip, port=21000 + num, master_ip=ip, master_port=15000 + num, master_tracker=False)
    tracker7 = Tracker(ip=ip, port=22000 + num, master_ip=ip, master_port=15000 + num, master_tracker=False)

    while not (tracker1.init_finished and tracker2.init_finished and tracker3.init_finished and
               tracker4.init_finished and tracker5.init_finished and tracker6.init_finished and tracker7.init_finished):
        pass
    #time.sleep(1)

    print("\n-----result-----\n")
    master_tracker.print_all()
    tracker1.print_all()
    tracker2.print_all()
    tracker3.print_all()
    tracker4.print_all()
    tracker5.print_all()
    tracker6.print_all()
    tracker7.print_all()


    time.sleep(1)
    '''
    hash = '365ec63a43faa5b2ce109561b17e3ca200586b55a0d2ef94bc7e869ba4d69d92'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, 15000+num))
        msg = 'add_peer,'+hash+','+ip+',15900'
        s.send(msg.encode())

    time.sleep(3)

    hash = '365ec63a43faa5b2ce109561b17e3ca200586b55a0d2ef94bc7e869ba4d69d92'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, 15000 + num))
        msg = 'get_peers,' + hash + ',' + ip + ',15900'
        s.send(msg.encode())

    '''
    time.sleep(10000)

'''
    master_tracker.close()
    tracker1.close()
    tracker2.close()
    tracker3.close()
'''