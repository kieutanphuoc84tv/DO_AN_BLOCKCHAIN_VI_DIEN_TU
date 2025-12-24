# ==========================================
# BLOCKCHAIN DEMO - FLASK WEB APP VỚI VÍ TIỀN
# ==========================================
# Copy toàn bộ code này vào 1 cell trong Jupyter Notebook
# Chạy cell -> Web app sẽ tự mở trên trình duyệt!
# ==========================================

import hashlib, json, time, threading, webbrowser, binascii
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
from werkzeug.serving import make_server

try:
    import ecdsa
    ECDSA_AVAILABLE = True
except ImportError:
    ECDSA_AVAILABLE = False
    print("[!] Cần cài ecdsa: pip install ecdsa")

# ==========================================
# WALLET CLASS
# ==========================================
class Wallet:
    """Ví tiền điện tử sử dụng ECDSA"""
    
    def __init__(self, name=""):
        self.name = name
        if ECDSA_AVAILABLE:
            self._private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
            self._public_key = self._private_key.get_verifying_key()
        else:
            self._private_key = None
            self._public_key = None
    
    @property
    def private_key(self):
        if self._private_key:
            return binascii.hexlify(self._private_key.to_string()).decode()
        return "no_ecdsa_" + hashlib.sha256(self.name.encode()).hexdigest()[:32]
    
    @property
    def public_key(self):
        if self._public_key:
            return binascii.hexlify(self._public_key.to_string()).decode()
        return "no_ecdsa_pub_" + hashlib.sha256(self.name.encode()).hexdigest()[:32]
    
    @property
    def address(self):
        """Địa chỉ ví (16 ký tự đầu)"""
        return self.public_key[:16]
    
    def sign_transaction(self, receiver, amount):
        """Ký giao dịch"""
        tx_data = {"sender": self.public_key, "receiver": receiver, "amount": amount}
        tx_string = json.dumps(tx_data, sort_keys=True).encode()
        
        if ECDSA_AVAILABLE and self._private_key:
            signature = self._private_key.sign(tx_string)
            sig_hex = binascii.hexlify(signature).decode()
        else:
            sig_hex = hashlib.sha256(tx_string + self.private_key.encode()).hexdigest()
        
        return {**tx_data, "signature": sig_hex}
    
    @staticmethod
    def verify_transaction(transaction):
        """Xác thực chữ ký"""
        if not ECDSA_AVAILABLE:
            return True  # Skip verification nếu không có ecdsa
        
        try:
            sender_key = ecdsa.VerifyingKey.from_string(
                binascii.unhexlify(transaction["sender"]),
                curve=ecdsa.SECP256k1
            )
            tx_data = {
                "sender": transaction["sender"],
                "receiver": transaction["receiver"],
                "amount": transaction["amount"]
            }
            tx_string = json.dumps(tx_data, sort_keys=True).encode()
            signature = binascii.unhexlify(transaction["signature"])
            return sender_key.verify(signature, tx_string)
        except:
            return False
    
    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "public_key": self.public_key,
            "private_key": self.private_key[:16] + "..." # Chỉ hiện 1 phần
        }

# Tạo sẵn một số ví mẫu
wallets = {}

def create_wallet(name):
    """Tạo ví mới và lưu vào dict"""
    wallet = Wallet(name)
    wallets[wallet.public_key] = wallet
    return wallet

# Tạo ví mặc định
default_wallet = create_wallet("Vi_Cua_Tui")

# ==========================================
# BLOCKCHAIN CORE
# ==========================================
class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index, "transactions": self.transactions,
            "previous_hash": self.previous_hash, "timestamp": self.timestamp, "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash
    
    def to_dict(self):
        return {"index": self.index, "transactions": self.transactions, "previous_hash": self.previous_hash,
                "timestamp": self.timestamp, "nonce": self.nonce, "hash": self.hash}

