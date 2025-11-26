#Giới thiệu đồ án: Tìm hiểu cơ bản về Blockchain và Ví Tiền Điện Tử (Python)

## 📋 Mục lục
1. [Giới thiệu về Blockchain](#giới-thiệu-về-blockchain)
2. [Mục tiêu dự án](#mục-tiêu-dự-án)
3. [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
4. [Các thành phần chính](#các-thành-phần-chính)
5. [Cài đặt và Yêu cầu](#cài-đặt-và-yêu-cầu)
6. [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
7. [API Documentation](#api-documentation)
8. [Kết quả đạt được](#kết-quả-đạt-được)

---

## 🌐 Giới thiệu về Blockchain

### Blockchain là gì?

**Blockchain** (chuỗi khối) là một công nghệ lưu trữ dữ liệu dưới dạng các khối (block) được liên kết với nhau bằng mã hóa, tạo thành một chuỗi không thể thay đổi. Mỗi block chứa:
- **Dữ liệu giao dịch**: Các giao dịch được nhóm lại
- **Hash của block**: Mã định danh duy nhất của block
- **Hash của block trước**: Liên kết với block trước đó
- **Timestamp**: Thời gian tạo block
- **Nonce**: Số ngẫu nhiên dùng trong quá trình đào (mining)

### Tác dụng và Ứng dụng của Blockchain

1. **Tính bất biến (Immutability)**
   - Dữ liệu một khi đã được ghi vào blockchain thì không thể sửa đổi hoặc xóa bỏ
   - Mỗi block có hash riêng, nếu sửa đổi sẽ làm thay đổi hash và phá vỡ chuỗi

2. **Phân tán (Decentralization)**
   - Không cần máy chủ trung tâm
   - Mỗi node trong mạng đều có bản sao của blockchain
   - Tăng tính bảo mật và độ tin cậy

3. **Minh bạch (Transparency)**
   - Tất cả giao dịch đều công khai
   - Mọi người có thể xem lịch sử giao dịch

4. **Bảo mật cao**
   - Sử dụng mã hóa (cryptography) để bảo vệ dữ liệu
   - Chữ ký số (digital signature) đảm bảo tính xác thực

5. **Ứng dụng thực tế**:
   - **Tiền điện tử**: Bitcoin, Ethereum
   - **Hợp đồng thông minh**: Tự động thực thi khi đáp ứng điều kiện
   - **Quản lý chuỗi cung ứng**: Theo dõi nguồn gốc sản phẩm
   - **Bỏ phiếu điện tử**: Đảm bảo tính minh bạch và công bằng
   - **Quản lý danh tính**: Xác thực danh tính số

### Proof of Work (Bằng chứng công việc)

**Proof of Work (PoW)** là cơ chế đồng thuận được sử dụng trong blockchain để:
- Xác minh và thêm block mới vào chuỗi
- Ngăn chặn tấn công spam và double-spending
- Thợ đào (miner) phải giải quyết bài toán khó (tìm nonce phù hợp)
- Block hợp lệ phải có hash bắt đầu bằng số số 0 nhất định (difficulty)

---

## 🎯 Mục tiêu dự án

### Mục tiêu chính

1. **Hiểu rõ nguyên lý Blockchain**
   - Nắm vững cấu trúc block, hash, nonce
   - Hiểu cơ chế Proof of Work
   - Hiểu cách các block được liên kết với nhau

2. **Xây dựng Blockchain đơn giản**
   - Tạo class `Block` và `Blockchain` bằng Python
   - Triển khai thuật toán mining (đào block)
   - Quản lý giao dịch và mempool

3. **Triển khai API RESTful**
   - Sử dụng Flask framework
   - Tạo các endpoint để tương tác với blockchain
   - Xử lý giao dịch và mining qua API

4. **Triển khai Ví điện tử và Chữ ký số**
   - Sử dụng ECDSA (Elliptic Curve Digital Signature Algorithm)
   - Tạo ví với private key và public key
   - Ký và xác thực giao dịch bằng chữ ký số

5. **Giao diện trực quan**
   - Xây dựng UI với Jupyter Widgets
   - Hiển thị blockchain, giao dịch, lịch sử đào
   - Tra cứu số dư ví

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ Jupyter UI   │  │  Wallet Tool  │  │  API Client  │ │
│  │ (Widgets)    │  │  (ECDSA)      │  │  (Requests)  │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    API LAYER (Flask)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  /chain  │  │   /mine  │  │/add_trans│  │    /     │ │
│  │   GET    │  │   POST   │  │  POST    │  │   GET    │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                 BLOCKCHAIN CORE                          │
│  ┌──────────────┐         ┌──────────────┐              │
│  │    Block     │         │  Blockchain  │              │
│  │ - index      │◄───────►│ - chain[]    │              │
│  │ - hash       │         │ - difficulty │              │
│  │ - nonce      │         │ - pending_tx │              │
│  │ - timestamp  │         │ - mining_hist│              │
│  │ - transactions│        └──────────────┘              │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Các thành phần chính

### 1. Block (Khối)

**Block** là đơn vị cơ bản của blockchain, chứa:

```python
class Block:
    - index:          Số thứ tự block
    - transactions:   Danh sách giao dịch
    - previous_hash:  Hash của block trước đó
    - timestamp:      Thời gian tạo block
    - nonce:          Số ngẫu nhiên dùng trong mining
    - hash:           Mã hash của block (SHA-256)
```

**Tính năng:**
- `calculate_hash()`: Tính toán hash của block
- `mine_block(difficulty)`: Đào block bằng cách tìm nonce phù hợp

### 2. Blockchain (Chuỗi khối)

**Blockchain** quản lý toàn bộ chuỗi các block:

```python
class Blockchain:
    - chain:                  Danh sách các block
    - difficulty:             Độ khó mining (số số 0 đầu hash)
    - pending_transactions:   Giao dịch đang chờ
    - mining_reward:          Phần thưởng cho thợ đào
    - mining_history:         Lịch sử đào block
```

**Tính năng:**
- `add_transaction()`: Thêm giao dịch vào mempool
- `mine_pending_transactions()`: Đào block mới từ giao dịch đang chờ
- `get_latest_block()`: Lấy block mới nhất

### 3. Wallet (Ví điện tử)

**Wallet** sử dụng ECDSA để tạo và quản lý khóa:

```python
- Private Key:  Khóa bí mật (dùng để ký giao dịch)
- Public Key:   Khóa công khai (dùng để xác thực)
```

**Tính năng:**
- `create_wallet()`: Tạo cặp khóa mới
- `sign_transaction()`: Ký giao dịch bằng private key
- Xác thực chữ ký bằng public key

### 4. API Server (Flask)

**Flask API** cung cấp các endpoint:

- `GET /`: Trang chủ, hiển thị thông tin API
- `GET /chain`: Lấy toàn bộ blockchain
- `POST /add_transaction`: Thêm giao dịch mới
- `POST /mine`: Đào block mới

### 5. Giao diện Jupyter

**Jupyter Widgets UI** cung cấp:
- Form gửi giao dịch
- Nút đào block với hiển thị kết quả
- Tra cứu số dư ví
- Tabs hiển thị: Blockchain, Lịch sử đào, Giao dịch

---

## 📦 Cài đặt và Yêu cầu

### Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **Hệ điều hành**: Windows, Linux, hoặc macOS
- **Jupyter Notebook**: Để chạy giao diện trực quan

### Cài đặt thư viện

**Cách 1: Sử dụng requirements.txt**

```powershell
python -m pip install -r "d:\CODE PYTHON\requirements.txt"
```

**Cách 2: Cài đặt trực tiếp trong Jupyter**

```python
%pip install networkx matplotlib flask requests ecdsa streamlit pytest ipywidgets pandas
```

### Các thư viện chính

- **flask**: Framework web để tạo API
- **ecdsa**: Thư viện mã hóa cho ví điện tử
- **ipywidgets**: Tạo giao diện tương tác trong Jupyter
- **pandas**: Xử lý và hiển thị dữ liệu dạng bảng
- **hashlib**: Tính toán hash (SHA-256)

---

## 🚀 Hướng dẫn sử dụng

### Bước 1: Khởi động Jupyter Notebook

Mở file `DOANTIMHIEUBLOCKCHAINVAVITIEN.ipynb` trong Jupyter hoặc VS Code.

### Bước 2: Chạy các cell theo thứ tự

#### Cell 1: Cài đặt thư viện
```python
pip install networkx matplotlib flask requests ecdsa
```

#### Cell 2: Tạo ví và ký giao dịch
- Tạo ví mới với `create_wallet()`
- Ký giao dịch với `sign_transaction()`
- Copy JSON để gửi lên API

#### Cell 3: Khởi động Flask Server
- Chạy cell này để khởi động API server
- Server sẽ chạy tại `http://127.0.0.1:5000`

#### Cell 4: Giao diện Jupyter (Demo trực quan)
- Sử dụng các form để:
  - Gửi giao dịch
  - Đào block
  - Tra cứu số dư
- Xem kết quả trong các tabs

### Bước 3: Sử dụng API (Tùy chọn)

#### Thêm giao dịch
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/add_transaction -Method Post `
  -Body (ConvertTo-Json @{
    sender="Alice"
    receiver="Bob"
    amount=10.5
    signature="..."
  }) -ContentType 'application/json'
```

#### Đào block
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/mine -Method Post `
  -Body (ConvertTo-Json @{miner="Miner_1"}) -ContentType 'application/json'
```

#### Xem blockchain
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/chain -Method Get
```

---

## 📡 API Documentation

### Base URL
```
http://127.0.0.1:5000
```

### Endpoints

#### 1. GET `/`
**Mô tả**: Trang chủ, hiển thị thông tin về API

**Response:**
```json
{
  "message": "🚀 Blockchain API Server đang chạy!",
  "endpoints": {
    "GET /chain": "Xem toàn bộ blockchain",
    "POST /add_transaction": "Thêm giao dịch mới",
    "POST /mine": "Đào block mới"
  }
}
```

#### 2. GET `/chain`
**Mô tả**: Lấy toàn bộ blockchain

**Response:**
```json
{
  "length": 3,
  "chain": [
    {
      "index": 0,
      "transactions": [],
      "previous_hash": "0",
      "timestamp": 1234567890.123,
      "nonce": 0,
      "hash": "abc123..."
    }
  ]
}
```

#### 3. POST `/add_transaction`
**Mô tả**: Thêm giao dịch mới vào mempool

**Request Body:**
```json
{
  "sender": "public_key_hex",
  "receiver": "receiver_address",
  "amount": 15.5,
  "signature": "signature_hex"
}
```

**Response:**
- `201`: Giao dịch đã được thêm thành công
- `406`: Chữ ký không hợp lệ
- `500`: Lỗi server

#### 4. POST `/mine`
**Mô tả**: Đào block mới từ các giao dịch đang chờ

**Request Body:**
```json
{
  "miner": "miner_address"
}
```

**Response:**
```json
{
  "message": "Đào thành công",
  "block_index": 2
}
```

---

## ✅ Kết quả đạt được

### Tính năng đã hoàn thành

1. ✅ **Blockchain Core**
   - Tạo và quản lý chuỗi block
   - Thuật toán Proof of Work
   - Tính toán hash (SHA-256)
   - Liên kết block bằng previous_hash

2. ✅ **Ví điện tử**
   - Tạo cặp khóa ECDSA
   - Ký giao dịch bằng private key
   - Xác thực chữ ký bằng public key

3. ✅ **API Server**
   - RESTful API với Flask
   - Endpoints đầy đủ cho các chức năng
   - Xử lý lỗi và validation

4. ✅ **Giao diện trực quan**
   - UI với Jupyter Widgets
   - Hiển thị blockchain, giao dịch, lịch sử
   - Tra cứu số dư
   - Thống kê mining

5. ✅ **Tài liệu**
   - README đầy đủ
   - Giải thích chi tiết các thành phần
   - Hướng dẫn sử dụng

### Kiến thức đã học được

- ✅ Hiểu rõ cấu trúc và nguyên lý blockchain
- ✅ Nắm vững Proof of Work
- ✅ Thực hành mã hóa và chữ ký số
- ✅ Tạo giao diện tương tác với Python

### Ứng dụng thực tế

Dự án này có thể được mở rộng thành:
- Hệ thống thanh toán phi tập trung
- Ứng dụng quản lý tài sản số
- Hệ thống bỏ phiếu điện tử
- Quản lý chuỗi cung ứng

---

## 📝 Ghi chú

- Đây là phiên bản mô phỏng đơn giản, không phù hợp cho môi trường production
- Độ khó mining có thể điều chỉnh trong code (mặc định: 3)
- Phần thưởng mining mặc định: 50 coin
- Blockchain được lưu trong memory, sẽ mất khi tắt server

---

## 👨‍💻 Tác giả

Đồ án được thực hiện bởi sinh viên trong môn học về Blockchain và Tiền điện tử.

---

## 📚 Tài liệu tham khảo

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Blockchain Explained](https://www.investopedia.com/terms/b/blockchain.asp)
- [ECDSA Documentation](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)
- [Flask Documentation](https://flask.palletsprojects.com/)





