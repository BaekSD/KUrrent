
class TrackerCore:
    def __init__(self, db):
        self.db = db

    def match_peer(self, hash):
        leecher_block_list = {}
        leecher_list = self.db.get_leecher_list(hash)
        for leecher in leecher_list:
            block_num_list = self.db.get_block_num_list(hash, leecher)
            leecher_block_list[leecher] = block_num_list

        leecher = leecher_list[0]
        #### 여기 해야 함
        for block in block_num_list:
            print(block)
        block = block_num_list[0]


        return leecher_ip, block
        pass