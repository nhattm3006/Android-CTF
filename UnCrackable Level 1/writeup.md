# UnCrackable Level 1

Link tải file apk: [UnCrackable-Level1.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/UnCrackable-Level1.apk)

UnCrackable Level 1 là bài đầu tiên về reverse android apk trong series bài luyện tập mobile reverse engineeing của Owasp.

Link repo gốc: https://github.com/OWASP/owasp-mstg/tree/master/Crackmes

Để đúng với mục đích luyện tập thì mình sẽ làm bài này bằng cả 2 kỹ thuật trong quá trình reversing: phân tích tĩnh (Static analysis) và phân tích động (Dynamic analysis)

## Cấu trúc code decompiled

Cấu trúc file code decompiled bằng bytecode viewer:

```
sg.vantagepoint/
├── a/
│   ├── a.class
│   ├── b.class
│   ├── c.class
└── uncrackable1/
    ├── a.class
    ├── MainActivity$1.class
    ├── MainActivity$2.class
    └── MainActivity.class
```

***Tên file và tên hàm toàn a b c nên có thể gây nhầm lẫn, rối trong quá trình làm.***

## Bypass root check

Ngay khi mở ứng dụng lên thì sẽ có thông báo "Root detected" hiện lên. Ấn vào button "OK" thì chương trình sẽ tắt luôn.

![root-detect](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-11.PNG)

Vậy thì bước đầu tiên là phải bypass được phần check root. Nếu chỉ để xem các chức năng của app như nào thì có thể cài apk vào 1 thiết bị không bị root là được. Tất nhiên là chúng ta không làm thế, nếu bị detect thì mình bypass thẳng luôn.

Code phần check root:

![root-code](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-12.PNG)

Việc kiểm tra root được thực hiện bằng 3 cách, class c trong package **sg.vantagepoint.a** sẽ làm việc này

![c.class](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-13.PNG)

#### Static: patch apk

Decompile bằng apktool: ``` java -jar apktool_2.4.1.jar d UnCrackable-Level1.apk ```

Sửa code 3 hàm **c.a()**, **c.b()** và **c.c()** trong smali/sg/vantagepoint/a. Cách sửa rất đơn giản, chỉ cần ***đảm bảo 3 hàm này luôn return false*** là được: sửa các đoạn **const/4** trước lệnh **return** thành khai báo 0x0 hết. VD: ``` const/4 v0, 0x1 ``` -> ``` const/4 v0, 0x0 ```

Build lại bằng apktool: ``` java -jar apktool_2.4.1.jar b UnCrackable-Level1 ```

Tạo key: ``` keytool -genkeypair -v -keystore key.keystore -alias publishingdoc -keyalg RSA -keysize 2048 -validity 10000 ```

Sign new apk: ``` jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore ./key.keystore UnCrackable-Level1.apk publishingdoc ```

Cài đặt lại và không còn thông báo nào hiện l

Code smali đã sửa: [c.smali](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/code/c.smali)

#### Dynamic: hook bằng Frida

Ý tưởng đầu tiên là mình sẽ hook và sửa nội dung 3 hàm **c.a()**, **c.b()** và **c.c()** return false hết. Như vậy sẽ vượt qua được bước check root của app:

```python
import frida
import sys

def onMessage(message, data):
    print(message)

package = "owasp.mstg.uncrackable1"

jscode = """
Java.perform(function () {
    send("[-] Starting hooks sg.vantagepoint.a.c");
    var rootCheck = Java.use("sg.vantagepoint.a.c");
    rootCheck.a.implementation = function() {
        return false;
    };
    rootCheck.b.implementation = function() {
        return false;
    };
    rootCheck.c.implementation = function() {
        return false;
    };

});
"""

process = frida.get_usb_device().attach(package)
script = process.create_script(jscode)
script.on("message", onMessage)
print("[*] Hooking", package)
script.load()
sys.stdin.read()
```

Nhưng không thành công. Mình kiểm tra lại và nghĩ rằng code không sai. Mình đoán lí do hook không thành công là do các hàm này được gọi ngay khi chương trình bắt đầu (được gọi ngay đầu onCreate() ) nên frida không kịp chuẩn bị.

=> Cần tìm 1 hàm chưa được gọi ngay khi chương trình bắt đầu để Frida có thể hook và sửa nội dung.

Chú ý rằng việc đóng app chỉ xảy ra khi thực hiện ấn button OK trong thông báo phát hiện root. Vì thế ý tưởng thứ 2 là hook và thay đổi chức năng của button đó. Đây là lệnh thực thi của button OK:

```java
var2.setButton(-3, "OK", new 1(this));
```

New 1(this) chính là phần code trong MainActivity$1.class:

![system.exit](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-14.PNG)

Khi click button OK thì sẽ chạy hàm System.exit(0), muốn chặn việc đóng chương trình lại thì chúng ta có thể hook và sửa nội dung chức năng exit này:

