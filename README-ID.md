# Skrip Otomasi Testnet Pharos

## Deskripsi
Bot testnet Pharos (Insentif) - sebuah skrip Python otomatisasi untuk berinteraksi dengan platform seperti Check-in, Klaim Faucet, Swap (Semua Pasangan), Tambah Likuiditas (Semua Pasangan), kirim token, selesaikan misi, dan Auto Referral.

## Fitur
- **Dukungan Multithread**: Jalankan bot Anda lebih cepat (10 akun dengan pengaturan default selesai dalam 5 menit)

- **Klaim Faucet**: Mendukung klaim faucet resmi secara otomatis

- **Penyelesai Captcha**: Menyelesaikan captcha untuk faucet

- **Check-in**: Mendukung Check-in Harian tanpa terlewat sehari pun

- **Dukungan Proxy**: Mendukung proxy seluler dan proxy reguler.

- **Auto Referral**: Mendukung Pendaftaran akun baru dengan Referral

- **Penanganan Wallet**: Mengacak wallet dan `mengonfigurasi` jeda antar operasi.

- **Pertukaran Token**: Mendukung SEMUA PASANGAN contoh: `USDT-USDC, PHRS-USDT, PHRS-USDC, WPHRS-USDT, WPHRS-USDC`

- **Likuiditas**: Mendukung Deposit SEMUA PASANGAN contoh: `USDT-USDC, WPHRS-USDT, WPHRS-USDC`

- **WRAP/UNWRAP**: Mendukung Wrapping `PHRS ke WPHRS` dan Unwrapping `WPHRS ke PHRS`

- **Penyelesaian Quest**: Mendukung penyelesaian quest otomatis (harus terhubung x)

- **User Agent Acak**: Menghasilkan user agent yang acak, namun masuk akal, untuk setiap akun.

## Prasyarat
Python 3.8 atau lebih tinggi
`pip` (penginstal paket Python)

### Instalasi dan Mulai
1. Kloning repositori:
```bash
git clone https://github.com/rasputingrigori/pharos-testnet-bot.git
cd pharos-testnet-bot
```
2. Buat dan aktifkan lingkungan virtual (disarankan):
```bash
python -m venv venv
```
#### Di Windows
```bash
venv\Scripts\activate
```
#### Di macOS/Linux
```bash
source venv/bin/activate
```

3. Instal dependensi:

`requirements.txt` Anda pastikan `requirements.txt` Anda terlihat seperti ini sebelum menginstal:
```yaml
aiohttp>=3.9.0
asyncio
requests>=2.31.0
web3>=6.0.0
eth-account>=0.10.0
pyjwt>=2.8.0
python-dotenv>=1.0.1
colorama>=0.4.6
aiofiles==23.2.1
```

Kemudian instal:
```bash
pip install -r requirements.txt
```

4. private_key.txt:

    - Buat file bernama `private_key.txt` di direktori root proyek (tingkat yang sama dengan main.py).

    - Tambahkan kunci pribadi Ethereum Anda ke file ini, satu kunci pribadi per baris.

    - Kunci dapat dengan atau tanpa awalan 0x.

    - Contoh:
        ```yaml
        0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
        fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321
        ```

5. Tambahkan Proxy Anda di `proxies.txt`
```yaml
http://login:pass@ip:port
http://login:pass@ip:port
```

6. Tambahkan referral & wallet

- Ubah atau Buat example.env menjadi .env dan isi kode referral Anda di `REF_CODE`

- Isi `wallet.txt` dengan alamat token penerima Anda

Jalankan (modul pertama, lalu modul kedua):
```bash
python main.py
```

## Konfigurasi
Semua pengaturan ada di `.env`. Opsi utama meliputi:

### Pengaturan Fitur
```yaml
AUTO_FAUCET=false

AUTO_LIQUIDITY=true
NUMBER_LIQUIDITY=1
AMOUNT_LIQUIDITY = [1, 5]  # Ini berarti 1%-5% dari token0 akan digunakan

AUTO_SEND=true
NUMBER_SEND=1
AMOUNT_SEND=[0.01,0.022]

AUTO_WRAP=false
AUTO_UNWRAP=false
NUMBER_WRAP_UNWRAP=1
AMOUNT_WRAP_UNWRAP=[0.1,0.21]

AUTO_SWAP=false
NUMBER_SWAP=1
AMOUNT_SWAP=[1,2]

AUTO_CHECKIN=false
```

## Berkontribusi
Kontribusi dipersilakan! Jangan ragu untuk mengirimkan pull request atau membuka issue untuk setiap bug, fitur, atau peningkatan.

## Penafian
- Bot ini dimaksudkan untuk tujuan pendidikan dan pengujian, khususnya untuk berinteraksi dengan lingkungan testnet Pharos.

- Pengguna bertanggung jawab penuh untuk memastikan penggunaan bot ini sesuai dengan persyaratan layanan Pharos dan kebijakan platform yang berlaku.

- Pemelihara proyek ini tidak bertanggung jawab atas penyalahgunaan, pembatasan akun, atau konsekuensi lain yang timbul dari penggunaan bot ini.

## Lisensi
Proyek ini adalah open-source—modifikasi dengan "MIT License" dan distribusikan sesuai kebutuhan.