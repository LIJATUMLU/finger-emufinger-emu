import concurrent.futures
import socket
import argparse

def finger(ip, port, username):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.sendall(username.encode()+b'\n')
        res = s.recv(1)
        if b'f' in res:
            # print(f'user {username} undefine')
            pass
        else:
            print(f'username: {username}', end='')
            print(f'respond: {res}')
        s.close()
    except socket.error as e:
        print(f'access {ip}:{port} ->error: {e}')
def main():
    parser = argparse.ArgumentParser(description='Finger Emulator')
    parser.add_argument('-i', type=str, help='target IP')
    parser.add_argument('-p', type=int, help='TARGET port')
    parser.add_argument('-w', type=str, help='PATH of worldlists ')

    args = parser.parse_args()
    ip = args.i
    port = args.p
    wordlist = args.w
    
    with open(wordlist, 'r') as f:
        usernames = f.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for username in usernames:
            executor.submit(finger, ip, port, username)

if __name__ == '__main__':
    main()
