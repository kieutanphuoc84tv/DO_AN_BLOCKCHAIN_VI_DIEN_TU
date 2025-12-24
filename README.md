# Đồ Án: Blockchain Cơ Bản và Ví Tiền Điện Tử

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask&logoColor=white)
![Blockchain](https://img.shields.io/badge/Blockchain-Demo-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## Thông Tin Đồ Án

| Thông tin | Chi tiết |
|-----------|----------|
| **Sinh viên** | Kiều Tấn Phước |
| **MSSV** | 110122144 |
| **Lớp** | DA22TTB |
| **Giảng viên** | ThS. Phan Thị Phương Nam |
| **Trường** | Đại học Trà Vinh |
| **Khoa** | Kỹ Thuật và Công Nghệ Thông Tin |

---

## Giới Thiệu

Đây là ứng dụng mô phỏng hệ thống **Blockchain** và **Ví tiền điện tử**, được xây dựng bằng Python với giao diện web Flask. Ứng dụng giúp người dùng hiểu rõ nguyên lý hoạt động của công nghệ Blockchain thông qua giao diện trực quan và các tính năng tương tác.

---

## Tính Năng Chính

### Blockchain
- Cấu trúc block hoàn chỉnh (index, hash, previous_hash, nonce, transactions, timestamp)
- Proof of Work với độ khó có thể điều chỉnh
- Mô phỏng quá trình đào với hiển thị thất bại/thành công real-time
- Blockchain Explorer để xem toàn bộ chuỗi

### Ví Điện Tử
- Tạo ví với cặp khóa ECDSA (Elliptic Curve Digital Signature Algorithm)
- Hiển thị khóa công khai và khóa bí mật
- Kiểm tra số dư theo thời gian thực

### Giao Dịch
- Tạo giao dịch giữa các ví
- Ký giao dịch bằng chữ ký số ECDSA
- Xác minh chữ ký tự động

### Mạng P2P
- Mô phỏng 4 node mạng (Alpha, Beta, Gamma, Delta)
- Broadcast block mới đến các node
- Đồng bộ blockchain giữa các node
- Bật/tắt node để mô phỏng tình huống thực tế

---

## Cài Đặt

### Yêu Cầu
- Python 3.8 trở lên
- pip (Python package manager)

### Các Bước Cài Đặt

1. **Clone repository**
```bash
git clone https://github.com/kieutanphuoc84tv/DO_AN_BLOCKCHAIN_VI_DIEN_TU.git
cd DO_AN_BLOCKCHAIN_VI_DIEN_TU
```

2. **Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

3. **Chạy ứng dụng**
```bash
# Mở file Jupyter Notebook
jupyter notebook DOANTIMHIEUBLOCKCHAINVAVITIEN.ipynb
```

4. **Truy cập ứng dụng**
```
http://127.0.0.1:5000
```

---

## Hướng Dẫn Sử Dụng

### 1. Tạo Ví
- Nhập tên ví vào ô "Tên định danh ví"
- Nhấn "Tạo Ví Mới"
- Ví mới sẽ xuất hiện trong danh sách

### 2. Gửi Giao Dịch
- Chọn ví gửi và ví nhận
- Nhập số lượng coin
- Nhấn "Thực hiện Giao dịch"
- Giao dịch sẽ được ký tự động và đưa vào hàng đợi

### 3. Đào Block
- Chọn ví nhận thưởng
- Nhấn "Bắt đầu Đào"
- Quan sát quá trình đào với các lần thử thất bại/thành công
- Phần thưởng 50 coin cho mỗi block

### 4. Xem Mạng P2P
- Chuyển sang tab "Mạng P2P"
- Xem trạng thái các node
- Thử tắt/bật node để xem broadcast hoạt động

---

## Cấu Trúc Thư Mục

```
DO_AN_BLOCKCHAIN_VI_DIEN_TU/
├── DOANTIMHIEUBLOCKCHAINVAVITIEN.ipynb  # Jupyter Notebook chính
├── blockchain_flask_jupyter.py           # Code Python
├── requirements.txt                       # Thư viện cần cài
├── README.md                              # Tài liệu này
└── BAO_CAO_TUAN/                          # Báo cáo tuần
    ├── CHUAN_BI.md
    ├── TUAN_1.md
    ├── TUAN_2.md
    ├── TUAN_3.md
    ├── TUAN_4.md
    └── KET_THUC.md
```

---

## Công Nghệ Sử Dụng

| Công nghệ | Mục đích |
|-----------|----------|
| **Python** | Ngôn ngữ lập trình chính |
| **Flask** | Web framework |
| **ECDSA** | Thuật toán chữ ký số |
| **SHA-256** | Hàm băm |
| **Jupyter Notebook** | Môi trường phát triển |

---

## Tác Giả

**Kiều Tấn Phước** - Sinh viên Đại học Trà Vinh


