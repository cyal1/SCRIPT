import paramiko

# https://www.cnblogs.com/breezey/p/6663546.html

ssh_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA4Rrl+76ioaFmMveYoz4fF5sNXo5OEbx2YQgySwbfimjYfLWF
0AVeHCW/0JwI42AOkBGmEcrZBUwUUsh1I6Q0FxeasCkiE49KYEbeadcqA3uEjnyV
lr2SuyRdCs+nZqUS2O5WRpbqnbBzRUYziRlNC8qmXBu7msPj1zSGQHcv2ht3l9S7
RBFNnydtEEBPgEqr8qyUTPoyqyCfilXdyV1XqMIIQaIG0JU4zZrk6Fm+Nuv8TcVA
Sn7RnUUkO0cplFf+8A6t74WCedFhRt1Drw7yOv/T/aQQw3uWTM+DTzcdjWZloMrd
YlEEMhcbzT6fHSE1IHk8Ok4PVE869TmjmLW96QIDAQABAoIBAAxw1iERqh9QsjtC
39a1yjYc40JEjx//0HMQZucqnBQkM0LBLYIPqeHYXD+FQCCA4I0pzInTMidOyxjA
J2ku3AoirdPqkg2Or8eeYxBqadIDc5IEZKgOFhvtqI6+ZzwPB3mhwnboRFMuu1Aq
zxJWqaFrM8KHbdjh1qfAKWNKswRUwbPEg1EWJCqWYo7WTDETxXaatxWvYTLNPy5q
cEyafYhbY2yI1kIMFcKO63awDBE5V62yVXUbShCEWmv0te0QyTpLCx3fw8WZ/g14
i6/QIA6ZwjyOHGiWK4JBmmSqeAXf28FOEkIuBzUf2LdOHpnFqRJ07wEj9pdM7JQq
EyUIL+ECgYEA/zAvnVQqYtMiykf6YMa41y8YPCFhBp5s0lGe6hgmIVp/+jBrWNCD
leTLXB9PdsdObS47hDyuceH/7lBWxzWH4AW3D5lFuQmAh8gDx8QWus7lVuN+N8FY
gDv9BVA51HbsW/BaY7s5AzP2Ao1dCwVz3ZQW2cBVwPzGhfTopqR1a4UCgYEA4dI2
x+DQoqcVqMY70se1RhtZs+IzVOOtTORZvwiE8xm/vO7YVm/b7w5dLIGMIk9tbvYe
gN1Gd35QvFPjYzv9DU+JIrmP0hs8GCe7Aptl63YnJtnyUzvZZ72f+zh2GSSe9WSK
zHiRDMkLn5mVrPquIWZbx2atQ4JmXZCY2NRZ/BUCgYEA0R3ilvGmvk843jy3r+CJ
DkVYfcX4pZzjnkImkLzzWje4UgSloyVT/1x7TWWXD8Xpvcy6FvZHGanSua76Pcrf
KrRkPBMlMKnZuussNeK5oaH0DAzmnLgDVypRgK4qhbJipEDFQZ7l7HsDKTpAucxh
E33Mb+qOG1TJNnLox85TLqUCgYBg126Irx+p8S93rnNvRBe4FfiVDPdoey8Rn4fh
Rb0GJ8+zLVZ3UwclcKqCcJfxCtDqWf/g0YPrsK7c5LjKEKrHr4km7B8CQo216ivn
xU6i+It3vNWP3kWwmIBoEuGKjMrif5iKcVX6/qjOa+XlRaexSR0o2R6KqfxOObli
m0ZvtQKBgQCg9aIvkPSHYKro/GP7JCxgNhEO1N6nO66egd3bmdIoaqekzQ2Ql9Fg
LAF2KrUSQzCLsNE9AhcFO9rAQhO54445ujEM8O1aGYOtdvxj2fdcs2+UlXViMWUu
TmaKbdDJNBr0dhnr3Li1cHIzPU9E7ZryaxjCTNoL1sR8VrEffLSLUw==
-----END RSA PRIVATE KEY-----

"""

try:
    with open('ssh_key.txt', 'w') as f:
        f.write(ssh_key)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for team in range(1,61):
        # ssh.connect(f'10.0.{team}.2', port=port, username='root', key_filename='./ssh_key.txt',timeout=timeout) 
        ssh.connect(f'10.0.{team}.2',22, "root", "root", timeout = 8)
        # sql = 'sed -i s/#bind-address/bind-address/g /etc/mysql/mysql.conf.d/mysqld.cnf'
        sql = 'sed -i s/fonts\\.googleapis\\.com/127\\.0\\.0\\.1/g /var/www/html/index.php'
        try:
            # stdin, stdout, stderr = ssh.exec_command(f"mysql -uroot -e '{sql}'")
            stdin, stdout, stderr = ssh.exec_command(sql)
        except Exception as e:
            print(e)
        print(f'10.0.{team}.2 has changed')
        ssh.close()
except Exception as e:
    print(e)
