class HTTPRequest:
    """Client Request.
    
    Request made by a browser to request
    a resource hosted on the server via
    the HTTP protocol.
    """
    
    def __init__(self, request: str) -> None:
        self.request = request
        fields_request = request.split('\n')
        # Request line processing
        request_line = fields_request[0]
        self.method, self.url = request_line.split(' ')[:2]
        # Header lines processing
        headers_line = [header.split(' ') for header in fields_request[1:]] # [['Host:', 'localhost'], ...]
        headers_line = {header[0][:-1]: header[1].replace('\r', '') # [:-1] -> Remove double dot
                        for header in headers_line if len(header) > 1} # {'Host': 'localhost', ...}
        # When a malformed request is received, the following headers are not provided:
        self.host = headers_line.get('Host', 'CarloFOL') 
        self.user_agent = headers_line.get('User-Agent', 'Unknown')
        
    
    def is_valid_method(self) -> bool:
        """Check if it is a valid method.
        
        The only methods that are valid
        for this practice are HEAD and GET.
        """
        return self.method in ('HEAD', 'GET')


    def __str__(self) -> str:
        """Request made.
        
        Simplified display of the request
        made by the browser.
        """
        return f'{self.method} {self.url} HTTP/1.0\nHost: {self.host}\nUser-Agent: {self.user_agent}\n'