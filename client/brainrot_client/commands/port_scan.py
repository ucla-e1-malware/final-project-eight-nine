from ..commands import Command

import socket

def scan_ip(target: str, port_range: tuple[int, int]) -> list[int]:

    open_ports = [] 

    start_port, end_port = port_range

    for port in range(start_port, end_port + 1): 

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0: 
            open_ports.append(port)

        sock.close()

    return open_ports
    

def pretty_print_scan(open_ports: list[int]) -> None:

    print("   Port      Service   ")
    print("-----------------------")

    for port in open_ports:

        try: 
            service = socket.getservbyport(port)
        except OSError:
            service = "unknown"

        print(f"   {port}      {service}   ")


class PortScan(Command):
    """
    Scan ports on a target host

    """

    def do_command(self, lines: str, *args): 

        tokens = lines.split()

        if len(tokens) != 3:
            print("Usage: port_scan <host> <start_port> <end_port>")
            return

        host = tokens[0]
        start_port = int(tokens[1])
        end_port = int(tokens[2])

        open_ports = scan_ip(host, (start_port, end_port))
        pretty_print_scan(open_ports)

command = PortScan