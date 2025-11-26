# 📚 BÁO CÁO ĐỒ ÁN TUẦN 1: TÌM HIỂU VỀ BLOCKCHAIN CƠ BẢN VÀ VÍ TIỀN ĐIỆN TỬ

|  |
| :---: |
| [cite_start]**TRƯỜNG ĐẠI HỌC TRÀ VINH** **- KHOA KỸ THUẬT VÀ CÔNG NGHỆ THÔNG TIN** [cite: 1, 2] |

---

## 📝 THÔNG TIN CHUNG VỀ ĐỒ ÁN

| Mục | Chi tiết |
| :--- | :--- |
| **Họ và tên** | [cite_start]Kiều Tấn Phước [cite: 5] |
| **MSSV** | [cite_start]110122144 [cite: 6] |
| **Lớp** | [cite_start]DA22TTB [cite: 7] |
| **Đề tài** | [cite_start]Tìm hiểu về BlockChain cơ bản và ví tiền điện tử [cite: 8] |
| **Giảng viên hướng dẫn** | [cite_start]ThS.Phan Thị Phương Nam [cite: 9] |
| **Repository GitHub** | [cite_start]`kieutanphuoc84tv/DO_AN_BLOCKCHAIN_VI_DIEN_TU` [cite: 15] |

---

## [cite_start]I. TƯỜNG TRÌNH ĐỒ ÁN TUẦN 1 (10/11/2025 - 16/11/2025) [cite: 11]

### [cite_start]🎯 Mục tiêu [cite: 12]

* [cite_start]Tìm hiểu tổng quan về công nghệ Blockchain nguyên lý hoạt động, cấu trúc block, hash, nonce và mạng P2P[cite: 13].
* [cite_start]Chuẩn bị ngôn ngữ lập trình python và các phần mềm để sử dụng và xây dựng lập trình[cite: 14].
* [cite_start]Tạo đồ án github cho đề tài: `kieutanphuoc84tv/DO_AN_BLOCKCHAIN_VI_DIEN_TU`[cite: 15].

### [cite_start]✅ Kết quả Đạt được [cite: 16]

* [cite_start]Hiểu được kiến thức cơ bản công nghệ blockchain và nguyên lý hoạt động của hash, block mạng P2P[cite: 17].
* [cite_start]Biết được hướng lập trình ngôn ngữ và cài đặt phần mềm chuẩn bị lập trình[cite: 18].
* [cite_start]Tạo đồ án github thành công[cite: 19].

### 💻 Công cụ Chuẩn bị

| Công cụ | Mô tả | Hình ảnh |
| :--- | :--- | :---: |
| **Anaconda** | [cite_start]Ứng dụng để liên kết thư viện python [cite: 21] | 

[Image of Anaconda logo]
 |
| **Visual Studio Code (VS Code)** | [cite_start]Ứng dụng để lập trình [cite: 21] | 

[Image of Visual Studio Code logo]
 |
| **Jupyter** | [cite_start]Ứng dụng mô phỏng [cite: 21] |  |

### 🛑 Khó khăn và Giải pháp

#### [cite_start]Khó khăn Gặp phải [cite: 22]

* [cite_start]Khó khăn gặp phải khi cài ứng dụng bị lỗi và không thành công trong quá trình cài đặt[cite: 23, 24].
* [cite_start]Khó khăn gặp phải khi liên kết thư viện python của phần mềm anaconda[cite: 25].

#### [cite_start]Nguyên nhân [cite: 26]

* [cite_start]**Xung đột môi trường (Environment Conflict):** Do máy tính tồn tại song song nhiều phiên bản Python (Python gốc và Python của Anaconda) dẫn đến việc Visual Studio Code nhận diện sai đường dẫn thư viện[cite: 27].
* [cite_start]**Thiếu cấu hình biến môi trường (Path Variable):** Chưa thiết lập đúng đường dẫn của Anaconda vào biến môi trường của Windows, khiến Terminal không gọi được lệnh `conda` hoặc `jupyter`[cite: 28].
* [cite_start]**Lỗi kernel:** Chưa cài đặt hoặc liên kết gói `ipykernel` cho môi trường ảo, dẫn đến việc Jupyter Notebook không thể thực thi code Python[cite: 29].

#### [cite_start]Kinh nghiệm Rút ra [cite: 30]

