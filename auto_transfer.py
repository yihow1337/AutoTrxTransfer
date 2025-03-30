import time
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider


# Tron 主網節點
client = Tron(network='mainnet')
client = Tron(provider=HTTPProvider(api_key=["api1", "api2", "api3","api4","api5","api6"]))
# 主要錢包的私鑰 (主錢包)
MAIN_WALLET_PRIVATE_KEY = "KEY"
main_wallet = PrivateKey(bytes.fromhex(MAIN_WALLET_PRIVATE_KEY))

# 簽名錢包的私鑰
SIGNER_WALLET_PRIVATE_KEY = "KEY"
signer_wallet = PrivateKey(bytes.fromhex(SIGNER_WALLET_PRIVATE_KEY))

# 目標 TRX 接收地址
TARGET_ADDRESS = "address"

# 設定最低餘額 (手續費 + 0.1 TRX 安全邊界)
MIN_BALANCE_TRX = 1.1

# 監控間隔時間 (秒)
CHECK_INTERVAL = 0.8  # 每  秒檢查一次餘額


def get_balance(address):
    """查詢 TRX 錢包餘額 (轉換為 TRX 單位)"""
    try:
        account = client.get_account(address)
        return account.get("balance", 0) / 1_000_000  # 轉換為 TRX 單位
    except Exception as e:
        print(f"查詢餘額失敗: {e}")
        return 0


def transfer_all_trx():
    """將主錢包的 TRX 轉出"""
    main_wallet_address = main_wallet.public_key.to_base58check_address()
    balance = get_balance(main_wallet_address)

    # 計算最大可轉 TRX
    max_trx_to_send = max(balance - MIN_BALANCE_TRX, 0)

    # 如果 TRX 不足以支付手續費，則不進行轉帳
    if max_trx_to_send <= 0:
        print("❌ 餘額不足，無法轉帳")
        return

    print(f"✅ 發現餘額 {balance} TRX，準備轉出 {max_trx_to_send} TRX")

    try:
        # 創建交易
        txn = (
            client.trx.transfer(main_wallet_address, TARGET_ADDRESS, int(max_trx_to_send * 1_000_000))
            .memo("Auto TRX Transfer")
            .build()
        )

        # 主錢包簽名交易
        signed_txn = txn.sign(main_wallet)

        # 簽名錢包進行二次簽名（多重簽名）
        double_signed_txn = signed_txn.sign(signer_wallet)

        # 廣播交易
        tx_hash = client.broadcast(double_signed_txn)

        print(f"🚀 交易已發送！交易哈希: {tx_hash}")

    except Exception as e:
        print(f"⚠️ 交易失敗: {e}")


if __name__ == "__main__":
    main_wallet_address = main_wallet.public_key.to_base58check_address()
    print(f"🎯 開始監控 TRX 錢包: {main_wallet_address}")

    while True:
        transfer_all_trx()
        time.sleep(CHECK_INTERVAL)  # 等待  秒後再次檢查
