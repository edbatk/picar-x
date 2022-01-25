from readerwriterlock import rwlock

class message_bus:
    def __init__(self):
        self.message = None
        self.lock = rwlock.RWLockWriteD()
        
    def write(self, new_message):
        with self.lock.gen_wlock():
            self.message = new_message
        # print(f'{new_message} written to bus')
        
    def read(self):
        with self.lock.gen_rlock():
            return self.message
    
