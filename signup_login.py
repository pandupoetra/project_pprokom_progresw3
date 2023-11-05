import getpass
import hashlib
import sqlite3
import os
import re
# init new db
try:
    os.mkdir("./saves")
except FileExistsError: pass
con = sqlite3.connect('saves/db.sqlite')
cur = con.cursor()
try:
    cur.execute('''CREATE TABLE auth
        (username text, password text, salt text)''')
except: pass
con.commit()
con.close()

# static Password Salt: appendet to each password before hashing, from os.urandom(64)
static_passwd_salt = b'%\x89\x08-\x82\xb9\xdf\x07\xbd\xbb\x88]\xa2q\x08\x90\xfb\x97\xa7R\xd5\xfc\xfda\x8b\xdd\xcb\x1c\x00\x84\x0e\xdc\xc4\xc0|1\x02-\xb0y\xff`0!gn\xa7\xdf)=\xba.w\x9f\x0b\x9a\xe6n\x9c\xa6\xc5S\xa0\xa0'

# return user or not found
def Query_user(user):
    con = sqlite3.connect('saves/db.sqlite')
    cur = con.cursor()
    db = [i for i in cur.execute("SELECT * FROM auth")]
    dbpasswd_hash = None
    for i in range(len(db)):
        if db[i][0] == user:
            return db[i]
    return "nf"
    
# Initialising peppers against bruteforce attacks
peppers = []
for i in range(256):
    peppers.append(chr(i))
# generate a random pepper for new user
def rand_pepper():
    bits = bin(ord(os.urandom(1))).replace("0b", "")
    while len(bits) <= 7:
        bits += "0"
    return peppers[int(bits, 2)]
    
# Check password of user
def check_passwd(user, raw_passwd):     
    uq = Query_user(user)
    if uq == "nf":
        return "nf"
    dbpasswd_hash = uq[1]
    usersalt = uq[2]
    for i in peppers:
        passwd = raw_passwd + i
        if hashlib.scrypt(password=passwd.encode("UTF-8"), salt=static_passwd_salt+usersalt, n=16, r=16, p=16).hex() == dbpasswd_hash:
            return True
    return False
def block_and_remove_user(username):
    con = sqlite3.connect('saves/db.sqlite')
    cur = con.cursor()
    # Remove the user from the database
    cur.execute("DELETE FROM auth WHERE username = ?", (username,))
    # Optionally, you can add the username to a blocked list or perform other actions
    con.commit()
    con.close()

#Function to add new users
def signUp():
    print("\nUntuk melakukan Sign UP masukan username dan password terlebih dahulu")
    print("Username harus terdiri minimal 1 huruf kapital, 1 angka, 1 karakter khusus($#@), panjang username minimal 4 karakter dan maksimal 8 karakter, serta tidak boleh terdapat spasi didalamnya")
    while True:
        newUsername = input("Masukan usernamemu : ")
        if (
            len(newUsername) < 4 or
            len(newUsername) > 8 or
            not re.search("[a-z]", newUsername) or
            not re.search("[0-9]", newUsername) or
            not re.search("[A-Z]", newUsername) or
            not re.search("[$#@]", newUsername) or
            re.search(r"\s", newUsername)
        ):
            print("Maaf, username Anda tidak sesuai ketentuan, harap ulangi lagi pembuatan username Anda.")
        else:
            print("Username Anda telah sesuai dengan ketentuan.")
            break
  
    newPassword = getpass.getpass(prompt = "Masukan kata sandi : ", stream = None)
    passConfirm = getpass.getpass(prompt = "Konfirmasi kata sandi : ", stream = None)

    if passConfirm == newPassword:
        print("Selamat data anda sudah tersimpan anda dapat login sekarang\n")
        con = sqlite3.connect('saves/db.sqlite')
        otsalt = os.urandom(63)
        passwd = newPassword + rand_pepper()
        cur = con.cursor()
        if Query_user(newUsername) == "nf":
            cur.execute("INSERT INTO auth VALUES (:user, :passwd, :salt)", {"user":newUsername, "passwd":hashlib.scrypt(password=passwd.encode("UTF-8"), salt=static_passwd_salt + otsalt, n=16, r=16, p=16).hex(), "salt":otsalt})
        else:
            print("Data pengguna telah ditambahkan\n")
        con.commit()
        con.close()
        cont = False
    else:
        print("Terdapat kesalahan, ulangi kata sandi anda")  
            
# log the user in            
def LogIn():
    Username = str(input("\nMasukan username:"))
    if Query_user(Username) == "nf":
        print("That User doesn't exist")
    else:
        Password = getpass.getpass(prompt = "Masukan kata sandi: ", stream = None)
        if check_passwd(Username, Password) == True:
            print("kamu sudah login")
        else:
            print("Terdapat kesalahan kata sandi, masukan kembali kata sandi anda")
            cek=0
            while cek<3:
                Password = getpass.getpass(prompt = "Masukan kata sandi: ", stream = None)
                if cek<2:
                    print("Terdapat kesalahan kata sandi, masukan kembali kata sandi anda")
                cek+=1
                if cek == 3:
                    print("Anda telah melebihi batas percobaan login. Akun Anda akan diblokir dan dihapus.")
                    block_and_remove_user(Username)  # Block and remove the user


def register():
    while True:
        print("\nSingle Sign On ")
        print("a) Sign Up")
        print("b) login")
        pilihan = input("masukan apa yang ingin kamu lakukan: ")
        pilihan=pilihan.lower()
        if pilihan == "a":
            signUp()
        if pilihan == "b":
            LogIn()
            break
        else:
            print("maaf pilihan yang anda pilih tidak ada dalam menu")
            
register()