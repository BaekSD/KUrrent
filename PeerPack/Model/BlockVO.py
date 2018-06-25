class BlockVO:
    def __init__(self, file_hash, file_path, block_num, block_data):
        self.file_hash = file_hash
        self.file_path = file_path
        self.block_data = block_data
        self.block_num = block_num

