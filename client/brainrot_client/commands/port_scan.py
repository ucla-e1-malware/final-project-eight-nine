from ..commands import Command

import socket

HTTP_GET_HEADER = "GET / HTTP/1.1\n\n"
HTTP_SERVER_PREFIX = "Server: "
def parseHttpServerVersion(response: str):
	for line in response.split('\n'):
		if line.startswith(HTTP_SERVER_PREFIX):
			return line[len(HTTP_SERVER_PREFIX):]
	return None

def scan_ip(target: str, port_range: tuple[int, int], do_service_scan = False) -> list[tuple[int, str]]:

	open_ports = [] 

	start_port, end_port = port_range

	if do_service_scan:
		for port in range(start_port, end_port + 1):
			service = None
			try:
				client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				client_socket.settimeout(1)
				client_socket.connect((target, port))
				
				response = client_socket.recv(2048) # *Tries* to get 2048 bytes of data
				service = response.decode().strip()

				# close socket
				client_socket.close()
			except: pass

			if service==None:
				try:
					client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					client_socket.settimeout(1)
					client_socket.connect((target, port))

					client_socket.send(HTTP_GET_HEADER.encode())
					
					response = client_socket.recv(2048) # *Tries* to get 2048 bytes of data
					httpResponse = response.decode().strip()

					serverVersion = parseHttpServerVersion(httpResponse)
					if serverVersion != None: service = "HTTP: "+serverVersion
					
					client_socket.close()
				except: pass
			
			if service != None:
				open_ports.append((port, service))


		return open_ports
	
	else:
		for port in range(start_port, end_port + 1): 

			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(0.5)
			result = sock.connect_ex((target, port))
			if result == 0:
				try: 
					service = socket.getservbyport(port)
				except OSError:
					service = "unknown"
				
				open_ports.append((port, service))
			sock.close()

		return open_ports
	

def pretty_print_scan(open_ports: list[int]) -> None:

	print("   Port      Service   ")
	print("-----------------------")

	for port, service in open_ports:
		print(f"   {port}      {service}   ")


class PortScan(Command):
	"""
	Scan ports on a target host

	"""

	def do_command(self, lines: str, *args): 

		tokens = lines.split()

		if len(tokens) < 3:
			print("Usage: port_scan <host> <start_port> <end_port> [--service-scan]")
			return

		host = tokens[0]
		start_port = int(tokens[1])
		end_port = int(tokens[2])
		do_service_scan = len(tokens)>=4 and tokens[3] == "--service-scan"

		open_ports = scan_ip(host, (start_port, end_port), do_service_scan=do_service_scan)
		pretty_print_scan(open_ports)

command = PortScan