class Poll_Object():

    _poll_id = ''
    _poll_name = ''    
    _connection_string = ''
    
    def __init__(self, poll_data: dict):
        self._poll_id = poll_data['poll_id']
        self._poll_name = poll_data['poll_name']
        self._connection_string = poll_data['connection_string']

    # def __str__(self):
    #     print(self._poll_name)

    @property
    def poll_id(self):
        return self._poll_id

    @poll_id.setter
    def poll_id(self, value):
        self._poll_id = value

    @property
    def poll_name(self):
        return self._poll_name

    @poll_name.setter
    def poll_name(self, value):
        self._poll_name = value

    @property
    def connection_string(self):
        return self._connection_string

    @connection_string.setter
    def connection_string(self, value):
        self._connection_string = value