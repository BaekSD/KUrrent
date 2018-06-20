class Parser:
    def __int__(self):
        pass

    def get_file_info(self, kurrent_file):
        file_info = kurrent_file.read().split('\n')
        return file_info

    def get_file_hash(self, kurrent_file):
        file_info = self.get_file_info(kurrent_file)
        return file_info[0]

    def get_tracker_size(self, kurrent_file):
        file_info = self.get_file_info(kurrent_file)
        tracker_size = file_info[1].split(' ')[-1]
        return tracker_size

    def get_tracker_list(self, kurrent_file):
        file_info = self.get_file_info(kurrent_file)
        tracker_size = self.get_tracker_size(kurrent_file)
        file_hash = file_info[0]
        tracker_list = []
        for i in range(2, int(tracker_size) + 2):
            tracker_list.append(file_info[i])
        return tracker_list, file_hash

    def parse_tracker_text(self, tracker_text):
        tracker_list = tracker_text.split('\n')
        return tracker_list

    def get_file_list(self, kurrent_file):
        file_list = {}
        file_info = self.get_file_info(kurrent_file)
        for i in range(int(self.get_tracker_size(kurrent_file))+2, len(file_info), 2):
            file_list[file_info[i]] = int(file_list[file_info[i+1]])
        return file_list

    def get_total_size(self, kurrent_file):
        file_list = self.get_file_list(kurrent_file)
        size = 0
        for i in file_list.values():
            size += i
        return size
