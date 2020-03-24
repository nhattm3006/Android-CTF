# Picoctf 2019: Droids3

Link tải file apk: [three.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/three.apk)

## Tìm hiểu ứng dụng

Các chức năng của ứng dụng không có gì thay đổi so với bài Droid0. Vẫn là 1 trường input, 2 phần text và 1 button.

Khi click vào button sẽ hiện text "don't wanna", và hint là "make this app your own".

## Tìm flag

Đây là source code sau khi reverse mà chúng ta cần quan tâm:

![FlagstaffHill](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/three0.PNG)

Ở đây chúng ta để ý thấy có 2 hàm **nope()** và **yep()**. Hàm **getFlag()** lại trả về kết quả của hàm nope - "don't wanna". Vậy thì cái chúng ta cần ở đây là getFlag phải return yep. Để làm được điều đó chúng ta cần sử dụng kỹ thuật ***patch*** lại app.

Trước khi giới thiệu về kỹ thuật patch thì mình sẽ nói qua về cấu trúc của file apk. File apk thực chất là một dạng file nén như zip, rar, v..v.. Chúng ta hoàn toàn có thể rename three.apk thành three.zip và giải nén ra bình thường. Tất nhiên các file sau khi giải nén ra chưa thể xem trực tiếp được luôn

![unzip](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/three1.PNG)

Trong các file giải nén ra có 1 file **class.dex**, file này chứa các class trong code java. Khi làm ứng dụng Android thì lập trình viên sẽ code bằng java/kotlin. Khi compile thì các file class sẽ được nén lại thành 1 file dex.

![compile](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/three2.PNG)

Khi thực hiện reverse file apk thì chúng ta sẽ không nhận được các file code bằng java đâu, thay vào đó chúng ta sẽ nhận được các file smali code. Từ các file smali này, decompiler sẽ chuyển sang code java để chúng ta đọc, nhưng sẽ không chính xác hoàn toàn, và sẽ có sự khác biệt khi sử dụng các decompiler khác nhau. Thứ có độ tin cậy cao nhất khi thực hiện reverse app là smali code (smali code trong reverse android có vai trò như assembly code trong reverse exe, elf vậy).

Mình chỉ giới thiệu sơ qua như vậy thôi. Giờ thì chúng ta sẽ bắt tay vào việc path lại app.

#### Đầu tiên chúng ta sẽ decompile file apk bằng apktool

Để file apk và apktool cùng thư mục và chạy lệnh: ``` java -jar apktool_2.4.1.jar d three.apk ```

![apktool-d](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/three3.PNG)

Kết quả sẽ được folder three với các sub folder, file

#### Tiếp theo chúng ta sẽ tiến hành sửa code

Mở file three/smali/com/hellocmu/picoctf/FlagstaffHill.smali

Mình sử dụng VScode cài thêm extension smali để dễ nhìn hơn, tiện cho việc sửa code.

![smali](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/three5.PNG)

Chúng ta sẽ chú ý vào hàm getFlag, chỗ mình gạch chân **->nope** tương ứng với ***return nope*** trong code java. Bây giờ cùng xem lại code java:
- Thứ nhất: chúng ta cần hàm getFlag phải return yep thay vì return nope
- Thứ hai: cả hai hàm yep và nope đều có cùng argument

=> Vậy, để getFlag return yep thì chúng ta chỉ cần đổi **->nope** thành **->yep**, sau đó save lại file.

### Bước 3: build lại thành file apk mới

Khi đã sửa được code theo ý muốn, chúng ta cần từ các file đó build ra file apk mới. apktool cũng có chức năng cho phép build ra file apk sau khi sửa code, chỉ cần chạy lệnh: ``` java -jar apktool_2.4.1.jar b three ```

![apktool-b](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/three6.PNG)

File apk mới nằm tại thư mục three/dist.

![hold-up](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/hold-up.png)

File three.apk mới này không cài được ngay đâu, chúng ta cần làm tiếp bước cuối cùng.

### sign apk

Các bạn hãy copy 2 câu lệnh sau vào file text:

```
keytool -genkeypair -v -keystore key.keystore -alias publishingdoc -keyalg RSA -keysize 2048 -validity 10000

jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore ./key.keystore %1 publishingdoc
```

Đổi tên file thành **sign-apk.bat** sau đó chạy lệnh cmd: ``` sign-apk.bat [file-name].apk ```

Lần lượt điền keystore và các thông tin, các bạn thích điền gì cũng được, mình để "123123" hết. Lệnh đầu tiên sẽ tạo **key.keystore**, lệnh thứ 2 sẽ sign apk bằng key vừa tạo.

![gen-key](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/three7.PNG)

![sign](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/three8.PNG)

Như vậy là chúng ta đã sign thành công file apk patched. Giờ chỉ cần xóa ứng dụng cũ trong giả lập, cài ứng dụng mới đã patch vào và bấm nút để nhận flag.

![get-flag](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/image/three9.PNG)

**Flag: picoCTF{tis.but.a.scratch}**
