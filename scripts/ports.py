#!/usr/bin/python3

import socket
import threading
import subprocess
import os

def scan_port(host: str, port: int, open_ports: list) -> None:
    """
    Scan a single port on a given host.

    Parameters:
        host (str): The IP address of the host to scan.
        port (int): The port number to scan.
        open_ports (list): A list of open ports.

    Returns:
        None
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        s.connect((host, port))
        open_ports.append(port)
        print(f'🟢 Port {port} is open.')
        s.close()
    except (socket.timeout, ConnectionRefusedError):
        pass

def scan_ports(host: str, ports: int) -> list:
    """
    Scan ports on a given host using multiple threads.

    Parameters:
        host (str): The IP address of the host to scan.
        ports (int): The number of ports to scan.

    Returns:
        list: A list of open ports.
    """
    open_ports = []
    threads = []
    print(f'🔍 Scanning {ports} ports on {host}...')

    for port in range(1, ports):
        thread = threading.Thread(target=scan_port, args=(host, port, open_ports))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return open_ports

def scan_with_nmap(ports: int, host='127.0.0.1') -> list:
    """
    Scan ports on a given host using Nmap.

    Parameters:
        ports (int): The number of ports to scan.
        host (str, optional): The IP address of the host to scan. Defaults to '127.0.0.1'.

    Returns:
        list: A list of results from Nmap.
    """
    results = []
    print(f'🔍 Scanning {ports} ports on {host} using Nmap...')

    for port in ports:
        result = subprocess.run([f'nmap', '-T4', '-p', str(port), '-o', str(port), '-Pn', host], capture_output=True, text=True)

        if not os.path.exists('ports/'): subprocess.run(['mkdir', 'ports/'])
        subprocess.run(['mv', str(port), 'ports/'])

        if result.returncode != 0:
            print(f'❌ Error scanning port {port}.')
            continue

        if "closed" in result.stdout:
            print(f'❌ Port {port} is closed.')
            continue
        
        results.append(result.stdout)

    return results

def main() -> None:
    """
    The main entry point of the program, responsible for initiating the port scanning process.
    
    It sets the host IP address, scans all available ports, and prints the results, including the list of open ports and their count.
    
    Parameters:
        None
    
    Returns:
        None
    """
    host = input('🖥 Enter the host IP address: [127.0.0.1] ') or '127.0.0.1'
    open_ports = scan_ports(host, 65535)
    if not open_ports:
        print('❌ No open ports found.')

    print('📂 Open ports:', open_ports)
    print('🔢 Number of open ports:', len(open_ports))

    print('🔍 Scanning with Nmap...')
    results = scan_with_nmap(open_ports, host)

    if not results:
        print('❌ Scanning with nmap failed.')

    for result in results:
        print(result)

if __name__ == '__main__':
    main()
