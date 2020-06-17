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

| Thứ tự | Flag      |
|:------:|-----------|
| 1      | Static 2  |
| 2      | Static 1  |
| 3      | Dynamic 1 |
| 4      | Dynamic 2 |
| 5      | Static 3  |
| 6      | NULL      |

## Get flag

### Static flag 2

Decompile file apk bằng apktool và thực hiện tìm kiếm trong các folder, file.

Static flag 2 nằm tại /assets/ch2.key

### Static flag 1

Reverse file bằng Bytecode Viewer, tìm thấy static flag 2 Challenge1.generateDynamicKey().

### Dynamic flag 1

Tiếp tục tập trung vào class Challenge1. Flow như sau: constructor -> generateKey() -> generateDynamicKey(). Về cơ bản thì hàm generateDynamicKey() sẽ mã hóa DES string **"CyB3r_tRucK_Ch4113ng3"** với 1 khóa được tạo từ Static flag 1 (việc mã hóa thực hiện bằng hàm doFinal).

Giờ thì mình phải sử dụng Frida để lấy được giá trị return của hàm generateDynamicKey(). Do hàm này trả về 1 byte array nên sẽ cần chuyển byte array > string.

Frida script:
```python
import frida, sys

package = "org.nowsecure.cybertruck"

def append_zero(hex):
	if len(hex) == 1:
		return '0'+hex
	return hex

def on_message(message, data):
	if message['type'] == 'send':
		byte_array = message['payload']
		flag = ""
		for byte in byte_array:
			if byte < 0:
				flag += append_zero(str(hex(byte & 0xff))[2:])
			else:
				flag += append_zero(str(hex(byte))[2:])

		print("[*] Flag: {}".format(flag))
	else:
		print(message)
	

jscode = """
Java.perform(function(){
	var Challenge1 = Java.use('org.nowsecure.cybertruck.keygenerators.Challenge1');
	Challenge1.generateDynamicKey.overload('[B').implementation = function(var_1){
		var result = this.generateDynamicKey(var_1);

		send(result);
		return result 
	};
});
"""

process = frida.get_usb_device().attach(package)
script = process.create_script(jscode)
script.on('message', on_message)
print("[*] Hooking", package)
script.load()
sys.stdin.read()
```

Kết quả:

![](https://github.com/MinhNhatTran/Android-CTF/blob/master/CyberTruck2019/image/cybertruck-3.png)

### Dynamic flag 2

Quá dễ, làm 1 được 2. Bê nguyên script lấy Dynamic flag 1 sang để lấy Dynamic flag 2. Lần này Dynamic flag 2 được mã hóa AES bằng hàm keygenerators.a.a(byte[], byte[]).

### Static flag 3

Tại MainActivity ta thấy code load thư viện native-lib.so

Thư viện code luôn được lưu tại /lib/

Chạy command strings lib ra tìm được Static flag 3.

### Dynamic flag 3

Phải reverse lại lib .... đọc code asm... chưa làm được.
