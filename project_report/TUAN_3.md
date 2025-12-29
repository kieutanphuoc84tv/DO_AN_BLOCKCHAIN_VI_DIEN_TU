# Đồ Án: Blockchain Cơ Bản và Ví Tiền Điện Tử

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Blockchain](https://img.shields.io/badge/Blockchain-Learning-green)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

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

# BÁO CÁO TUẦN 3

## Thông tin cơ bản

- **Thời gian**: Từ 08/12/2025 đến 14/12/2025
- **Giai đoạn**: Tuần 3 - Thiết kế và xây dựng chương trình

## Nội dung công việc

### 1. Thiết kế cấu trúc Block

Tạo class Block với các thành phần:
- **index**: Số thứ tự block
- **transactions**: Danh sách giao dịch
- **previous_hash**: Hash của block trước
- **timestamp**: Thời gian tạo
- **nonce**: Giá trị dùng cho Proof of Work
- **hash**: Hash của block hiện tại

### 2. Xây dựng class Blockchain

**Các thành phần chính:**
- chain: Mảng chứa các block
- pending_transactions: Giao dịch chờ xác nhận
- difficulty: Độ khó đào (số lượng số 0 ở đầu hash)
- mining_reward: Phần thưởng đào

**Các phương thức:**
- create_genesis_block(): Tạo block đầu tiên
- get_latest_block(): Lấy block cuối cùng
- add_transaction(): Thêm giao dịch mới
- mine_pending_transactions(): Đào block mới
- get_balance(): Tính số dư ví

### 3. Xây dựng hệ thống ví điện tử

Tạo class Wallet sử dụng thư viện ecdsa:
- Tạo cặp khóa ECDSA tự động
- Phương thức ký giao dịch (sign_transaction)
- Phương thức xác minh chữ ký

### 4. Xây dựng giao diện web với Flask

**Các tính năng chính:**
- Tạo ví mới
- Xem danh sách ví
- Gửi giao dịch có chữ ký
- Bật/dừng tự động đào
- Xem Blockchain và lịch sử giao dịch

### 5. Mô phỏng quá trình đào (Mining)

Hiện thực Proof of Work:
- Thử các giá trị nonce từ 0
- Tính hash với mỗi nonce
- Tìm hash bắt đầu bằng số lượng số 0 theo độ khó
- Hiển thị quá trình thất bại và thành công

### 6. Mô phỏng mạng P2P

Tạo 4 node ảo để mô phỏng mạng phân tán:
- Node_Alpha, Node_Beta, Node_Gamma, Node_Delta
- Mô phỏng broadcast block mới đến các node
- Mô phỏng đồng bộ blockchain giữa các node
- Cho phép bật/tắt node để mô phỏng tình huống thật

## Kết quả đạt được

- Hoàn thành cấu trúc Block và Blockchain
- Hoàn thành hệ thống ví điện tử với ECDSA
- Hoàn thành giao diện web với Flask
- Hoàn thành mô phỏng Proof of Work
- Hoàn thành mô phỏng mạng P2P
- Ứng dụng chạy được trên Jupyter Notebook

## Khó khăn gặp phải

- Thiết kế giao diện để xem quá trình mining chi tiết
- Xử lý đồng bộ giữa frontend và backend
- Fix lỗi JavaScript trong việc hiển thị dữ liệu

## Kế hoạch tuần tiếp theo

Kiểm tra, sửa lỗi và hoàn thiện báo cáo, slide thuyết trình.
