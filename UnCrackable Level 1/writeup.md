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

## Bypass root check

Ngay khi mở ứng dụng lên thì sẽ có thông báo "Root detected" hiện lên. Ấn vào button "OK" thì chương trình sẽ tắt luôn.

![root-detect](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-11.PNG)

Vậy thì bước đầu tiên là phải bypass được phần check root. Nếu chỉ để xem các chức năng của app như nào thì có thể cài apk vào 1 thiết bị không bị root là được. Tất nhiên là chúng ta không làm thế, nếu bị detect thì mình bypass thẳng luôn.

Code phần check root:

![root-code](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-12.PNG)

Việc kiểm tra root được thực hiện bằng 3 cách, class c trong package sg.vantagepoint.a sẽ làm việc này

![c.class](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-13.PNG)

#### Static: patch apk

#### Dynamic: hook bằng Fride

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

