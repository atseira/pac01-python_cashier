Latar belakang problems
Penjelasan requirements / objectives yang dibutuhkan untuk membuat program
Penjelasan alur code atau flowchart.
Penjelasan mengenai functions atau attribute yang dibuat dan fungsinya untuk apa
Demonstrasi code dengan Test Case yang diberikan dan outputnya bagaimana
Conclusion

## Latar Belakang
Seorang pemilik supermarket besar di salah satu kota di Indonesia memiliki rencana untuk melakukan perbaikan proses bisnis, yaitu membuat sistem kasir yang self-service di supermarket miliknya dengan harapan Customer bisa langsung memasukkan item yang dibeli, jumlah item yang dibeli, dan harga item yang dibeli dan fitur yang lain.

## Kebutuhan
Customer dapat melakukan hal-hal berikut:
* memulai transaksi dengan menginstansi objek `Transaction()`
* menambah item dengan menggunakan method `add_item()` disertai argumen nama item, jumlah item, dan harga per item
* mengubah nama, jumlah, atau harga item dengan method `update_item_name()`, `update_item_qty()`, `update_item_price()`
* menghapus salah satu item dengan `delete_item()`
* menghapus seluruh item dengan `reset_transaction()`
* mengecek daftar belanjaan dengan `check_order()`
* melakukan `check_out()` dan mendapatkan perhitungan dan diskon, jika ada. Setiap kali `check_out()` dilakukan, data transaksi masuk ke dalam database.

## Penjelasan dan contoh
Ada dua class: `Transaction` dan `Item`.
Customer akan menggunakan kasir lewat kode Python, cukup dengan class `Transaction` saja. Data pembelian disimpan oleh `Transaction` sebagai dictionary dengan nama item sebagai key dan object `Item` sebagai value yang memuat jumlah dan harga per item.

```
# inisiasi
trx = Transaction()
assert f"{trx} == "{}"

# menambah item
trx.add_item('Ayam Goreng', 2, 20000)
assert f"{trx}" == "{'Ayam Goreng': [2, 20000]}"

# mengubah nama, jumlah, atau harga
trx.update_item_name('Ayam Goreng', 'Fried Chicken')
trx.update_item_qty('Fried Chicken', 1)
trx.update_item_price('Fried Chicken', 30000)
assert f"{trx}" == "{'Fried Chicken': [1, 30000]}"

# menghapus sebuah item
trx.delete_item('Fried Chicken')
assert f"{trx} == "{}"

# menghapus seluruh item
trx.reset_transaction()
assert f"{trx} == "{}"

# menambah item & cek pesanan
trx.add_item('Ayam Goreng', 2, 20000)
trx.check_order()

# melakukan check_out & memasukkan transaksi ke database
trx.check_out() 
```
Method `check_out()` dari `Transaction` akan menghitung total belanjaan. Total belanjaan lalu akan dikurangi diskon dan ditampilkan harga final. Perhitungan diskon untuk sekarang ada 2 cara.

### Aturan diskon
Tanpa settingan apapun, secara default promo yang akan digunakan adalah promo per item (`BY_ITEM`). Sekarang ada dua jenis promo, `BY_ITEM` dan `BY_TRX` dengan peraturan lengkap di bawah. Contoh code mengganti promo:
```
trx.set_promo(promos.BY_TRX)
```

#### Promo per item (BY_ITEM)
* Jika total harga item di atas Rp200.000 maka harga item tersebut dikenakan diskon 5%
* Jika total harga item di atas Rp300.000 maka harga item tersebut dikenakan diskon 6%
* Jika total harga item di atas Rp500.000 maka harga item tersebut dikenakan diskon 7%

Contoh perhitungan:

| Nama Item              | Qty | Harga Item | Subtotal | Diskon | Setelah diskon |
|------------------------|-----|------------|----------|------------|----------------|
| Ayam Goreng           | 2    | 20,000        | 40,000      | 0              | 40,000             |
| Mainan Tamiya Paket | 1    | 300,000      | 300,000    | 5%           | 285,000           |
| Total                        |     |                | 340,000    | 4.41%        | 325,000           |

#### Promo per transaksi (BY_TRX)
* Jika total nilai transaksi di atas Rp200.000 maka akan mendapatkan diskon 5%
* Jika total nilai transaksi di atas Rp300.000 maka akan mendapatkan diskon 6%
* Jika total nilai transaksi di atas Rp500.000 maka akan mendapatkan diskon 7%
Contoh perhitungan:

| Nama Item            | Qty | Harga Item | Subtotal | Diskon (%) | Setelah diskon |
|----------------------|-----|------------|----------|------------|----------------|
| Ayam Goreng         | 2    | 20,000         | 40,000      | 0%           | 40,000             |
| Mainan Tamiya Paket | 1    | 300,000       | 300,000    | 0%           | 300,000           |
| Total                    |     |                  | 340,000    | 5.00%        | 323,000           |
<br>

### Struktur Database SQLite

**Table Name:** `transactions`

| **Columns:**                            |
|-----------------------------------------|
| - `id`: INTEGER (PRIMARY KEY, AUTOINCREMENT) |
| - `total_harga_rp`: INTEGER             |
| - `diskon_persen`: INTEGER              |
| - `harga_final_rp`: INTEGER             |

<br>

**Table Name:** `order_details`

| **Columns:**                               |
|--------------------------------------------|
| - `id`: INTEGER (PRIMARY KEY, AUTOINCREMENT)      |
| - `transaction_id`: INTEGER (FOREIGN KEY REFERENCES `transactions`(id)) |
| - `nama_item`: TEXT                              |
| - `jumlah_item`: INTEGER                          |
| - `harga_item`: INTEGER                           |

