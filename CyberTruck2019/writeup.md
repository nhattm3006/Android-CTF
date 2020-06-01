# CyberTruck2019

Link tải file apk: [cybertruck2019](https://github.com/MinhNhatTran/Android-CTF/blob/master/CyberTruck2019/cybertruck19.apk)

Một bài LAB nghe nói là full frida. Bài LAB tạo bởi nowsecure - 1 team chuyên làm bảo mật mobile, được giới thiệu trong 1 event của họ.

Flag không dễ nhận biết nên mình đã code 1 script python để kiểm tra flag dành cho ai muốn có chương trình kiểm tra flag thay vì đi xem đáp án. Download bằng lệnh:

```
wget https://raw.githubusercontent.com/MinhNhatTran/Android-CTF/master/CyberTruck2019/checkFlagCyberTruck.py
```

Các thông tin thêm về tài liệu, gợi ý, write up và flag đều có thể xem ở [repo gốc](https://github.com/nowsecure/cybertruckchallenge19)

## Challenge1 - DES key: Completely Keyless. Completely safe
- Static: There is a secret used to create a DES key. Can you tell me which one?
- Dynamic: There is a token generated at runtime to unlock the carid=1. Can you get it? (flag must be summitted in hexa all lowercase)

## Challenge2 - AES key: Your Cell Mobile Is Your Key
- Static: This challenge has been obfuscated with ProGuard, therefore you will not recover the AES key.
- Dynamic: There is a token generated at runtime to unlock the carid=2. Can you get it? (flag must be summitted in hexa all lowercase)

## Challenge3 - Mr Truck: Unlock me Baby!
- Static: There is an interesting string in the native code. Can you catch it?
- Dynamic: Get the secret generated at runtime to unlock the carid=3. Security by obscurity is not a great design. Use real crypto! (hint: check the length when summitting the secret!)

## Timeline

| Thứ tự | Flag     |
|:------:|----------|
| 1      | Static 2 |
| 2      | centered      |
| 3      | are neat      |
| 4      | are neat      |
| 5      | are neat      |
| 6      | are neat      |

