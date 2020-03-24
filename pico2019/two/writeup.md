# Picoctf 2019: Droids2

Link tải file apk: [two.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/two/two.apk)

## Tìm hiểu ứng dụng

Các chức năng của ứng dụng không có gì thay đổi so với bài Droid0. Vẫn là 1 trường input, 2 phần text và 1 button.

Khi click vào button sẽ hiện text "NOPE", và hint là "smali sounds like an ikea bookcase".

Từ hint thì mình đoán được bài này sẽ vẫn phải đi tìm password đúng để nhận flag, nhưng sẽ liên quan đến file **smali**.

## Tìm flag

Reverse file apk bằng Bytecode Viewer và tiếp tục kiểm tra hàm getFlag() tại class FlagstaffHill. Vì đoạn code so sánh dài và khó theo dõi nên mình copy và mở trong vscode.

![FlagstaffHill](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/two/image/two0.PNG)

Có vẻ BTC pico2019 tính toán chưa kỹ lắm vì bài này dễ hơn cả bài Droid1. Ở bài Droid1 thì sau khi reverse app chúng ta chỉ nhận được resource id, nếu sử dụng decompiler khác thì sẽ nhận được luôn cả resourse name mà không cần đi tìm như mình làm. Nếu không có decompiler nào xịn hơn, đưa luôn cả string value vào code thì bài Droid2 chính xác là dễ hơn Droid1.

Chỉ cần decompile ra thôi là chúng ta đã có đoạn code rất tường minh rồi. Mình sẽ chỉnh sửa lại chút để dễ nhìn hơn.

![modify](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/two/image/two2.PNG)

Rất dễ đọc, chỉ đơn giản là so sánh input nhập vào với 1 string được ghép từ các phần tử trong mảng var6. Nếu như là trong ứng dụng thật thì những lỗi lộ thông tin ở ngay trong code như này có tên gọi "hard coded string".

Giờ thì nối các string này với nhau và ta sẽ được password để get flag.

![flag](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/two/image/two1.PNG)

**Flag: picoCTF{what.is.your.favourite.colour}**
