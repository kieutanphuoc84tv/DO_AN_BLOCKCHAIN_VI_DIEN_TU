# BAO CAO TUAN 2

## Thong tin co ban

- **Thoi gian**: Tu 24/11/2025 den 30/11/2025
- **Giai doan**: Tuan 2 - Nghien cuu vi dien tu va co che giao dich

## Noi dung cong viec

### 1. Nghien cuu ve vi dien tu (Cryptocurrency Wallet)

Vi dien tu la cong cu quan ly khoa va thuc hien giao dich tren mang Blockchain. Mot vi bao gom:
- Khoa bi mat (Private Key): Chuoi ky tu bi mat, dung de ky giao dich
- Khoa cong khai (Public Key): Duoc tao tu khoa bi mat, dung de nhan tien
- Dia chi vi (Address): Phien ban rut gon cua khoa cong khai

### 2. Co che tao cap khoa

Su dung thuat toan ECDSA (Elliptic Curve Digital Signature Algorithm) voi duong cong SECP256k1:
- Tao khoa bi mat ngau nhien 256 bit
- Tinh khoa cong khai tu khoa bi mat bang phep nhan tren duong cong elliptic
- Dia chi vi la hash cua khoa cong khai

### 3. Co che giao dich

Mot giao dich bao gom cac buoc sau:
- Nguoi gui tao giao dich voi thong tin: nguoi gui, nguoi nhan, so tien
- Nguoi gui ky giao dich bang khoa bi mat cua minh
- Giao dich duoc broadcast len mang
- Cac node xac minh chu ky bang khoa cong khai cua nguoi gui
- Giao dich hop le duoc dua vao block tiep theo

### 4. Chu ky so ECDSA

Chu ky so dam bao:
- Xac thuc (Authentication): Chung minh giao dich do chu so huu vi tao ra
- Toan ven (Integrity): Giao dich khong bi sua doi sau khi ky
- Khong choi bo (Non-repudiation): Nguoi ky khong the phu nhan da ky

Quy trinh ky:
- Tao hash cua du lieu giao dich
- Su dung khoa bi mat de tao chu ky tu hash
- Chu ky duoc dinh kem vao giao dich

Quy trinh xac minh:
- Lay chu ky va du lieu giao dich
- Su dung khoa cong khai de xac minh chu ky
- Neu hop le, giao dich duoc chap nhan

### 5. Luu tru khoa

Cac phuong phap luu tru khoa bi mat:
- Luu trong file duoc ma hoa
- Luu trong phan mem vi (wallet software)
- Luu trong vi cung (hardware wallet)
- Ghi ra giay (paper wallet)

## Ket qua dat duoc

- Hieu cau truc va chuc nang cua vi dien tu
- Nam ro co che tao cap khoa cong khai va bi mat
- Hieu quy trinh giao dich va vai tro cua chu ky so
- Hieu cach xac minh giao dich bang chu ky ECDSA
- San sang cho viec thiet ke va xay dung ung dung

## Kho khan gap phai

- Mat ma hoc duong cong elliptic la khai niem phuc tap
- Can tim hieu them ve bao mat khoa bi mat

## Ke hoach tuan tiep theo

Thiet ke cau truc block va bat dau xay dung chuong trinh mo phong bang Python.
