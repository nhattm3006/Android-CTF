# Picoctf 2019: Droids0

Link tải file apk: [zero.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/zero/zero.apk)

## Cài đặt

Mở emulator lên, sau khi máy ảo khởi động thì copy file **zero.apk** vào cùng thư mục với **adb** để tiến hành cài đặt.

Chạy lệnh cài đặt ứng dụng vào máy ảo: ``` adb install zero.apk ```

![install zero.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/zero/image/zero0.PNG)

Sau khi cài đặt thành công, trên máy ảo sẽ xuất hiện ứng dụng **PicoCTF**

![PicoCTF app](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/zero/image/zero1.PNG)

## Tìm hiểu ứng dụng

Giao diện ứng dụng có các chức năng cơ bản:
- 1: Trường input
- 2: Button
- 3: Hai đoạn text

![giao diện](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/zero/image/zero2.PNG)

Đầu tiên chúng ta sẽ thử tương tác với button xem app hoạt động như nào. Cho dù có nhập gì vào trường input hay không thì khi click vào button, phần text bên dưới button sẽ thay đổi từ "I'm a flag!" sang "Not Today". Ngoài ra thì không còn gì thay đổi nữa.

![test button](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/zero/image/zero3.PNG)

Để ý đoạn text ngay trên cùng app, nó nói rằng
>  where else can output go?[PICO]

Đây chính là hint của bài này: khi click vào button thì chúng ta sẽ nhận được flag, nhưng flag sẽ xuất hiện ở đâu ?  
Theo như mình biết thì có 3 nơi output có thể xuất hiện:
- Ngay trên ứng dụng.
- Output được ghi ra file, lưu trên hệ thống hoặc trong thư mục của app.
- Phản hồi trên log.

## Tìm flag

Phân tích 3 khả năng về nơi flag xuất hiện:

- Đầu tiên là flag hiển thị ngay trên ứng dụng. Khả năng này nhỏ nhưng không phải không có. Ứng dụng này rất đơn giản, và chỉ có 1 màn hình duy nhất. Giả sử flag hiển thị trên ứng dụng thì có khả năng nó đã bị ẩn đi bằng cách điều chỉnh màu chữ trùng với màu nền chẳng hạn. Nếu vậy chúng ta sẽ phải đọc source code của ứng dụng để tìm ra flag.

- Trường hợp thứ 2, flag được ghi ra file, lưu trên thư mục của máy ảo hoặc lưu trong thư mục của app trên máy ảo. Nếu trường hợp này xảy ra, chúng ta sẽ phải tìm ở những đường dẫn mà ứng dụng thường ghi file ra, hoặc tìm đường dẫn cài đặt ứng dụng để kiểm tra.

- Trường hợp cuối cùng, flag được ghi ra log. Trường hợp này dễ tìm nhất, vì chúng ta chỉ cần mở cửa sổ xem log bằng adb.

Bây giờ chúng ta sẽ kiểm tra dừ dễ đến khó, từ trường hợp thứ ba ngược lên.

Xem **log** của máy ảo android bằng lệnh: ``` adb logcat ```

![logcat](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/zero/image/zero4.PNG)\

Và log bắt đầu xổ ra... Click vào button và flag xuất hiện. Trên log cũng xuất hiện flag do những lần trước ấn vào button.

![flag](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/zero/image/zero5.PNG)

Flag: **picoCTF{a.moose.once.bit.my.sister}**