```python
import frida
import sys

def onMessage(message, data):
    print(message)

package = "owasp.mstg.uncrackable1"

jscode = """
Java.perform(function () {
    send("[-] Starting hooks java.lang.System.exit");
    var sysexit = Java.use("java.lang.System");
    sysexit.exit.implementation = function(var_0) {
        send("[+] Success: prevent application exit");
    };

});
"""

process = frida.get_usb_device().attach(package)
script = process.create_script(jscode)
script.on("message", onMessage)
print("[*] Hooking", package)
script.load()
sys.stdin.read()
```

Thành công, chúng ta đã bypass được phần check root. Thực ra không hẳn là bypass root check vì chúng ta chỉ ngăn được việc chưng trình exit khi ấn button OK thôi. Nhưng cái chúng ta cần thực sự là tiếp cận được các chức năng chính của app, còn việc bypass root hay không, không quan trọng, vì các chức năng còn lại của app không bị ảnh hưởng tùy theo thiết bị root hay không root.

## Get flag

Tại MainActivity của app có chức năng nhập vào input và button kiểm tra. Nếu input đúng (nhập vào flag) thì sẽ có thông báo "Success", ngược lại thì "Nope". Chức năng này được xử lý trong hàm MainActivity.verify()

Việc kiểm tra input được xử lý bởi class **sg.vantagepoint.uncrackable1.a**:

![inputCheck](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-21.PNG)

Không cần để ý chi tiết code làm gì, chúng ta chỉ cần quan tâm xem flow của quá trình check input như nào:

```
-> Decode B64 xâu "5UJiFctbmgbDoLXmpL12mkno8HT4Lv8dlat8FxR2GOc=" và convert sang mảng kiểu byte (1)
   
-> Gọi hàm sg.vantagepoint.uncrackable1.a.b() để convert hex string "8d127684cbc37c17616d806cf50473cc" thành mảng kiểu byte (2)

-> Gọi hàm sg.vantagepoint.a.a.a() với 2 tham số lần lượt là mảng kiểu byte từ bước 2 và bước 1.

-> Chuyển kết quả của hàm sg.vantagepoint.a.a.a() thành String (4)

-> So sánh input nhập vào với string tại bước 4

-> Nếu input giống với string tại bước 4 thì đúng là flag và hiện thông báo Success.
```

Chúng ta sẽ thay đổi flow này, mục đích là lấy được kết quả của hàm sg.vantagepoint.a.a.a() với đúng tham số là 2 mảng byte.

#### Static: patch apk

#### Dynamic: hook bằng Frida

Khi hook bằng frida mình nghĩ ra 2 hướng hook:

**Cách 1:** Sau khi đã chạy 1 lần chức năng check input, sử dụng Java.choose() để tìm trên heap và sử dụng lại chức năng đó với đúng input. Như vậy chúng ta sẽ lấy được kết quả của hàm - flag cần tìm.

Cách này chỉ mới dừng lại ở ý tưởng của mình thôi, chứ mình cũng chưa làm được. Vì việc truyền tham số là mảng kiểu byte vào mình chưa làm được. Nếu muốn chuyển hex string sang mảng byte bằng hàm sg.vantagepoint.uncrackable1.a.b() luôn thì lại rắc rối nữa, vì sg.vantagepoint.uncrackable1.a.b() và sg.vantagepoint.a.a.a() nằm ở 2 class khác nhau.

Vì thế mình cần tìm cách khác để hook

**Cách 2:** Sử dụng Java.use() để hook hàm sg.vantagepoint.a.a.a() và sửa nội dung hàm ngay trước khi hàm đó được chạy. Ý tưởng là mình sẽ hook hàm sg.vantagepoint.a.a.a(), sửa nội dung cho hàm này gọi instance của chính nó trước khi bị hook. Hơi khó hiểu nhỉ, cụ thể như trong hình sau:

![mo-hinh](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-22.PNG)

Theo ý tưởng đó, chúng ta có script:

```python
import frida
import sys
import time

def onMessage(message, data):
    print(message)

package = "owasp.mstg.uncrackable1"

jscode = """
Java.perform(function () {
    send("[-] Starting hooks sg.vantagepoint.a.a");
    var aes_decrypt = Java.use("sg.vantagepoint.a.a");
    aes_decrypt.a.implementation = function(var_0, var_1) {
        var ret = this.a.call(this, var_0, var_1);
        var flag = "";
        
        for (var i=0; i < ret.length; i++){
            flag += String.fromCharCode(ret[i]);
        }
        send("[*] Decrypted flag: " + flag);

        return ret;
    };

});
"""

time.sleep(1)
process = frida.get_usb_device().attach(package)
script = process.create_script(jscode)
script.on("message", onMessage)
print("[*] Hooking", package)
script.load()
sys.stdin.read()
```

Kết quả hook:

![flag](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-23.PNG)