* [cite_start]Không nên cài đặt jupyter vì lý do bị lỗi và không nhận thư viện python từ anaconda[cite: 31].
* [cite_start]Phải cài thư viện python trước và cài thêm môi trường của python vào visual studio code sau đó cài được jupyter[cite: 32].

---

## II. [cite_start]NỘI DUNG BÁO CÁO: KIẾN THỨC BLOCKCHAIN CƠ BẢN [cite: 33, 34]

### [cite_start]1. Nguyên lý hoạt động của Blockchain [cite: 35]

* [cite_start]**Khái niệm:** Blockchain là sổ cái kỹ thuật số phi tập trung, lưu các giao dịch trên nhiều máy tính[cite: 36]. [cite_start]Dữ liệu trong các khối đã ghi sẽ không thể sửa đổi nếu không thay đổi toàn bộ chuỗi phía sau[cite: 37].
* [cite_start]**Cơ chế:** Dữ liệu được lưu trong các block[cite: 38]. [cite_start]Mỗi block chứa mã băm (hash) và liên kết với block trước đó để tạo thành chuỗi[cite: 38].
* [cite_start]**Đặc tính:** Bảo mật cao, hạn chế gian lận, minh bạch[cite: 39].

### [cite_start]2. Cấu trúc một Block trong Python [cite: 40]

[cite_start]Một block gồm các thành phần chính[cite: 41]:

* [cite_start]**Index:** Số thứ tự block[cite: 42].
* [cite_start]**Timestamp:** Thời gian tạo block[cite: 43].
* [cite_start]**data/Transactions:** Nội dung giao dịch hoặc dữ liệu lưu trữ[cite: 44].
* [cite_start]**Previous Hash:** Hash của block đứng trước[cite: 45].
* [cite_start]**Hash:** Hash của block hiện tại[cite: 46].
* [cite_start]**Nonce:** Số được thay đổi liên tục trong quá trình đào (mining)[cite: 47].

### [cite_start]3. Hàm băm (Hash) [cite: 48]

* [cite_start]**Định nghĩa:** Chuyển dữ liệu đầu vào bất kỳ thành chuỗi ký tự cố định (sử dụng SHA-256 trong đồ án)[cite: 49].
* [cite_start]**Đặc điểm:** [cite: 50]
    * [cite_start]**Ổn định:** Cùng một dữ liệu $\rightarrow$ cùng một hash[cite: 51].
    * [cite_start]**Nhạy cảm:** Chỉ thay đổi rất nhỏ cũng làm hash khác hoàn toàn $\rightarrow$ giúp phát hiện sửa đổi dữ liệu[cite: 52].

### [cite_start]4. Nonce và Proof of Work (PoW) [cite: 53]

* [cite_start]**Nonce:** Số nguyên được thử liên tục khi đào block[cite: 54].
* [cite_start]**Mục tiêu:** Tìm ra hash thỏa điều kiện difficulty (ví dụ hash bắt đầu bằng 4 số 0)[cite: 55].
* [cite_start]**Cách thực hiện:** Máy tính thử nhiều giá trị Nonce $\rightarrow$ tính lại hash $\rightarrow$ đến khi đạt yêu cầu[cite: 56].

### [cite_start]5. Mạng ngang hàng (P2P - Peer-to-Peer) [cite: 57]

* [cite_start]**Mô hình:** Không có máy chủ trung tâm[cite: 58]. [cite_start]Mỗi node đều có bản sao blockchain[cite: 58].
* [cite_start]**Đồng thuận:** Khi có block mới: [cite: 59]
    * [cite_start]Nó được gửi đến tất cả node[cite: 60].
    * [cite_start]Các node kiểm tra hợp lệ $\rightarrow$ đồng ý thêm vào chuỗi[cite: 61].
    * [cite_start]Đảm bảo dữ liệu đồng bộ và tránh gian lận[cite: 62].

---

## III. [cite_start]KẾ HOẠCH TUẦN TIẾP THEO (24/11/2025 - 30/11/2025) [cite: 63]

* [cite_start]Nghiên cứu về ví điện tử và cơ chế giao dịch lưu trữ khóa công khai và riêng tư[cite: 64].

---

[cite_start]**SINH VIÊN THỰC HIỆN** [cite: 65]

[cite_start]**KIỀU TẤN PHƯỚC** [cite: 66]
