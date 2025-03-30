# TRON Auto Transfer Script

本腳本用於監控 TRON (TRX) 主錢包餘額，並在餘額超過設定的最低閾值時，自動將可用 TRX 轉帳至指定目標地址。

## 功能特點
- 監控指定 TRX 錢包餘額。
- 當餘額超過安全邊界 (`MIN_BALANCE_TRX`) 時，自動轉出多餘 TRX。
- 交易採用雙重簽名機制。
- 支援多個 API 金鑰，提高請求穩定性。
- 週期性檢查餘額並自動執行轉帳。

## 環境需求
- Python 3.7 以上
- `tronpy` 套件

## 安裝方式

請先安裝 `tronpy` 依賴套件：

```sh
pip install tronpy
```

## 配置設定

1. 設定 Tron 主網節點：
   ```python
   client = Tron(network='mainnet')
   client = Tron(provider=HTTPProvider(api_key=["api1", "api2", "api3", "api4", "api5", "api6"]))
   ```
2. 設定主要錢包與簽名錢包私鑰：
   ```python
   MAIN_WALLET_PRIVATE_KEY = "你的私鑰"
   SIGNER_WALLET_PRIVATE_KEY = "你的私鑰"
   ```
3. 設定接收 TRX 的目標地址：
   ```python
   TARGET_ADDRESS = "你的目標地址"
   ```
4. 設定最低餘額閾值 (`MIN_BALANCE_TRX`)，確保主錢包保持足夠的 TRX 用於交易手續費。
   ```python
   MIN_BALANCE_TRX = 1.1  # 預留 0.1 TRX 安全邊界
   ```
5. 設定監控頻率 (`CHECK_INTERVAL`)，單位為秒：
   ```python
   CHECK_INTERVAL = 0.8  # 每 0.8 秒檢查一次餘額
   ```

## 使用方式

運行腳本即可開始監控主錢包餘額，並根據設定自動轉帳：

```sh
python auto_transfer.py
```

運行後，終端會顯示當前監控的主錢包地址，並在餘額足夠時自動發送 TRX 交易。

## 注意事項
- **請確保私鑰安全，不要洩露給他人！**
- **最低餘額 (`MIN_BALANCE_TRX`) 建議保留至少 1.1 TRX，以確保支付手續費。**
- **請確認 `TARGET_ADDRESS` 是否正確，以免資金損失。**
- **API 金鑰請填入有效的 API Key，以提高請求成功率。**

## 版權與許可
本專案基於 MIT License 授權，可自由修改與使用，請確保遵循相關法律與規範。

