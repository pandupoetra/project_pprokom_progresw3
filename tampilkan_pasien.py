daftar_pasien=[]
def tampilkan_daftar_pasien():
    # membuat informasi awal jika memasuki menu menampilkan daftar pasien
    print("\n------- Daftar Pasien -------")
    # mebuat percabangan untuk mengecek adanya data dalam varaibel array daftar pasien 
    if not daftar_pasien:
        print("Daftar pasien kosong.")
    else:
        print("Daftar Pasien:")
        #melakukan perulangan untuk menampilkan data pasien yang ada dalam varaibel daftar pasien 
        for pasien in daftar_pasien:
            print(f"Nama: {pasien['nama']}")
            print(f"Umur: {pasien['umur']}")
            print(f"Alamat: {pasien['alamat']}")
            print(f"Tanggal: {pasien['tanggal']}")
            print(f"Keluhan: {pasien['keluhan']}")
            print(f"nomor urut:{pasien['nomor urutan']}")
            print("-----------------------------")