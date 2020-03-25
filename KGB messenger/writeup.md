# KGB messenger

Link tải file apk: [kgb-messenger.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/kgb-messenger.apk)

Theo thông tin từ [repo gốc](https://github.com/tlamb96/kgb_messenger) thì app này có 3 flag ở 3 mức độ dễ - trung bình - khó.

## Alert (trung bình)

Đây là chướng ngại đầu tiên chúng ta phải vượt qua nếu muốn tiếp cận các thông tin bí mật của tổ chức tình báo Nga. Ngay khi vừa bật app lên chúng ta đã nhận được không báo rằng chỉ thiết bị của Nga mới có thể sử dụng được app.

![rusian-devices]()

Đoạn check Russian Devices nằm trong class MainActivity
