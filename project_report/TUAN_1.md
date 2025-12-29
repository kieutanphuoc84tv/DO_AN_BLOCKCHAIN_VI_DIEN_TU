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

# BÁO CÁO TUẦN 1

## Thông tin cơ bản

- **Thời gian**: Từ 10/11/2025 đến 16/11/2025
- **Giai đoạn**: Tuần 1 - Nghiên cứu lý thuyết Blockchain

## Nội dung công việc

### 1. Tìm hiểu tổng quan về công nghệ Blockchain

Blockchain là một công nghệ lưu trữ dữ liệu theo cấu trúc chuỗi khối, trong đó mỗi khối (block) chứa thông tin giao dịch và được liên kết với khối trước đó thông qua giá trị băm (hash). Đặc điểm quan trọng của Blockchain là tính bất biến - một khi dữ liệu đã được ghi vào, không thể sửa đổi mà không làm thay đổi toàn bộ chuỗi.

### 2. Nguyên lý hoạt động

Blockchain hoạt động dựa trên các nguyên tắc sau:
- Phi tập trung (Decentralized): Không có máy chủ trung tâm, dữ liệu được phân tán trên nhiều node
- Minh bạch (Transparent): Tất cả giao dịch đều công khai và có thể kiểm tra
- Bất biến (Immutable): Dữ liệu đã ghi không thể thay đổi
- Đồng thuận (Consensus): Các node phải đồng ý về trạng thái của chuỗi

### 3. Cấu trúc Block

Mỗi block trong Blockchain bao gồm các thành phần:
- **Index**: Số thứ tự của block trong chuỗi
- **Timestamp**: Thời gian tạo block
- **Transactions**: Danh sách các giao dịch
- **Previous Hash**: Giá trị băm của block trước đó
- **Nonce**: Giá trị số được điều chỉnh để tìm hash hợp lệ
- **Hash**: Giá trị băm của block hiện tại

### 4. Hàm băm SHA-256

SHA-256 (Secure Hash Algorithm 256-bit) là hàm băm một chiều được sử dụng rộng rãi trong Blockchain. Đặc điểm:
- Đầu ra luôn có độ dài cố định 256 bit (64 ký tự hex)
- Thay đổi nhỏ trong đầu vào sẽ tạo ra đầu ra hoàn toàn khác
- Không thể tính ngược từ hash ra dữ liệu gốc

### 5. Nonce và Proof of Work

Nonce là một số nguyên được điều chỉnh liên tục trong quá trình đào (mining). Máy đào sẽ thử lần lượt các giá trị nonce cho đến khi tìm được hash thỏa mãn điều kiện độ khó (ví dụ: bắt đầu bằng một số lượng số 0 nhất định).

### 6. Mạng P2P (Peer-to-Peer)

Blockchain sử dụng mạng ngang hàng P2P để phân tán dữ liệu:
- Mỗi node giữ một bản sao của toàn bộ blockchain
- Khi có block mới, nó được broadcast đến tất cả các node
- Các node xác minh và đồng bộ blockchain

## Kết quả đạt được

- Hiểu rõ nguyên lý hoạt động cơ bản của Blockchain
- Nắm vững cấu trúc của một block và cách liên kết giữa các block
- Hiểu cách hàm băm SHA-256 hoạt động và vai trò trong Blockchain
- Hiểu cơ chế Proof of Work và vai trò của nonce
- Hiểu kiến trúc mạng P2P trong hệ thống Blockchain

## Khó khăn gặp phải

- Cần thời gian để hiểu rõ các khái niệm kỹ thuật phức tạp
- Tài liệu tiếng Việt còn hạn chế

## Kế hoạch tuần tiếp theo

Nghiên cứu về ví điện tử, cơ chế giao dịch, lưu trữ khóa công khai và khóa bí mật.
