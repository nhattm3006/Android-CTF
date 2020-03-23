# Picoctf 2019: Droids1

Link tải file apk: [one.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/one.apk)

## Cài đặt

Sau khi khởi động máy ảo genymotion, tiến hàng cài đặt **one.apk** (nhớ xóa app PicoCTF cài bằng file **zero.apk**, vì tên ứng dụng của các bài picoctf android giống nhau, không gỡ app cũ thì không cài tiếp được).

Từ giờ, thay vì phải vào hẳn đường dẫn chứa adb thì chúng ta sẽ viết 1 file **.bat** cho đỡ mất thời gian. Copy dòng lệnh dưới đây, lưu vào file install_app.txt, sau đó đổi tên file thành install_app.bat

```
"C:\Program Files\Genymobile\Genymotion\tools\adb.exe" install %1
```

Khi cần cài đặt file apk vào máy ảo, chúng ta chỉ cần đặt file apk và file install_app.bat cùng thư mục và chạy lệnh cmd:

```
install_app.bat [tên-file].apk
```

![cmd](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/image/one0.PNG)

## Tìm hiểu ứng dụng

Các chức năng của ứng dụng không có gì thay đổi so với bài Droid0. Vẫn là 1 trường input, 2 phần text và 1 button.

Khi click vào button thì đoạn text đổi thành "NOPE", và hint là "brute force not required". Vậy hẳn là bài này phải nhập đúng **flag** vào trường input để check.

Chúng ta sẽ cần bung code ra để tìm xem input (flag) đúng là gì.

## Tìm flag

Bây giờ chúng ta sẽ reverse file apk để đọc code. Với các app Android thì việc reverse và đọc code đơn giản hơn so với app iOS hoặc các file thường thấy trong các bài ctf RE như: .exe .elf

Chúng ta sẽ sử dụng tool Bytecode Viewer, cách dùng rất đơn giản: mở tool lên, sau đó kéo file apk vào là được. Bytecode Viewer sẽ tự động dịch ngược file apk về code java.

![bytecode-viewer](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/image/one1.PNG)

Tại cửa sổ ***Files*** chúng ta có thể thấy được các file sau khi đã reverse thành công, tool cũng sắp xếp lại các file vào từng folder. Khi mở một file bất kỳ lên thì nội dung sẽ xuất hiện tại cửa sổ ***Work Space***.

Các file code chính sẽ nằm trong đường dẫn **com/hellocmu/picoctf**. Để ý thấy một file có cái tên "đáng ngờ" **FlagstaffHill.class**, click vào file đó để đọc code java.

![FlagstaffHill](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/image/one2.PNG)

Work Space chia thành tận 2 phần: phía bên trái là sử dụng FernFlower Decompiler, còn phía bên phải sử dụng Bytecode Decompiler. Ở đây mình chỉ cần quan tâm đến phần bên trái thôi. Vì sao?

> Vì phần bên trái dễ đọc code hơn chứ sao nữa :v

Và đây là phần code quan trọng nhất:

![getFlag](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/image/one3.PNG)

