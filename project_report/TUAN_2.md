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

# BÁO CÁO TUẦN 2

## Thông tin cơ bản

- **Thời gian**: Từ 24/11/2025 đến 30/11/2025
- **Giai đoạn**: Tuần 2 - Nghiên cứu ví điện tử và cơ chế giao dịch

## Nội dung công việc

### 1. Nghiên cứu về ví điện tử (Cryptocurrency Wallet)

Ví điện tử là công cụ quản lý khóa và thực hiện giao dịch trên mạng Blockchain. Một ví bao gồm:
- **Khóa bí mật (Private Key)**: Chuỗi ký tự bí mật, dùng để ký giao dịch
- **Khóa công khai (Public Key)**: Được tạo từ khóa bí mật, dùng để nhận tiền
- **Địa chỉ ví (Address)**: Phiên bản rút gọn của khóa công khai

### 2. Cơ chế tạo cặp khóa

Sử dụng thuật toán ECDSA (Elliptic Curve Digital Signature Algorithm) với đường cong SECP256k1:
- Tạo khóa bí mật ngẫu nhiên 256 bit
- Tính khóa công khai từ khóa bí mật bằng phép nhân trên đường cong elliptic
- Địa chỉ ví là hash của khóa công khai

### 3. Cơ chế giao dịch

Một giao dịch bao gồm các bước sau:
1. Người gửi tạo giao dịch với thông tin: người gửi, người nhận, số tiền
2. Người gửi ký giao dịch bằng khóa bí mật của mình
3. Giao dịch được broadcast lên mạng
4. Các node xác minh chữ ký bằng khóa công khai của người gửi
5. Giao dịch hợp lệ được đưa vào block tiếp theo

### 4. Chữ ký số ECDSA

Chữ ký số đảm bảo:
- **Xác thực (Authentication)**: Chứng minh giao dịch do chủ sở hữu ví tạo ra
- **Toàn vẹn (Integrity)**: Giao dịch không bị sửa đổi sau khi ký
- **Không chối bỏ (Non-repudiation)**: Người ký không thể phủ nhận đã ký

**Quy trình ký:**
1. Tạo hash của dữ liệu giao dịch
2. Sử dụng khóa bí mật để tạo chữ ký từ hash
3. Chữ ký được đính kèm vào giao dịch

**Quy trình xác minh:**
1. Lấy chữ ký và dữ liệu giao dịch
2. Sử dụng khóa công khai để xác minh chữ ký
3. Nếu hợp lệ, giao dịch được chấp nhận

### 5. Lưu trữ khóa

Các phương pháp lưu trữ khóa bí mật:
- Lưu trong file được mã hóa
- Lưu trong phần mềm ví (wallet software)
- Lưu trong ví cứng (hardware wallet)
- Ghi ra giấy (paper wallet)

## Kết quả đạt được

- Hiểu cấu trúc và chức năng của ví điện tử
- Nắm rõ cơ chế tạo cặp khóa công khai và bí mật
- Hiểu quy trình giao dịch và vai trò của chữ ký số
- Hiểu cách xác minh giao dịch bằng chữ ký ECDSA
- Sẵn sàng cho việc thiết kế và xây dựng ứng dụng

## Khó khăn gặp phải

- Mật mã học đường cong elliptic là khái niệm phức tạp
- Cần tìm hiểu thêm về bảo mật khóa bí mật

## Kế hoạch tuần tiếp theo

Thiết kế cấu trúc block và bắt đầu xây dựng chương trình mô phỏng bằng Python.
