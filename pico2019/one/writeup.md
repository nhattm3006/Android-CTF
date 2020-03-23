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

![MainActivity](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/image/one4.PNG)

![getFlag](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/image/one3.PNG)

Khi không biết bắt đầu từ đâu thì mình nên đi từ **MainActivity** trước, đây là giao diện chính của app, tương tự main trong codeing vậy. Đọc code trong MainActivity chúng ta thấy được khi button được click, thì input chúng ta nhập sẽ được truyền vào FlagstaffHill.getFlag().

Hàm getFlag() trong FlagstaffHill sẽ trả về kết quả khi so sánh input nhập vào với flag. Nhưng có làm thì mới có ăn, flag không được dọn ra ngay đấy mà chúng ta phải đi tìm tiếp. ``` var1.getString(2131427375) ``` sẽ trả về string có id = 2131427375, muốn biết nội dung string, chúng ta phải tìm dựa vào id đó.

Để tìm được string có id đó thì bắt buộc chúng ta phải hoàn toàn reverse file apk ra mới được, Bytecode Viewer cũng có sẵn chức năng export các file đã reverse: File > Save As Zip

Sau khi giải nén chúng ta kiểm tra trong **Decoded Resources/res/values/public.xml** trước. Trong đây sẽ lưu các ***resource name*** và ***resource id*** sử dụng trong code. Dễ thấy được các resource id đều đang ở dạng hex, vì thế chúng ta cần encodeHex(2131427375) = 7f0b002f.

![public-xml](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/image/one5.PNG)

Ứng với id 0x7f0b002f là string name ***password***. Khi có được string name rồi thì chúng ta có thể tìm được value của string đó tại **Decoded Resources/res/values/strings.xml**.

![strings-xml](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/image/one6.PNG)

Và password là **opossum** -> Nhập vào ứng dụng test thử...

![flag](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/image/one7.PNG)

**Flag: picoCTF{pining.for.the.fjords}**
