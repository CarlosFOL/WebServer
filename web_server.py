from HTTPComunication import HTTPRequest, HTTPResponse
from random import randint
from socket import AF_INET, SOCK_STREAM
import socket as sock
import threading


class WebServer:
  """
  A simple web server that uses a socket interface to establish TCP connections 
  with various browsers simultaneously. Through these connections, it receives 
  their requests and parses the structure of these messages to generate the 
  correct HTTP response.
  
  Attribute
  ---------
  port: int
    Port number where the Web server will listen the requests. 
  socketServer: socket
    Socket interface that supports TCP connections. 
  """
  
  
  def __init__(self, port: int) -> None:
    self.port = port
    self.socketServer = sock.socket(family=AF_INET, type = SOCK_STREAM)


  def thread(self, conn) -> None:
    """
    It creates a thread to handle a particular TCP non-persistent 
    connection accepted by the web server. It takes care of 
    processing and sending the proper http response. 
    """
    mensaje = conn.recv(4096)
    if mensaje:
      request = HTTPRequest(request=mensaje.decode('UTF-8'))
      response = HTTPResponse(request=request)
      print(f"{'-'*60}\nBrowser:\n{request}")
      print(f"{response}\n{'-'*60}\n\n")
      conn.send(response.get_response())
    else:
      print('Cerrando conexión')
    conn.close()
  
  
  def start_listening(self) -> None:
    """
    It associates the socket with any available local address 
    on the specified port, enabling it to start listening for 
    requests from multiple browsers.
    """
    try:
      self.socketServer.bind(("", self.port))
      # Set a random timeout
      self.socketServer.settimeout(300)
      self.socketServer.listen()
      print(f'Starting server on port: {self.port}')
      while True:
        conn, addr = self.socketServer.accept()
        print('Connection accepted from {}:{}'.format(addr[0], addr[1]))
        # It starts a new thread
        threading.Thread(target=self.thread, args=(conn,)).start()
    except (sock.timeout, KeyboardInterrupt):
      print('The server is closing...')
    finally:
      self.socketServer.close()
      

   
def main():
  random_port = randint(1024, 65535)
  web_server = WebServer(port=random_port)
  web_server.start_listening()
  


if __name__ == "__main__":
	main()