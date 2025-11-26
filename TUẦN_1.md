# 🔗 Đồ Án: Blockchain Cơ Bản và Ví Tiền Điện Tử

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Blockchain](https://img.shields.io/badge/Blockchain-Learning-orange.svg)](https://github.com/kieutanphuoc84tv/DO_AN_BLOCKCHAIN_VI_DIEN_TU)
[![Status](https://img.shields.io/badge/Status-In%20Progress-yellow.svg)]()

## 📋 Thông Tin Đồ Án

| Thông tin | Chi tiết |
|-----------|----------|
| **Sinh viên** | Kiều Tấn Phước |
| **MSSV** | 110122144 |
| **Lớp** | DA22TTB |
| **Giảng viên** | ThS. Phan Thị Phương Nam |
| **Trường** | Đại học Trà Vinh |
| **Khoa** | Kỹ Thuật và Công Nghệ Thông Tin |

---

## 🎯 Mục Tiêu Đồ Án

Tìm hiểu và xây dựng ứng dụng **Blockchain cơ bản** và **Ví tiền điện tử** sử dụng Python, nắm vững các khái niệm:
- 🔐 Công nghệ Blockchain và cơ chế hoạt động
- 🧩 Cấu trúc Block, Hash, Nonce
- 🌐 Mạng P2P (Peer-to-Peer)
- 💰 Ví điện tử và cơ chế giao dịch

---

## 📅 Tiến Độ Thực Hiện

### 📍 Tuần 1: (10/11/2025 - 16/11/2025)

#### ✅ Mục tiêu
- [x] Tìm hiểu tổng quan về công nghệ Blockchain
- [x] Nghiên cứu nguyên lý hoạt động: block, hash, nonce, mạng P2P
- [x] Chuẩn bị môi trường: Python và các công cụ phát triển
- [x] Tạo repository GitHub cho đồ án

#### 🎉 Kết quả đạt được
- ✅ Nắm được kiến thức cơ bản về Blockchain
- ✅ Hiểu nguyên lý Hash, Block và mạng P2P
- ✅ Cài đặt thành công môi trường lập trình
- ✅ Tạo GitHub repository: [DO_AN_BLOCKCHAIN_VI_DIEN_TU](https://github.com/kieutanphuoc84tv/DO_AN_BLOCKCHAIN_VI_DIEN_TU)

#### 🛠️ Công cụ sử dụng
| Công cụ | Mục đích |
|---------|----------|
| ![Anaconda](https://img.shields.io/badge/Anaconda-44A833?style=flat&logo=anaconda&logoColor=white) | Quản lý thư viện Python |
| ![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=flat&logo=visual-studio-code&logoColor=white) | IDE lập trình |
| ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white) | Notebook để mô phỏng |

#### ⚠️ Khó khăn gặp phải
- **Vấn đề 1**: Lỗi cài đặt ứng dụng
- **Vấn đề 2**: Xung đột khi liên kết thư viện Python với Anaconda
- **Vấn đề 3**: Lỗi kernel Jupyter Notebook

#### 💡 Nguyên nhân & Giải pháp

**Xung đột môi trường:**
- ❌ Máy tính có nhiều phiên bản Python song song
- ✅ Giải pháp: Cấu hình đúng Python Interpreter trong VS Code

**Thiếu biến môi trường:**
- ❌ Chưa thiết lập Path cho Anaconda
- ✅ Giải pháp: Thêm đường dẫn Anaconda vào System Environment Variables

**Lỗi Jupyter kernel:**
- ❌ Chưa cài đặt `ipykernel`
- ✅ Giải pháp: `conda install ipykernel` và liên kết với môi trường ảo

#### 📚 Bài học kinh nghiệm
> 💡 **Tip 1**: Cài Anaconda trước, sau đó cấu hình Python environment trong VS Code
> 
> 💡 **Tip 2**: Không nên cài Jupyter riêng lẻ - dùng Jupyter tích hợp sẵn trong Anaconda
> 
> 💡 **Tip 3**: Luôn kiểm tra Python Interpreter trước khi chạy code

---

## 📖 Kiến Thức Đã Tìm Hiểu

### 1️⃣ Nguyên Lý Hoạt Động Blockchain

**Khái niệm:**
> Blockchain là sổ cái kỹ thuật số phi tập trung, lưu trữ giao dịch trên nhiều máy tính. Dữ liệu trong các khối đã ghi không thể sửa đổi nếu không thay đổi toàn bộ chuỗi phía sau.

**Cơ chế hoạt động:**
- 📦 Dữ liệu được lưu trong các **block**
- 🔗 Mỗi block chứa **hash** và liên kết với block trước đó
- ⛓️ Tạo thành một chuỗi khối liên tục

**Đặc tính nổi bật:**
- 🔒 **Bảo mật cao** - Khó can thiệp và giả mạo
- 🚫 **Hạn chế gian lận** - Mọi thay đổi đều được phát hiện
- 👁️ **Minh bạch** - Tất cả node đều có bản sao

---

### 2️⃣ Cấu Trúc Một Block

```python
class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index              # Số thứ tự block
        self.timestamp = timestamp      # Thời gian tạo block
        self.data = data                # Dữ liệu/giao dịch
        self.previous_hash = previous_hash  # Hash của block trước
        self.nonce = nonce              # Số dùng trong mining
        self.hash = self.calculate_hash()   # Hash của block hiện tại
```

**Các thành phần:**
| Thành phần | Mô tả |
|------------|-------|
| `index` | Số thứ tự của block trong chuỗi |
| `timestamp` | Thời gian tạo block |
| `data` | Nội dung giao dịch hoặc dữ liệu lưu trữ |
| `previous_hash` | Hash của block đứng trước |
| `hash` | Hash của block hiện tại |
| `nonce` | Số thay đổi liên tục trong quá trình đào (mining) |

---

### 3️⃣ Hàm Băm (Hash Function)

**Định nghĩa:**
> Chuyển đổi dữ liệu đầu vào bất kỳ thành chuỗi ký tự cố định (sử dụng **SHA-256** trong đồ án)

**Đặc điểm:**

🔹 **Ổn định**
```
Cùng dữ liệu đầu vào → Cùng một hash
```

🔹 **Nhạy cảm**
```
Thay đổi nhỏ → Hash khác hoàn toàn
Ví dụ:
"Hello"  → 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
"hello"  → 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

---

### 4️⃣ Nonce và Proof of Work

**Nonce (Number Only Used Once):**
- Số nguyên được thử liên tục khi đào block
- Mục tiêu: Tìm hash thỏa điều kiện **difficulty**

**Proof of Work:**
```python
# Ví dụ: Hash phải bắt đầu bằng 4 số 0
difficulty = 4
target = "0" * difficulty

while block.hash[:difficulty] != target:
    block.nonce += 1
    block.hash = block.calculate_hash()
```

**Quy trình:**
1. 🔄 Máy tính thử nhiều giá trị Nonce
2. 🧮 Tính lại hash với mỗi Nonce
3. ✅ Dừng khi hash đạt yêu cầu difficulty

---

### 5️⃣ Mạng Ngang Hàng (P2P Network)

**Mô hình:**
```
     Node A ←→ Node B
        ↕         ↕
     Node C ←→ Node D
```
- 🚫 Không có máy chủ trung tâm
- 📚 Mỗi node có bản sao blockchain đầy đủ

**Cơ chế đồng thuận:**
1. 📤 Block mới được gửi đến tất cả node
2. ✔️ Các node kiểm tra tính hợp lệ
3. ➕ Node đồng ý → Thêm vào chuỗi
4. 🔄 Đảm bảo dữ liệu đồng bộ và chống gian lận

---

## 🔜 Kế Hoạch Tuần Tiếp Theo

### 📍 Tuần 2: (24/11/2025 - 30/11/2025)

#### 🎯 Mục tiêu
- [ ] Nghiên cứu về **ví điện tử**
- [ ] Tìm hiểu **cơ chế giao dịch**
- [ ] Học về **khóa công khai** và **khóa riêng tư**
- [ ] Xây dựng prototype ví đơn giản

---

## 🤝 Đóng Góp

Mọi góp ý và đóng góp đều được hoan nghênh! Vui lòng tạo **Issue** hoặc **Pull Request**.

---

## 📧 Liên Hệ

- 👤 **Sinh viên**: Kiều Tấn Phước
- 📧 **Email**: 110122144@st.tvu.edu.vn
- 🔗 **GitHub**: [@kieutanphuoc84tv](https://github.com/kieutanphuoc84tv)

---

## 📜 License

Đồ án này được thực hiện cho mục đích học tập tại Trường Đại học Trà Vinh.

---

<div align="center">

**⭐ Nếu thấy hữu ích, hãy cho repo một ngôi sao! ⭐**

Made with ❤️ by Kiều Tấn Phước

</div>
