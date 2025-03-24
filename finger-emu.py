import concurrent.futures
import socket
import argparse
# 定义一个函数，用于处理每个用户名
def finger(ip, port, username):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.sendall(username.encode()+b'\n')
        res = s.recv(1)
        if b'f' in res:
            # print(f'用户 {username} 不存在')
            pass
        else:
            print(f'存在用户: {username}', end='')
            print(f'响应内容: {res}')
        s.close()
    except socket.error as e:
        print(f'连接到 {ip}:{port} 时出错: {e}')



def main():
    parser = argparse.ArgumentParser(description='Finger Emulator')

    # 添加参数
    parser.add_argument('-i', type=str, help='目标IP地址')
    parser.add_argument('-p', type=int, help='目标端口')
    parser.add_argument('-w', type=str, help='字典文件路径')

    # 解析参数
    args = parser.parse_args()
    ip = args.i
    port = args.p
    wordlist = args.w
    
    # 读取字典文件
    with open(wordlist, 'r') as f:
        usernames = f.read().splitlines()

    # 创建一个线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # 遍历用户名列表
        for username in usernames:
            # 提交任务到线程池
            executor.submit(finger, ip, port, username)

if __name__ == '__main__':
    main()
