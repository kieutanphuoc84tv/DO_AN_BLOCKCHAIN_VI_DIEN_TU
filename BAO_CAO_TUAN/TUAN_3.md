# BAO CAO TUAN 3

## Thong tin co ban

- **Thoi gian**: Tu 08/12/2025 den 14/12/2025
- **Giai doan**: Tuan 3 - Thiet ke va xay dung chuong trinh

## Noi dung cong viec

### 1. Thiet ke cau truc Block

Tao class Block voi cac thanh phan:
- index: So thu tu block
- transactions: Danh sach giao dich
- previous_hash: Hash cua block truoc
- timestamp: Thoi gian tao
- nonce: Gia tri dung cho Proof of Work
- hash: Hash cua block hien tai

### 2. Xay dung class Blockchain

Cac thanh phan chinh:
- chain: Mang chua cac block
- pending_transactions: Giao dich cho xac nhan
- difficulty: Do kho dao (so luong so 0 o dau hash)
- mining_reward: Phan thuong dao

Cac phuong thuc:
- create_genesis_block(): Tao block dau tien
- get_latest_block(): Lay block cuoi cung
- add_transaction(): Them giao dich moi
- mine_pending_transactions(): Dao block moi
- get_balance(): Tinh so du vi

### 3. Xay dung he thong vi dien tu

Tao class Wallet su dung thu vien ecdsa:
- Tao cap khoa ECDSA tu dong
- Phuong thuc ky giao dich (sign_transaction)
- Phuong thuc xac minh chu ky

### 4. Xay dung giao dien web voi Flask

Cac tinh nang chinh:
- Tao vi moi
- Xem danh sach vi
- Gui giao dich co chu ky
- Bat/dung tu dong dao
- Xem Blockchain va lich su giao dich

### 5. Mo phong qua trinh dao (Mining)

Hien thuc Proof of Work:
- Thu cac gia tri nonce tu 0
- Tinh hash voi moi nonce
- Tim hash bat dau bang so luong so 0 theo do kho
- Hien thi qua trinh that bai va thanh cong

### 6. Mo phong mang P2P

Tao 4 node ao de mo phong mang phan tan:
- Node_Alpha, Node_Beta, Node_Gamma, Node_Delta
- Mo phong broadcast block moi den cac node
- Mo phong dong bo blockchain giua cac node
- Cho phep bat/tat node de mo phong tinh huong that

## Ket qua dat duoc

- Hoan thanh cau truc Block va Blockchain
- Hoan thanh he thong vi dien tu voi ECDSA
- Hoan thanh giao dien web voi Flask
- Hoan thanh mo phong Proof of Work
- Hoan thanh mo phong mang P2P
- Ung dung chay duoc tren Jupyter Notebook

## Kho khan gap phai

- Thiet ke giao dien de xem qua trinh mining chi tiet
- Xu ly dong bo giua frontend va backend
- Fix loi JavaScript trong viec hien thi du lieu

## Ke hoach tuan tiep theo

Kiem tra, sua loi va hoan thien bao cao, slide thuyet trinh.
