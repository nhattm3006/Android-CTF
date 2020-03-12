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

![cmd](https://github.com/MinhNhatTran/Android-CTF/edit/master/pico2019/one/image/one0.PNG)

