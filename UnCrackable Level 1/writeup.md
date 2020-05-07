# UnCrackable Level 1

Link tải file apk: [UnCrackable-Level1.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/UnCrackable-Level1.apk)

UnCrackable Level 1 là bài đầu tiên về reverse android apk trong series bài luyện tập mobile reverse engineeing của Owasp.

Link repo gốc: https://github.com/OWASP/owasp-mstg/tree/master/Crackmes

Để đúng với mục đích luyện tập thì mình sẽ làm bài này bằng cả 2 kỹ thuật trong quá trình reversing: phân tích tĩnh (Static analysis) và phân tích động (Dinamic analysis)

## Cấu trúc code decompiled

Cấu trúc file code decompiled bằng bytecode viewer:

```
sg.vantagepoint
└───a  
|   |   a.class
|   |   b.class
|   |   c.class
└───uncrackable1
    |   a.class
    |   MainActivity.class
```

## Bypass root check

Ngay khi mở ứng dụng lên thì sẽ có thông báo "Root detected" hiện lên. Ấn vào button "OK" thì chương trình sẽ tắt luôn.

![root-detect](https://github.com/MinhNhatTran/Android-CTF/blob/master/UnCrackable%20Level%201/image/uncrackable1-11.PNG)

Vậy thì bước đầu tiên là phải bypass được phần check root. Nếu chỉ để xem các chức năng của app như nào thì có thể cài apk vào 1 thiết bị không bị root là được. Tất nhiên là chúng ta không làm thế, nếu bị detect thì mình bypass thẳng luôn.
