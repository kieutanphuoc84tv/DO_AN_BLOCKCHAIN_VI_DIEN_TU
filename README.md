# Đồ án: Mô phỏng Blockchain và Ví Tiền Điện Tử (Python)

Mục tiêu
- Nắm nguyên lý Blockchain: block, hash, nonce, proof-of-work.
- Xây dựng chương trình mô phỏng chuỗi khối đơn giản bằng Python.
- Triển khai API (Flask) để thêm giao dịch, đào (mine) và xem chuỗi.
- Thêm module ví (ECDSA) để ký giao dịch.

Yêu cầu môi trường
- Python 3.8+
- Cài các gói trong `requirements.txt`

Cài đặt

PowerShell:

```powershell
python -m pip install -r "d:\CODE PYTHON\requirements.txt"
```

Hoặc trong Jupyter notebook (ô đầu):

```python
%pip install networkx matplotlib flask requests ecdsa streamlit pytest
```

Chạy Flask (server)
- Mở file `DOANTIMHIEUBLOCKCHAINVAVITIEN.ipynb` trong Jupyter/VSCode và chạy tuần tự các ô đến ô chứa Flask app (ô có `app.run(port=5000)`).
- Hoặc xuất thành script và chạy:

```powershell
# nếu bạn đã chuyển thành script .py
python "d:\CODE PYTHON\DOANTIMHIEUBLOCKCHAINVAVITIEN.py"
```

Kiểm tra endpoints (PowerShell examples)

```powershell
# Thêm giao dịch (ví dụ cấp tiền từ Network)
Invoke-RestMethod -Uri http://127.0.0.1:5000/add_transaction -Method Post -Body (ConvertTo-Json @{sender="Network"; receiver="Alice"; amount=100; public_key=""; signature=""}) -ContentType 'application/json'

# Mine
Invoke-RestMethod -Uri http://127.0.0.1:5000/mine -Method Post -Body (ConvertTo-Json @{miner="Miner_1"}) -ContentType 'application/json'

# Lấy balance
Invoke-RestMethod -Uri http://127.0.0.1:5000/balance/Alice -Method Get

# Lấy chain
Invoke-RestMethod -Uri http://127.0.0.1:5000/chain -Method Get
```
DEMO CODE 

- sử dụng thunder client để chạy thử và kiểm nghiệm
- chạy code ở jupyter bằng stream ui để hiện giao diện mining và hiện ví tiền