class Blockchain:
    def __init__(self):
        self.chain = [Block(0, [], "0")]
        self.difficulty = 3
        self.pending_transactions = []
        self.mining_reward = 50
        self.mining_history = []

    def add_transaction(self, sender, receiver, amount, signature=None):
        """Thêm giao dịch - kiểm tra số dư và verify signature"""
        # Kiểm tra số dư (trừ giao dịch từ Network - phần thưởng mining)
        if sender != "Network":
            sender_balance = self.get_balance(sender)
            if sender_balance < amount:
                return False, f"Số dư không đủ! Hiện có: {sender_balance:.2f} coin"
        
        tx = {"sender": sender, "receiver": receiver, "amount": amount}
        if signature:
            tx["signature"] = signature
            # Verify nếu có ecdsa
            if ECDSA_AVAILABLE and sender != "Network":
                if not Wallet.verify_transaction(tx):
                    return False, "Chữ ký không hợp lệ!"
        self.pending_transactions.append(tx)
        return True, "OK"

    def mine_pending_transactions(self, miner_address):
        new_block = Block(len(self.chain), self.pending_transactions.copy(), self.chain[-1].hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        
        mining_info = {
            "block_index": new_block.index, "miner": miner_address, "reward": self.mining_reward,
            "transactions_count": len(new_block.transactions), "hash": new_block.hash[:16] + "...",
            "nonce": new_block.nonce, "timestamp": datetime.fromtimestamp(new_block.timestamp).strftime("%H:%M:%S")
        }
        self.mining_history.append(mining_info)
        self.pending_transactions = [{"sender": "Network", "receiver": miner_address, "amount": self.mining_reward}]
        return mining_info
    
    def get_balance(self, address):
        balance = 0
        print(f"--- Checking balance for: {address} ---")
        
        def is_match(addr1, addr2):
            if not addr1 or not addr2: return False
            if addr1 == addr2: return True
            # Allow matching if one is the short version (16 chars) of the other
            if len(addr1) > 16 and addr1[:16] == addr2: return True
            if len(addr2) > 16 and addr2[:16] == addr1: return True
            return False

        for block in self.chain:
            for tx in block.transactions:
                sender = tx.get("sender")
                receiver = tx.get("receiver")
                amount = tx.get("amount", 0)
                
                if is_match(receiver, address):
                    balance += amount
                    print(f" + Found IN (Block {block.index}): {amount} from {sender}")
                
                if is_match(sender, address):
                    balance -= amount
                    print(f" - Found OUT (Block {block.index}): {amount} to {receiver}")

        for tx in self.pending_transactions:
            sender = tx.get("sender")
            receiver = tx.get("receiver")
            amount = tx.get("amount", 0)
            
            if is_match(receiver, address):
                balance += amount
                print(f" + Found PENDING IN: {amount} from {sender}")
            
            if is_match(sender, address):
                balance -= amount
                print(f" - Found PENDING OUT: {amount} to {receiver}")
                
        print(f"--- Total Balance: {balance} ---")
        return balance

bc = Blockchain()

# ==========================================
# P2P NETWORK SIMULATION
# ==========================================
class Node:
    """Represents a node in the P2P network"""
    def __init__(self, name, node_id):
        self.name = name
        self.node_id = node_id
        self.is_online = True
        self.blockchain_length = 1  # Genesis block
        self.pending_transactions = 0
        self.last_block_hash = "0"
        self.sync_status = "Synced"
        self.received_blocks = []
        self.received_transactions = []
    
    def to_dict(self):
        return {
            "name": self.name,
            "node_id": self.node_id,
            "is_online": self.is_online,
            "blockchain_length": self.blockchain_length,
            "pending_transactions": self.pending_transactions,
            "last_block_hash": self.last_block_hash[:16] + "..." if len(self.last_block_hash) > 16 else self.last_block_hash,
            "sync_status": self.sync_status
        }

class P2PNetwork:
    """Simulates a P2P network with multiple nodes"""
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.nodes = {}
        self.network_log = []
        self.broadcast_history = []
        
        # Create default nodes
        self._create_default_nodes()
    
    def _create_default_nodes(self):
        """Create 4 default nodes for the network"""
        node_names = [
            ("Node_Alpha", "alpha_001"),
            ("Node_Beta", "beta_002"),
            ("Node_Gamma", "gamma_003"),
            ("Node_Delta", "delta_004")
        ]
        for name, node_id in node_names:
            self.nodes[node_id] = Node(name, node_id)
        self._log(f"[NETWORK] Khởi tạo mạng P2P với {len(self.nodes)} nodes")
    
    def _log(self, message):
        """Add message to network log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {"time": timestamp, "message": message}
        self.network_log.append(log_entry)
        if len(self.network_log) > 50:
            self.network_log = self.network_log[-50:]
    
    def sync_all_nodes(self):
        """Sync all nodes with the main blockchain"""
        main_length = len(self.blockchain.chain)
        main_hash = self.blockchain.chain[-1].hash if self.blockchain.chain else "0"
        pending_count = len(self.blockchain.pending_transactions)
        
        for node_id, node in self.nodes.items():
            if node.is_online:
                old_length = node.blockchain_length
                node.blockchain_length = main_length
                node.last_block_hash = main_hash
                node.pending_transactions = pending_count
                node.sync_status = "Synced"
                
                if old_length < main_length:
                    blocks_received = main_length - old_length
                    self._log(f"[SYNC] {node.name} nhận {blocks_received} block mới (height: {main_length})")
    
    def broadcast_block(self, block_info):
        """Broadcast a new block to all nodes"""
        block_index = block_info.get("block_index", 0)
        block_hash = block_info.get("hash", "")[:16]
        
        self._log(f"[BROADCAST] 📡 Block #{block_index} được broadcast đến tất cả nodes")
        
        online_nodes = [n for n in self.nodes.values() if n.is_online]
        for node in online_nodes:
            node.received_blocks.append(block_index)
            if len(node.received_blocks) > 10:
                node.received_blocks = node.received_blocks[-10:]
            self._log(f"[RECEIVE] {node.name} nhận Block #{block_index} ✅")
        
        # Sync all nodes after broadcast
        self.sync_all_nodes()
        
        self.broadcast_history.append({
            "type": "block",
            "block_index": block_index,
            "hash": block_hash,
            "nodes_reached": len(online_nodes),
            "time": datetime.now().strftime("%H:%M:%S")
        })
    
    def broadcast_transaction(self, tx_info):
        """Broadcast a new transaction to all nodes"""
        amount = tx_info.get("amount", 0)
        
        self._log(f"[BROADCAST] 📡 Giao dịch {amount} coin được broadcast")
        
        online_nodes = [n for n in self.nodes.values() if n.is_online]
        for node in online_nodes:
            node.pending_transactions += 1
            self._log(f"[RECEIVE] {node.name} nhận giao dịch → Mempool: {node.pending_transactions}")
    
    def toggle_node(self, node_id):
        """Toggle node online/offline status"""
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.is_online = not node.is_online
            status = "ONLINE 🟢" if node.is_online else "OFFLINE 🔴"
            self._log(f"[STATUS] {node.name} chuyển sang {status}")
            
            if node.is_online:
                # Sync when coming back online
                node.sync_status = "Syncing..."
                self.sync_all_nodes()
            return True
        return False
    
    def get_network_status(self):
        """Get full network status"""
        return {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "total_nodes": len(self.nodes),
            "online_nodes": sum(1 for n in self.nodes.values() if n.is_online),
            "network_log": self.network_log[-20:],
            "broadcast_history": self.broadcast_history[-10:]
        }

# Initialize P2P Network
p2p_network = P2PNetwork(bc)

# ==========================================
# AUTO-MINING ENGINE (Realistic Version)
# ==========================================
class AutoMiner:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.is_running = False
        self.timer = None
        self.interval = 10
        self.miner_address = default_wallet.address
        self.blocks_mined = 0
        # Mining progress tracking
        self.current_attempt = 0
        self.current_hash = ""
        self.mining_in_progress = False
        self.last_mine_time = 0
        self.total_attempts = 0
        self.failed_attempts = []  # Store recent failed attempts for display
        self.hash_rate = 0
        self.mine_start_time = 0
    
    def start(self, miner_address, interval):
        if self.is_running: return False
        self.miner_address = miner_address
        self.interval = interval
        self.is_running = True
        self._schedule_next_mine()
        return True
    
    def stop(self):
        self.is_running = False
        self.mining_in_progress = False
        if self.timer: self.timer.cancel()
        self.timer = None
        return True
    
    def _schedule_next_mine(self):
        if self.is_running:
            self.timer = threading.Timer(self.interval, self._do_mine)
            self.timer.daemon = True
            self.timer.start()
    
    def _do_mine(self):
        if not self.is_running: return
        
        self.mining_in_progress = True
        self.mine_start_time = time.time()
        self.current_attempt = 0
        # Don't clear failed_attempts here - keep last block's attempts visible
        self.failed_attempts = []
        
        if len(self.blockchain.pending_transactions) == 0:
            self.blockchain.add_transaction("Network", self.miner_address, 0)
        
        # Mine with progress tracking
        result = self._mine_with_progress(self.miner_address)
        
        self.mining_in_progress = False
        self.last_mine_time = time.time() - self.mine_start_time
        self.blocks_mined += 1
        self.total_attempts += self.current_attempt
        
        # Calculate hash rate
        if self.last_mine_time > 0:
            self.hash_rate = int(self.current_attempt / self.last_mine_time)
        
        # Keep the last result visible (don't reset failed_attempts here)
        self.last_mining_result = result
        
        # Broadcast block to P2P network
        try:
            p2p_network.broadcast_block(result)
        except:
            pass  # P2P network may not be initialized yet
        
        self._schedule_next_mine()
    
    def _mine_with_progress(self, miner_address):
        """Mine block while tracking progress for UI display"""
        new_block = Block(len(self.blockchain.chain), self.blockchain.pending_transactions.copy(), self.blockchain.chain[-1].hash)
        
        difficulty = self.blockchain.difficulty
        target = "0" * difficulty
        
        while new_block.hash[:difficulty] != target:
            self.current_attempt += 1
            old_hash = new_block.hash
            
            # Store failed attempt (keep last 10 for better visibility)
            if len(self.failed_attempts) >= 10:
                self.failed_attempts.pop(0)
            self.failed_attempts.append({
                "nonce": new_block.nonce,
                "hash": old_hash[:40],
                "status": "FAILED",
                "leading_zeros": len(old_hash) - len(old_hash.lstrip('0'))
            })
            
            self.current_hash = old_hash
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
        
        # Success! Add the successful hash to the list for comparison
        self.failed_attempts.append({
            "nonce": new_block.nonce,
            "hash": new_block.hash[:40],
            "status": "SUCCESS",
            "leading_zeros": difficulty
        })
        
        self.current_hash = new_block.hash
        self.blockchain.chain.append(new_block)
        
        mining_info = {
            "block_index": new_block.index, "miner": miner_address, "reward": self.blockchain.mining_reward,
            "transactions_count": len(new_block.transactions), "hash": new_block.hash[:16] + "...",
            "nonce": new_block.nonce, "timestamp": datetime.fromtimestamp(new_block.timestamp).strftime("%H:%M:%S"),
            "attempts": self.current_attempt, "time_seconds": round(time.time() - self.mine_start_time, 2)
        }
        self.blockchain.mining_history.append(mining_info)
        self.blockchain.pending_transactions = [{"sender": "Network", "receiver": miner_address, "amount": self.blockchain.mining_reward}]
        
        return mining_info
    
    def get_status(self):
        return {
            "is_running": self.is_running, 
            "blocks_mined": self.blocks_mined, 
            "interval": self.interval, 
            "miner_address": self.miner_address
        }
    
    def get_mining_progress(self):
        """Return detailed mining progress for real-time UI updates"""
        return {
            "mining_in_progress": self.mining_in_progress,
            "current_attempt": self.current_attempt,
            "current_hash": self.current_hash[:32] + "..." if self.current_hash else "",
            "failed_attempts": self.failed_attempts[-5:],  # Last 5 failed attempts
            "hash_rate": self.hash_rate,
            "last_mine_time": round(self.last_mine_time, 2),
            "total_attempts": self.total_attempts,
            "difficulty": self.blockchain.difficulty,
            "target": "0" * self.blockchain.difficulty + "x" * (64 - self.blockchain.difficulty)
        }

auto_miner = AutoMiner(bc)

# ==========================================
# FLASK APP + HTML TEMPLATE
# ==========================================
app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blockchain Demo - Ví Tiền Điện Tử</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-body: #0f172a;
            --bg-card: #1e293b;
            --bg-input: #334155;
            --border-color: #475569;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #0ea5e9;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-body);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.5;
        }

        .container { max-width: 1400px; margin: 0 auto; }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 30px;
        }

        .header h1 { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px; }
        .header p { color: var(--text-secondary); font-size: 0.9rem; }
        .header .sub-info { text-align: right; }
        .header .sub-info strong { color: var(--primary); }

        .cards-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 24px;
            margin-bottom: 24px;
        }

        .card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
        }

        .col-4 { grid-column: span 4; }
        .col-6 { grid-column: span 6; }
        .col-8 { grid-column: span 8; }
        .col-12 { grid-column: span 12; }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border-color);
        }

        .card-title {
            font-size: 0.95rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-secondary);
        }

        .form-group { margin-bottom: 16px; }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .form-control {
            width: 100%;
            padding: 10px 12px;
            background-color: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            transition: border-color 0.2s;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary);
        }

        select.form-control { cursor: pointer; }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 10px 20px;
            border-radius: 6px;
            border: none;
            font-weight: 500;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
            width: 100%;
        }

        .btn-primary { background-color: var(--primary); color: white; }
        .btn-primary:hover { background-color: var(--primary-hover); }

        .btn-success { background-color: var(--success); color: white; }
        .btn-success:hover { filter: brightness(110%); }

        .btn-danger { background-color: var(--danger); color: white; }
        .btn-danger:hover { filter: brightness(110%); }

        .btn-group { display: flex; gap: 10px; }

        .status-box {
            margin-top: 15px;
            padding: 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            background-color: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
            color: var(--text-primary);
        }

        .status-success { background-color: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.2); color: #34d399; }
        .status-error { background-color: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.2); color: #f87171; }
        .status-warning { background-color: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.2); color: #fbbf24; }

        .tabs { display: flex; gap: 2px; margin-bottom: 20px; border-bottom: 1px solid var(--border-color); }
        .tab {
            padding: 12px 24px;
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            color: var(--text-secondary);
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        .tab:hover { color: var(--text-primary); }
        .tab.active { color: var(--primary); border-bottom-color: var(--primary); }

        .tab-content { 
            display: none; 
            opacity: 0;
            animation: fadeIn 0.3s ease-in-out forwards;
        }
        .tab-content.active { 
            display: block; 
            opacity: 1;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }

        .stat-card {
            background-color: var(--bg-input);
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }

        .stat-val { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); }
        .stat-label { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; margin-top: 5px; }

        .table-wrapper { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
        
        th {
            text-align: left;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.8rem;
            text-transform: uppercase;
        }

        td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        tr:last-child td { border-bottom: none; }
        
        .font-mono { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }

        .wallet-details {
            margin-top: 15px;
            padding: 15px;
            background-color: var(--bg-input);
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            word-break: break-all;
        }
        .wallet-item { margin-bottom: 8px; }
        .wallet-label { color: var(--text-secondary); margin-right: 8px; }

        .log-box {
            height: 200px;
            overflow-y: auto;
            background-color: #000;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 15px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #10b981;
        }
        .log-entry { margin-bottom: 4px; border-bottom: 1px solid #111; padding-bottom: 4px; }

        @media (max-width: 1024px) {
            .col-4, .col-8 { grid-column: span 12; }
            .col-6 { grid-column: span 12; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>Blockchain Demo</h1>
                <p>Hệ thống mô phỏng Blockchain & Tiền điện tử</p>
            </div>
            <div class="sub-info">
                <p>Sinh viên thực hiện: <strong>Kiều Tấn Phước</strong></p>
                <p>Version: 2.0 (Pro UI)</p>
            </div>
        </div>

        <div class="cards-grid">
            <!-- Create Wallet -->
            <div class="card col-4">
                <div class="card-header">
                    <span class="card-title">Tạo Ví Mới</span>
                </div>
                <div class="form-group">
                    <label>Tên định danh ví</label>
                    <input type="text" id="wallet-name" class="form-control" value="Vi_Cua_Tôi" placeholder="Nhập tên ví...">
                </div>
                <button class="btn btn-primary" onclick="createWallet()">
                    <span>+ Tạo Ví Mới</span>
                </button>
                <div id="wallet-info"></div>
            </div>

            <!-- Transaction -->
            <div class="card col-4">
                <div class="card-header">
                    <span class="card-title">Chuyển Tiền</span>
                </div>
                <div class="form-group">
                    <label>Gửi từ</label>
                    <select id="sender-wallet" class="form-control" onchange="updateSenderKey()">
                        <option value="">-- Chọn ví gửi --</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Gửi đến</label>
                    <select id="receiver" class="form-control">
                        <option value="">-- Chọn ví nhận --</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Số lượng (Coin)</label>
                    <input type="number" id="amount" class="form-control" value="10" min="0.01" step="0.01">
                </div>
                <button class="btn btn-info" style="background: var(--info); color: white;" onclick="sendTx()">
                    Thực hiện Giao dịch
                </button>
                <div id="tx-status"></div>
            </div>

            <!-- Mining -->
            <div class="card col-4">
                <div class="card-header">
                    <span class="card-title">⛏️ Hệ thống Mining</span>
                </div>
                <div class="form-group">
                    <label>Ví nhận thưởng (Coinbase)</label>
                    <select id="miner-wallet" class="form-control">
                        <option value="">-- Chọn ví --</option>
                    </select>
                </div>
                <div class="btn-group">
                    <button class="btn btn-success" onclick="startAuto()">⛏️ Bắt đầu Đào</button>
                    <button class="btn btn-danger" onclick="stopAuto()">⏹️ Dừng</button>
                </div>
                
                <div id="auto-status" class="status-box" style="display:flex; justify-content:space-between;">
                    <span>TRẠNG THÁI: <strong>DỪNG</strong></span>
                    <span>Blocks: 0</span>
                </div>
                
                <!-- Mining Progress Display -->
                <div id="mining-progress" style="margin-top: 15px; display: none;">
                    <div style="background: var(--bg-input); border-radius: 6px; padding: 12px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span style="color: var(--text-secondary); font-size: 0.8rem;">Tốc độ Hash:</span>
                            <span id="hash-rate" class="font-mono" style="color: var(--warning);">0 H/s</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span style="color: var(--text-secondary); font-size: 0.8rem;">Lần thử:</span>
                            <span id="attempt-count" class="font-mono" style="color: var(--info);">0</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: var(--text-secondary); font-size: 0.8rem;">Độ khó:</span>
                            <span id="difficulty-display" class="font-mono" style="color: var(--danger);">3 zeros</span>
                        </div>
                    </div>
                    
                    <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 5px;">Hash gần nhất:</div>
                    <div id="current-hash" class="font-mono" style="background: #000; padding: 8px; border-radius: 4px; font-size: 0.7rem; color: var(--danger); word-break: break-all; margin-bottom: 10px;">
                        Đang chờ...
                    </div>
                    
                    <!-- 2 Column Layout: Failed | Success -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div>
                            <div style="font-size: 0.75rem; color: var(--danger); margin-bottom: 5px;">❌ Thất bại gần đây:</div>
                            <div id="failed-attempts" style="background: rgba(239,68,68,0.1); border: 1px solid var(--danger); padding: 8px; border-radius: 4px; max-height: 150px; overflow-y: auto; font-size: 0.6rem;">
                                <div style="color: var(--text-secondary);">Chưa có...</div>
                            </div>
                        </div>
                        <div>
                            <div style="font-size: 0.75rem; color: var(--success); margin-bottom: 5px;">✅ Thành công:</div>
                            <div id="success-attempts" style="background: rgba(16,185,129,0.1); border: 1px solid var(--success); padding: 8px; border-radius: 4px; max-height: 150px; overflow-y: auto; font-size: 0.6rem;">
                                <div style="color: var(--text-secondary);">Chưa có...</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="mining-status" style="margin-top: 10px; font-size: 0.8rem; color: var(--text-secondary);">
                    Sẵn sàng hoạt động...
                </div>
            </div>
        </div>

        <div class="cards-grid">
            <!-- Balance & List -->
            <div class="card col-12">
                <div class="card-header">
                    <span class="card-title">Quản lý Ví</span>
                </div>
                <div style="display: flex; gap: 20px; align-items: flex-end; margin-bottom: 20px;">
                    <div style="flex: 1;">
                        <label style="display:block; margin-bottom:8px; color:var(--text-secondary); font-size:0.85rem;">Tra cứu số dư</label>
                        <select id="bal-addr" class="form-control"></select>
                    </div>
                    <button class="btn btn-primary" style="width: auto;" onclick="checkBal()">Kiểm tra</button>
                    <button class="btn btn-danger" style="width: auto;" onclick="deleteWallet()">Xóa Ví</button>
                </div>
                
                <div id="bal-display" class="status-box status-success" style="display:none; text-align:center;">
                    <div class="balance-amount" style="font-size: 2rem; font-weight: 700;">0.00 COIN</div>
                    <div id="bal-wallet-name" style="font-size: 0.9rem; opacity: 0.8;">-</div>
                </div>

                <div style="margin-top: 20px;">
                    <h4 style="font-size: 0.9rem; margin-bottom: 10px; color: var(--text-secondary);">DANH SÁCH VÍ TRONG HỆ THỐNG</h4>
                    <div id="wallets-list" style="max-height: 200px; overflow-y: auto; background: var(--bg-input); border-radius: 6px; padding: 10px;">
                        <!-- List populated by JS -->
                    </div>
                </div>
            </div>
        </div>

        <div class="cards-grid">
            <div class="card col-12">
                <div class="tabs">
                    <button class="tab active" onclick="showTab('chain')">Blockchain Explorer</button>
                    <button class="tab" onclick="showTab('history')">Lịch sử Mining</button>
                    <button class="tab" onclick="showTab('tx')">Sổ cái Giao dịch</button>
                    <button class="tab" onclick="showTab('p2p')">🌐 Mạng P2P</button>
                </div>

                <!-- Tab Blockchain -->
                <div id="tab-chain" class="tab-content active">
                    <div id="chain-stats" class="stats-grid"></div>
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Height</th>
                                    <th>Hash</th>
                                    <th>Prev Hash</th>
                                    <th>Nonce</th>
                                    <th>TXs</th>
                                </tr>
                            </thead>
                            <tbody id="chain-table"></tbody>
                        </table>
                    </div>
                    <div id="pending-info"></div>
                </div>

                <!-- Tab History -->
                <div id="tab-history" class="tab-content">
                    <div id="mining-stats" class="stats-grid"></div>
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Block</th>
                                    <th>Miner Address</th>
                                    <th>Reward</th>
                                    <th>Thất bại</th>
                                    <th>Nonce thành công</th>
                                    <th>Thời gian</th>
                                </tr>
                            </thead>
                            <tbody id="history-table"></tbody>
                        </table>
                    </div>
                </div>

                <!-- Tab Transactions -->
                <div id="tab-tx" class="tab-content">
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Block</th>
                                    <th>Sender</th>
                                    <th>Receiver</th>
                                    <th>Amount</th>
                                    <th>Signed?</th>
                                </tr>
                            </thead>
                            <tbody id="tx-table"></tbody>
                        </table>
                    </div>
                </div>

                <!-- Tab P2P Network -->
                <div id="tab-p2p" class="tab-content">
                    <div id="p2p-stats" class="stats-grid"></div>
                    
                    <h4 style="margin: 20px 0 15px; color: var(--text-secondary);">📡 Network Nodes</h4>
                    <div id="p2p-nodes" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;"></div>
                    
                    <h4 style="margin: 20px 0 15px; color: var(--text-secondary);">📋 Network Activity Log</h4>
                    <div id="p2p-log" style="background: #000; border-radius: 6px; padding: 15px; max-height: 200px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;"></div>
                </div>
            </div>
        </div>

        <div class="card" style="margin-top: 24px;">
            <div class="card-header">
                <span class="card-title">System Log</span>
            </div>
            <div id="log" class="log-box"></div>
        </div>
    </div>

    <script>
        let logs = [], autoRefresh = null, walletsList = [];

        function log(m) {
            let t = new Date().toLocaleTimeString('vi-VN');
            logs.unshift(`[${t}] ${m}`);
            if (logs.length > 50) logs = logs.slice(0, 50);
            document.getElementById('log').innerHTML = logs.map(l => `<div class="log-entry">${l}</div>`).join('');
        }

        async function createWallet() {
            let name = document.getElementById('wallet-name').value;
            if (!name) { alert('Vui lòng nhập tên ví!'); return; }
            
            let res = await fetch('/api/wallet/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name})
            });
            let d = await res.json();
            
            if (d.success) {
                document.getElementById('wallet-info').innerHTML = `
                    <div class="wallet-details">
                        <div class="wallet-item"><span class="wallet-label">Tên:</span> ${d.wallet.name}</div>
                        <div class="wallet-item"><span class="wallet-label">Đ/C:</span> ${d.wallet.address}</div>
                        <div class="wallet-item"><span class="wallet-label">Key:</span> ${d.wallet.private_key.substring(0, 32)}...</div>
                    </div>`;
                log(`[SUCCESS] Tạo ví mới: ${d.wallet.name} (${d.wallet.address})`);
                updateWalletSelects();
            }
        }

        async function updateWalletSelects() {
            let res = await fetch('/api/wallets');
            let d = await res.json();
            walletsList = d.wallets;
            
            let opts = d.wallets.map(w => `<option value="${w.public_key}">${w.name} (${w.address})</option>`).join('');
            
            document.getElementById('sender-wallet').innerHTML = '<option value="">-- Chọn ví gửi --</option>' + opts;
            document.getElementById('receiver').innerHTML = '<option value="">-- Chọn ví nhận --</option>' + opts;
            document.getElementById('miner-wallet').innerHTML = '<option value="">-- Chọn ví --</option>' + opts;
            document.getElementById('bal-addr').innerHTML = opts || '<option>Chưa có ví nào</option>';

            document.getElementById('wallets-list').innerHTML = d.wallets.map(w => `
                <div style="padding:10px; border-bottom:1px solid var(--border-color); display:flex; align-items:center;">
                    <input type="radio" name="wallet-select" value="${w.public_key}" style="margin-right:10px; transform:scale(1.2);">
                    <div style="flex:1">
                        <div style="font-weight:600; color:var(--text-primary);">${w.name}</div>
                        <div class="font-mono" style="color:var(--text-secondary); font-size:0.75rem;">${w.address}</div>
                    </div>
                </div>
            `).join('') || '<p style="color:var(--text-secondary); text-align:center; padding:10px;">Chưa có ví nào trong hệ thống</p>';
        }

        function updateSenderKey() {
            let sel = document.getElementById('sender-wallet');
            let pk = sel.value;
            if (pk) {
                let w = walletsList.find(x => x.public_key === pk);
                if (w) log(`Chọn ví gửi: ${w.name}`);
            }
        }

        async function sendTx() {
            let senderPk = document.getElementById('sender-wallet').value;
            let receiver = document.getElementById('receiver').value;
            let amount = parseFloat(document.getElementById('amount').value);
            
            if (!senderPk) { document.getElementById('tx-status').innerHTML = `<div class="status-box status-error">Vui lòng chọn ví gửi!</div>`; return; }
            if (!receiver) { document.getElementById('tx-status').innerHTML = `<div class="status-box status-error">Vui lòng chọn ví nhận!</div>`; return; }
            
            let res = await fetch('/api/tx/signed', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sender_pk: senderPk, receiver: receiver, amount: amount})
            });
            let d = await res.json();
            
            if (d.success) {
                document.getElementById('tx-status').innerHTML = `<div class="status-box status-success">${d.message}</div>`;
                log(`[TX] Giao dịch thành công: ${amount} coin`);
                refresh();
            } else {
                document.getElementById('tx-status').innerHTML = `<div class="status-box status-error">${d.error}</div>`;
                log(`[ERROR] Lỗi giao dịch: ${d.error}`);
            }
        }

        let miningProgressInterval = null;

        async function startAuto() {
            let minerPk = document.getElementById('miner-wallet').value;
            if (!minerPk) { alert('Vui lòng chọn ví để nhận phần thưởng Mining!'); return; }
            
            let w = walletsList.find(x => x.public_key === minerPk);
            
            document.getElementById('mining-status').innerHTML = '<span style="color:var(--warning)">⏳ Đang khởi động tiến trình đào...</span>';
            document.getElementById('mining-progress').style.display = 'block';
            
            await fetch('/api/auto/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({miner: minerPk, interval: 10})
            });
            
            log(`[MINING] ⛏️ Đã BẬT Auto-Mining. Miner: ${w ? w.name : 'Unknown'}`);
            updateAuto();
            updateMiningProgress();
            
            if (autoRefresh) clearInterval(autoRefresh);
            autoRefresh = setInterval(refresh, 2000);
            
            if (miningProgressInterval) clearInterval(miningProgressInterval);
            miningProgressInterval = setInterval(updateMiningProgress, 500);
        }

        async function stopAuto() {
            await fetch('/api/auto/stop', {method: 'POST'});
            log('[MINING] ⏹️ Đã DỪNG Auto-Mining.');
            document.getElementById('mining-status').innerHTML = '<span style="color:var(--text-secondary)">Mining đã dừng hoạt động.</span>';
            document.getElementById('mining-progress').style.display = 'none';
            updateAuto();
            
            if (autoRefresh) { clearInterval(autoRefresh); autoRefresh = null; }
            if (miningProgressInterval) { clearInterval(miningProgressInterval); miningProgressInterval = null; }
        }

        async function updateMiningProgress() {
            try {
                let res = await fetch('/api/auto/progress');
                let p = await res.json();
                
                // Update hash rate
                document.getElementById('hash-rate').innerText = `${p.hash_rate.toLocaleString()} H/s`;
                
                // Update attempt count
                document.getElementById('attempt-count').innerText = p.current_attempt.toLocaleString();
                
                // Update difficulty
                document.getElementById('difficulty-display').innerText = `${p.difficulty} zeros`;
                
                // Update current hash with color coding
                let hashEl = document.getElementById('current-hash');
                if (p.current_hash) {
                    let leading = p.current_hash.match(/^0*/)[0].length;
                    let coloredHash = `<span style="color:var(--success)">${'0'.repeat(leading)}</span><span style="color:var(--danger)">${p.current_hash.substring(leading)}</span>`;
                    hashEl.innerHTML = coloredHash;
                }
                
                // Update failed attempts log (left column) and success (right column)
                let failedEl = document.getElementById('failed-attempts');
                let successEl = document.getElementById('success-attempts');
                
                if (p.failed_attempts && p.failed_attempts.length > 0) {
                    // Separate failed and success
                    let failed = p.failed_attempts.filter(f => f.status === 'FAILED');
                    let success = p.failed_attempts.filter(f => f.status === 'SUCCESS');
                    
                    // Render failed attempts (left column)
                    if (failed.length > 0) {
                        failedEl.innerHTML = failed.slice(-8).map(f => {
                            let leadingZeros = f.leading_zeros || 0;
                            let hashDisplay = '<span style="color:var(--success)">' + '0'.repeat(leadingZeros) + '</span><span style="color:var(--danger)">' + f.hash.substring(leadingZeros, leadingZeros + 12) + '...</span>';
                            return '<div style="border-bottom: 1px solid rgba(239,68,68,0.3); padding: 2px 0;">' +
                                '<div style="color:var(--warning)">Nonce ' + f.nonce.toLocaleString() + '</div>' +
                                '<div class="font-mono">' + hashDisplay + '</div>' +
                                '<div style="color:var(--danger)">(' + leadingZeros + '/' + p.difficulty + ' zeros)</div>' +
                                '</div>';
                        }).join('');
                        failedEl.scrollTop = failedEl.scrollHeight;
                    }
                    
                    // Render success attempts (right column)
                    if (success.length > 0) {
                        successEl.innerHTML = success.map(f => {
                            let leadingZeros = f.leading_zeros || 0;
                            let hashDisplay = '<span style="color:var(--success)">' + '0'.repeat(leadingZeros) + '</span><span style="color:var(--success)">' + f.hash.substring(leadingZeros, leadingZeros + 12) + '...</span>';
                            return '<div style="border-bottom: 1px solid rgba(16,185,129,0.3); padding: 4px 0;">' +
                                '<div style="color:var(--success); font-weight:bold;">✅ Block Found!</div>' +
                                '<div style="color:var(--info)">Nonce: ' + f.nonce.toLocaleString() + '</div>' +
                                '<div class="font-mono">' + hashDisplay + '</div>' +
                                '</div>';
                        }).join('');
                    }
                    
                    // Log to System Log
                    if (failed.length > 0) {
                        let lastFailed = failed[failed.length - 1];
                        log('[MINING] ❌ Nonce ' + lastFailed.nonce.toLocaleString() + ' THẤT BẠI - Hash: ' + lastFailed.hash.substring(0,16) + '... (' + lastFailed.leading_zeros + '/' + p.difficulty + ' zeros)');
                    }
                    
                    // Check if there's a new success entry
                    let successEntry = success.length > 0 ? success[success.length - 1] : null;
                    if (successEntry && window.lastLoggedBlock !== successEntry.nonce) {
                        window.lastLoggedBlock = successEntry.nonce;
                        log('[MINING] ✅ Nonce ' + successEntry.nonce.toLocaleString() + ' THÀNH CÔNG! - Hash: ' + successEntry.hash.substring(0,20) + '...');
                    }
                }
                
                // Update mining status with progress
                if (p.mining_in_progress) {
                    document.getElementById('mining-status').innerHTML = `
                        <span style="color:var(--warning)">
                            ⛏️ Đang đào... ${p.current_attempt.toLocaleString()} lần thử | ${p.hash_rate} H/s
                        </span>`;
                } else if (p.last_mine_time > 0) {
                    document.getElementById('mining-status').innerHTML = `
                        <span style="color:var(--success)">
                            ✅ Block mới! Tìm thấy sau ${p.last_mine_time}s với ${p.current_attempt.toLocaleString()} lần thử
                        </span>`;
                }
            } catch (e) {
                console.log('Mining progress error:', e);
            }
        }

        async function updateAuto() {
            let res = await fetch('/api/auto/status');
            let d = await res.json();
            let el = document.getElementById('auto-status');
            
            if (d.is_running) {
                el.innerHTML = `<span>TRẠNG THÁI: <strong style="color:var(--success)">⛏️ ĐANG ĐÀO</strong></span><span>Blocks: ${d.blocks_mined}</span>`;
                el.className = 'status-box status-success';
                document.getElementById('mining-progress').style.display = 'block';
                
                let stats = await (await fetch('/api/stats')).json();
                if (stats.history.length > 0) {
                    let last = stats.history[stats.history.length - 1];
                    let attempts = last.attempts || 'N/A';
                    let timeStr = last.time_seconds ? `${last.time_seconds}s` : 'N/A';
                    log(`[SUCCESS] ✅ Block #${last.block_index} mined! +${last.reward} coin | ${attempts} tries in ${timeStr}`);
                }
            } else {
                el.innerHTML = `<span>TRẠNG THÁI: <strong style="color:var(--danger)">⏹️ ĐÃ DỪNG</strong></span><span>Blocks: ${d.blocks_mined}</span>`;
                el.className = 'status-box status-error';
            }
        }

        async function checkBal() {
            let addr = document.getElementById('bal-addr').value;
            if (!addr) return;
            
            let w = walletsList.find(x => x.public_key === addr);
            let dispAddr = w ? w.name : addr.substring(0, 16);
            
            let res = await fetch(`/api/balance/${addr}`);
            let d = await res.json();
            
            let el = document.getElementById('bal-display');
            let nameEl = document.getElementById('bal-wallet-name');
            
            el.style.display = 'block';
            el.querySelector('.balance-amount').innerText = `${d.balance.toFixed(2)} COIN`;
            nameEl.innerText = `${dispAddr} (${addr.substring(0,8)}...)`;
        }

        function showTab(n) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            
            document.querySelector(`[onclick="showTab('${n}')"]`).classList.add('active');
            document.getElementById(`tab-${n}`).classList.add('active');
        }

        async function refresh() {
            let res = await fetch('/api/chain');
            let d = await res.json();
            
            let txs = d.chain.reduce((s, b) => s + b.transactions.length, 0);
            
            document.getElementById('chain-stats').innerHTML = `
                <div class="stat-card"><div class="stat-val" style="color:var(--primary)">${d.length}</div><div class="stat-label">Total Blocks</div></div>
                <div class="stat-card"><div class="stat-val" style="color:var(--info)">${txs}</div><div class="stat-label">Transactions</div></div>
                <div class="stat-card"><div class="stat-val" style="color:var(--warning)">${d.pending.length}</div><div class="stat-label">In Mempool</div></div>
                <div class="stat-card"><div class="stat-val" style="color:var(--danger)">${d.difficulty}</div><div class="stat-label">Difficulty</div></div>
            `;
            
            document.getElementById('chain-table').innerHTML = d.chain.slice(-8).map(b => `
                <tr>
                    <td><strong style="color:var(--primary)">#${b.index}</strong></td>
                    <td class="font-mono">${b.hash.substring(0, 16)}...</td>
                    <td class="font-mono">${b.previous_hash === '0' ? '<span style="color:var(--success)">Genesis</span>' : b.previous_hash.substring(0, 16) + '...'}</td>
                    <td class="font-mono">${b.nonce.toLocaleString()}</td>
                    <td>${b.transactions.length}</td>
                </tr>
            `).join('');

            document.getElementById('pending-info').innerHTML = d.pending.length > 0 
                ? `<div class="status-box status-warning"><strong>Mempool Alert:</strong> Đang có ${d.pending.length} giao dịch chờ xác nhận</div>` 
                : '';
            
            let stats = await (await fetch('/api/stats')).json();
            document.getElementById('mining-stats').innerHTML = `
                <div class="stat-card"><div class="stat-val">${stats.history.length}</div><div class="stat-label">Mined Blocks</div></div>
                <div class="stat-card"><div class="stat-val" style="color:var(--success)">${stats.total_reward}</div><div class="stat-label">Total Reward</div></div>
                <div class="stat-card"><div class="stat-val" style="color:var(--warning)">${stats.total_nonces.toLocaleString()}</div><div class="stat-label">Total Nonces</div></div>
                <div class="stat-card"><div class="stat-val" style="color:var(--primary)">256-bit</div><div class="stat-label">Algorithm</div></div>
            `;
            
    document.getElementById('history-table').innerHTML = stats.history.slice(-10).reverse().map(h => {
                let attempts = h.attempts || h.nonce;
                let failedAttempts = attempts - 1; // nonce thành công không tính là thất bại
                let timeStr = h.time_seconds ? `${h.time_seconds}s` : 'N/A';
                
                return `
                <tr>
                    <td><strong>#${h.block_index}</strong></td>
                    <td class="font-mono">${h.miner.length > 15 ? h.miner.substring(0, 15) + '...' : h.miner}</td>
                    <td style="color:var(--success)">+${h.reward}</td>
                    <td style="color:var(--danger)">${failedAttempts.toLocaleString()} ❌</td>
                    <td class="font-mono" style="color:var(--success)">${h.nonce.toLocaleString()} ✅</td>
                    <td>${timeStr}</td>
                </tr>`;
            }).join('');
            
            let allTx = [];
            d.chain.forEach(b => b.transactions.forEach(tx => allTx.push({block: b.index, ...tx})));
            
            document.getElementById('tx-table').innerHTML = allTx.slice(-15).reverse().map(tx => `
                <tr>
                    <td><strong>#${tx.block}</strong></td>
                    <td class="font-mono">${(tx.sender || '').substring(0, 12)}...</td>
                    <td class="font-mono">${(tx.receiver || '').substring(0, 12)}...</td>
                    <td><strong>${(tx.amount || 0).toFixed(2)}</strong></td>
                    <td>${tx.signature ? '<span class="status-success" style="padding:2px 6px; border-radius:4px; font-size:0.7rem;">Verified</span>' : '<span style="opacity:0.5">None</span>'}</td>
                </tr>
            `).join('');
            
            updateAuto();
            refreshP2P();
        }

        async function refreshP2P() {
            var statsEl = document.getElementById('p2p-stats');
            var nodesEl = document.getElementById('p2p-nodes');
            var logEl = document.getElementById('p2p-log');
            
            if (!statsEl || !nodesEl || !logEl) {
                return;
            }
            
            try {
                var res = await fetch('/api/p2p/status');
                if (!res.ok) return;
                var p = await res.json();
                
                statsEl.innerHTML = '<div class="stat-card"><div class="stat-val" style="color:var(--primary)">' + p.total_nodes + '</div><div class="stat-label">Total Nodes</div></div>' +
                    '<div class="stat-card"><div class="stat-val" style="color:var(--success)">' + p.online_nodes + '</div><div class="stat-label">Online</div></div>' +
                    '<div class="stat-card"><div class="stat-val" style="color:var(--danger)">' + (p.total_nodes - p.online_nodes) + '</div><div class="stat-label">Offline</div></div>' +
                    '<div class="stat-card"><div class="stat-val" style="color:var(--warning)">' + p.broadcast_history.length + '</div><div class="stat-label">Broadcasts</div></div>';
                
                var nodesHtml = '';
                for (var i = 0; i < p.nodes.length; i++) {
                    var n = p.nodes[i];
                    var color = n.is_online ? 'var(--success)' : 'var(--danger)';
                    var icon = n.is_online ? '🟢' : '🔴';
                    var btnColor = n.is_online ? 'var(--danger)' : 'var(--success)';
                    var btnText = n.is_online ? 'Tắt Node' : 'Bật Node';
                    nodesHtml += '<div style="background:var(--bg-input);border:1px solid ' + color + ';border-radius:8px;padding:15px;text-align:center;">' +
                        '<div style="font-size:2rem;margin-bottom:10px;">' + icon + '</div>' +
                        '<div style="font-weight:600;color:var(--text-primary);">' + n.name + '</div>' +
                        '<div style="font-size:0.75rem;color:var(--text-secondary);margin:5px 0;">Blocks: ' + n.blockchain_length + ' | Mempool: ' + n.pending_transactions + '</div>' +
                        '<div style="font-size:0.65rem;color:' + color + ';">' + n.sync_status + '</div>' +
                        '<button data-nodeid="' + n.node_id + '" class="toggle-node-btn" style="margin-top:10px;padding:5px 10px;font-size:0.7rem;background:' + btnColor + ';color:white;border:none;border-radius:4px;cursor:pointer;">' + btnText + '</button></div>';
                }
                nodesEl.innerHTML = nodesHtml;
                
                // Add click handlers
                var btns = document.querySelectorAll('.toggle-node-btn');
                for (var j = 0; j < btns.length; j++) {
                    btns[j].onclick = function() { toggleNode(this.getAttribute('data-nodeid')); };
                }
                
                var logHtml = '';
                var recentLogs = p.network_log.slice(-15).reverse();
                for (var k = 0; k < recentLogs.length; k++) {
                    var l = recentLogs[k];
                    var logColor = 'var(--text-secondary)';
                    if (l.message.indexOf('BROADCAST') >= 0) logColor = 'var(--warning)';
                    else if (l.message.indexOf('RECEIVE') >= 0) logColor = 'var(--success)';
                    else if (l.message.indexOf('OFFLINE') >= 0) logColor = 'var(--danger)';
                    logHtml += '<div style="color:' + logColor + ';border-bottom:1px solid #222;padding:3px 0;"><span style="color:var(--text-secondary);">[' + l.time + ']</span> ' + l.message + '</div>';
                }
                logEl.innerHTML = logHtml || '<div style="color:var(--text-secondary)">Chưa có hoạt động...</div>';
                
            } catch (e) {
                console.log('P2P error:', e);
            }
        }

        async function toggleNode(nodeId) {
            await fetch(`/api/p2p/toggle/${nodeId}`, {method: 'POST'});
            refreshP2P();
            log(`[P2P] Đã chuyển đổi trạng thái node`);
        }

        async function deleteWallet() {
            let selected = document.querySelector('input[name="wallet-select"]:checked');
            if (!selected) { alert('Vui lòng chọn ví cần xóa từ Danh Sách Ví!'); return; }
            if (!confirm('Hành động này không thể hoàn tác. Bạn có chắc chắn muốn xóa ví này?')) return;
            
            try {
                let res = await fetch('/api/wallet/delete', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({public_key: selected.value})
                });
                let d = await res.json();
                
                if (d.success) {
                    log('[OK] Đã xóa ví khỏi hệ thống.');
                    updateWalletSelects();
                    alert('Đã xóa ví thành công!');
                } else {
                    log('[ERROR] Lỗi xóa ví: ' + d.error);
                    alert('Lỗi: ' + d.error);
                }
            } catch (e) {
                log('[ERROR] Lỗi kết nối: ' + e.message);
                alert('Lỗi kết nối server!');
            }
        }

        // Init
        updateWalletSelects();
        refresh();
        refreshP2P();
        setInterval(updateAuto, 3000);
        setInterval(refreshP2P, 5000);
    </script>
</body>
</html>'''

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/api/chain')
def get_chain(): return jsonify({"chain":[b.to_dict() for b in bc.chain],"length":len(bc.chain),"pending":bc.pending_transactions,"difficulty":bc.difficulty})

@app.route('/api/wallet/create',methods=['POST'])
def create_wallet_api():
    d=request.json
    name=d.get('name','Wallet')
    wallet=create_wallet(name)
    return jsonify({"success":True,"wallet":wallet.to_dict()})

@app.route('/api/wallets')
def get_wallets():
    return jsonify({"wallets":[w.to_dict() for w in wallets.values()]})

@app.route('/api/wallet/delete',methods=['POST'])
def delete_wallet_api():
    d=request.json
    pk=d.get('public_key')
    if pk in wallets:
        del wallets[pk]
        return jsonify({"success":True})
    return jsonify({"success":False,"error":"Không tìm thấy ví!"})

@app.route('/api/tx/signed',methods=['POST'])
def add_signed_tx():
    d=request.json
    sender_pk=d.get('sender_pk')
    receiver=d.get('receiver')
    amount=d.get('amount',0)
    
    # Tìm wallet
    if sender_pk not in wallets:
        return jsonify({"success":False,"error":"Khong tim thay vi!"})
    
    wallet=wallets[sender_pk]
    
    # Ký giao dịch
    signed_tx=wallet.sign_transaction(receiver, amount)
    
    # Thêm vào blockchain
    success, msg = bc.add_transaction(signed_tx["sender"], signed_tx["receiver"], signed_tx["amount"], signed_tx["signature"])
    
    if success:
        return jsonify({"success":True,"message":"Giao dich da ky va gui thanh cong!","tx":signed_tx})
    return jsonify({"success":False,"error":msg})

@app.route('/api/tx',methods=['POST'])
def add_tx():
    d=request.json
    bc.add_transaction(d['sender'],d['receiver'],d['amount'])
    return jsonify({"message":"Giao dich da them!"})

@app.route('/api/balance/<addr>')
def get_balance(addr): return jsonify({"address":addr,"balance":bc.get_balance(addr)})

@app.route('/api/stats')
def get_stats():
    return jsonify({"history":bc.mining_history,"total_reward":sum(h["reward"] for h in bc.mining_history),"total_nonces":sum(h["nonce"] for h in bc.mining_history)})

@app.route('/api/auto/start',methods=['POST'])
def start_auto(): d=request.json;auto_miner.start(d.get('miner','Miner'),d.get('interval',10));return jsonify({"ok":True})

@app.route('/api/auto/stop',methods=['POST'])
def stop_auto(): auto_miner.stop();return jsonify({"ok":True})

@app.route('/api/auto/status')
def auto_status(): return jsonify(auto_miner.get_status())

@app.route('/api/auto/progress')
def mining_progress(): return jsonify(auto_miner.get_mining_progress())

@app.route('/api/p2p/status')
def p2p_status(): return jsonify(p2p_network.get_network_status())

@app.route('/api/p2p/toggle/<node_id>', methods=['POST'])
def toggle_node(node_id):
    success = p2p_network.toggle_node(node_id)
    return jsonify({"success": success})

@app.route('/api/p2p/sync', methods=['POST'])
def sync_network():
    p2p_network.sync_all_nodes()
    return jsonify({"success": True})

# ==========================================
# RUN SERVER
# ==========================================
server = make_server('127.0.0.1', 5000, app, threaded=True)
def run(): server.serve_forever()
thread = threading.Thread(target=run, daemon=True)
thread.start()
time.sleep(1)
webbrowser.open('http://127.0.0.1:5000')
print("Blockchain Demo dang chay tai: http://127.0.0.1:5000")
print("De dung server, restart kernel cua Jupyter")