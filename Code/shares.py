class Share:
    '''
    A standard shared variable. Values can be accessed with read() or changed with write()
    '''
    def __init__(self, initial_value=None):
        '''
        Constructs a shared variable
            
        :param initial_value:     initial_value An optional initial value for the shared variable.
        '''
        self._buffer = initial_value
    
    def write(self, item):
        '''
        Updates the value of the shared variable.
       
        :param item:    The new value for the shared variable.
        '''
        self._buffer = item
        
    def read(self):
        '''
        Access the value of the shared variable
        
        :return: The value of the shared variable
        '''
        return self._buffer

class Queue:
    '''
    A queue of shared data. Values can be accessed with placed into queue with put() or
    removed from the queue with get(). Check if there are items in the queue with num_in() 
    before using get().
    '''
    def __init__(self):
        '''
        Constructs an empty queue of shared values
        '''
        self._buffer = []
    
    def put(self, item):
        '''
        Adds an item to the end of the queue.
            
        :param item: The new item to append to the queue.
        '''
        self._buffer.append(item)
        
    def get(self):
        '''
        Remove the first item from the front of the queue
        
        :return: The value of the item removed
        '''
        return self._buffer.pop(0)
    
    def num_in(self):
        '''
        Find the number of items in the queue. Call before get().
        
        :return: The number of items in the queue
        '''
        return len(self._buffer)