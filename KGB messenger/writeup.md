# KGB messenger

Link tải file apk: [kgb-messenger.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/kgb-messenger.apk)

Theo thông tin từ [repo gốc](https://github.com/tlamb96/kgb_messenger) thì app này có 3 flag ở 3 mức độ dễ - trung bình - khó.

## Alert (trung bình)

Đây là chướng ngại đầu tiên chúng ta phải vượt qua nếu muốn tiếp cận các thông tin bí mật của tổ chức tình báo Nga. Ngay khi vừa bật app lên chúng ta đã nhận được không báo rằng chỉ thiết bị của Nga mới có thể sử dụng được app.

![rusian-devices](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb10.PNG)

Đoạn check Russian Devices nằm trong class MainActivity

![check-devices](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb11.PNG)

Việc kiểm tra khá là phức tạp khi chúng ta cần phải vượt qua 2 if condition, mỗi lần đều phải thỏa mãn cả 3 yêu cầu thì mới sử dụng app được. Tất nhiên là nếu đã định patch lại ứng dụng thì chúng ta chẳng việc gì phải quan tâm xem làm sao để thỏa mãn tất cả các điều kiện, chỉ cần xác định xem vị trí mà chúng ta cần lệnh if nhảy vào là được.

Bây giờ thì decompile và xem code smali. Vì sử dụng 2 cấu trúc if - else nên trong code smali có 4 nhánh kết quả: cond_0 cond_1 cond_2 con_3. Đối chiếu với code java đã reverse, chúng ta có sơ đồ sau:

![if-map](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb12.PNG)

Xác định được target rồi thì câu chuyện lại đơn giản quá. Lệnh smali **if-nez** sẽ thực hiện so sánh và nhảy đến đoạn code xác định. Chúng ta chỉ cần sửa những chỗ lệnh if-nez nhảy đến **:cond_0** thành **:cond_1**, và sửa những chỗ nhảy đến **cond_2** thành **cond_3**.

Sau khi patch lại apk, chúng ta đã có thể sử dụng app. Các bạn có thể xem code mới tại [đây](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/code/MainActivity.smali).

![toLogin](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb13.PNG)

Ờ nhưng mà flag đâu ??? Theo như thiết kế thì tại bước bypass check devices này mình sẽ lấy được flag đầu tiên mà sao không thấy gì nhỉ ?

Hóa ra ở if condition 2 có một string với **id = 2131558400 (hex value: 7f0d0000)**. Tìm trong public.xml chúng ta biết được **resourse name = User**. Tìm resource name này trong strings.xml chúng ta thấy string value là một đoạn B64 = **RkxBR3s1N0VSTDFOR180UkNIM1J9Cg==**. Decode B64 và chúng ta sẽ được flag đầu tiên.

**Flag 1: FLAG{57ERL1NG_4RCH3R}**

## Login (dễ)

Phần code của chức năng login nằm trong file LoginActivity.class

![login-activity-1](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb20.PNG)

![login-activity-2](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb21.PNG)

Đọc code đã reverse thì chúng ta xác định được luôn 2 string **n** và **o** lần lượt là ***username*** và ***password*** nhập vào. Tại hàm onLogin() - xử lý các logic đăng nhập có truy cập 1 resourse id như các bài trước đó, làm tương tự chúng ta tìm đc username = **codenameduchess**

![username](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb22.PNG)

Chúng ta lấy được cả 1 value password = **84e343a0486ff05530df6c705c8bb4** luôn nhưng không login đc, app báo wrong password và cũng không tìm được giá trị trước khi hash. Kiểm tra kỹ hơn class LoginActivity, cụ thể là hàm j() chúng ta biết rằng đoạn string đó là giá trị password sau khi hash MD5, nhưng đã bị xóa đi 2 ký tự.

![func-i](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb23.PNG)

Hàm i() là hàm decode từ username và password đúng ra flag, chỉ dùng phép xor thôi. Nội dung flag có 10 ký tự, trong đó có 4 ký tự được xor với password đúng nên có thể thử guessing được: ***FLAG{G??G13??R0}***

Làm đến đây thì mình phải xem writeup của người khác. Hóa ra đúng như trong repo gốc đã nói trước thì flag này cần kỹ năng recon. Search từ khóa "codenameduchess" thì kết quả đầu tiên là trang twitter Sterling Archer, trùng với string value của resource user.

![codenameduchess](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb24.PNG)

Sau đó mình search từ khóa "Sterling Archer password" thì tìm được password là **guest**.

![Sterling](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb25.PNG)

![flag2](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb26.PNG)

**Flag 2: FLAG{G00G13_PR0}**

## Social Engineering (khó)

