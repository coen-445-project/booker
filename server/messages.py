from timer import Timer


class Message:
    def __init__(self, msg=None, source=None, *args):
        # unpack arguments
        self.header = msg
        self.source = source
        self.args = list(args)
        self.formed = False
        self.done = False
        
        # instantiate timer
        self.timer = Timer()
        # number of times retried
        self.retries = 0
        
        self.resp_reason = ""

    def __str__(self):
        data = f"Message received from ID {self.source}, contents:\n" \
            f"\tCommand: {self.header}\n" \
            f"\tDetails: {self.args}"
        return data


    def decode(self, source, msg_recv):
        self.source = source.split(".")[-1]
        parts = msg_recv.split(",;,")
        self.header = parts[0]
        self.args = parts[1:]
        
        if self.header == "REQUEST":
            # timeout stuff
            self.unavailable = True
            
            # details
            self.mt_id = -1
            self.rq_id = self.args[0]
            self.date = self.args[1]
            self.time = self.args[2]
            self.min_parts = self.args[3]
            tmp = self.args[4].split(",")
            tmp = [int(i) for i in tmp]
            self.ls_parts = dict(zip(tmp, [0 for i in tmp]))
            self.args[4] = ",".join([str(x) for x in list(self.ls_parts.keys())])
            self.topic = self.args[5]
            
        elif self.header == "CANCEL":
            self.mt_id = self.args[0]
            self.ls_parts = []
            
        elif self.header == "ACCEPT":
            self.mt_id = self.args[0]
            
        self.formed = True
    
    def encode(self):
        if self.header == "RESPONSE":
            concat = ",;,".join([self.header, self.rq_id, self.resp_reason])
        elif self.header == "INVITE":
            concat = ",;,".join([self.header, self.mt_id, self.date, self.time, self.topic, self.source])
        elif self.header == "CANCEL":
            concat = ",;,".join([self.header, self.mt_id, self.resp_reason])
        return concat.encode('utf-8')
        
