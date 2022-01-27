from readerwriterlock import rwlock

class message_bus:
    """
    A class for passing data on buses
    
    ...
    
    Attributes
    ----------
    message : optional
        data to be written to/read from bus
    lock :
        read writen lock for concurrent processes    
    
    """
    def __init__(self):
        """
        Parameters
        ----------
        message : optional
            data to be written to / read from bus
        lock : 
            prevent read/write issues of concurrent processes
        """
        
        self.message = None
        self.lock = rwlock.RWLockWriteD()
        
    def write(self, new_message):
        """
        Method that writes new_message data to bus object
        """
        with self.lock.gen_wlock():
            self.message = new_message
        # print(f'{new_message} written to bus')
        
    def read(self):
        """
        Method that reads from and returns what is written
        to data bus object
        """
        with self.lock.gen_rlock():
            return self.message
    
