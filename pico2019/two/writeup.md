# Picoctf 2019: Droids2

Link tải file apk: [two.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/two/two.apk)

## Tìm hiểu ứng dụng

Các chức năng của ứng dụng không có gì thay đổi so với bài Droid0. Vẫn là 1 trường input, 2 phần text và 1 button.

Khi click vào button sẽ hiện text "NOPE", và hint là "smali sounds like an ikea bookcase".

Từ hint thì mình đoán được bài này sẽ vẫn phải đi tìm password đúng để nhận flag, nhưng sẽ liên quan đến file **smali**.

## Tìm flag

Reverse file apk bằng Bytecode Viewer và tiếp tục kiểm tra hàm getFlag() tại class FlagstaffHill. Vì đoạn code so sánh dài và khó theo dõi nên mình copy và mở trong vscode.

![FlagstaffHill]()

