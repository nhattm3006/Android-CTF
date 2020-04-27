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

Sau khi đăng nhập được rồi thì chúng ta sẽ có 1 màn hình chat, tạm thời mình sẽ không gõ gì vào đây hết. Mình sẽ kiểm tra code trước, LAB này có 3 flag tương ứng với 3 activity, sau khi đã tìm đc 2 flag rồi thì cái cuối cùng cần kiểm tra là **MessengerActicity**.

Phần code của activity này khá dài nên mình sẽ không screenshot hết lên đây. Đọc code lần 1 thì mình thấy vài điểm đáng chú ý sau:

![2string](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb31.PNG)

![ab](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb32.PNG)

![onSendMessage](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb33.PNG)

Nhìn vào hàm **onSendMessage()** chúng ta thấy rằng nếu input nhập vào sau khi được xử lý bởi hàm **b()** trùng với **string r** thì flag sẽ xuất hiện. Vậy thì tìm hiểu xem hàm b() xử lý input như nào thôi. Trước khi phân tích kỹ hàm b() thì mình sẽ cố gắng viết lại thân hàm để dễ nhìn hơn, decompiler này chuyển sang while làm mọi thứ trông hơi rối, trong khi hoàn toàn có thể chuyển thành vòng lặp for tường minh hơn.

![nicelyB](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb34.PNG)

Việc xử lý của hàm b() rất đơn giản thôi. Mỗi ký tự sẽ được dịch phải 0 ~ 7 bit tùy theo index của nó trong mảng, sau đó xor với nội dung ban đầu của chính nó. Cuối cùng đảo ngược thứ tự mảng và ghép lại thành 1 string.

Để lấy lại nội dung ban đầu, chúng ta chỉ cần đảo ngược lại string r và brute force với toàn bộ ký tự printable. Tuy nhiên có 2 điều cần chú ý, đó là:
- Trong code smali thì string r có cái đoạn "\u0000" là null character, nên phải tách string thành mảng các char để xử lý, nếu để nguyên string sẽ dễ gây nhầm lẫn.
- Với các vị trí có index chia hết cho 8, chúng ta không thể tìm lại nội dung ban đầu do phép xor (1 ^ 1 = 0) với chính nó trả về char null.

Code brute force:
```python
import string

r = "\u0000dslp}oQ\u0000 dks$|M\u0000h +AYQg\u0000P*!M$gQ\u0000"
r = list(str(r))
r.reverse()

for i in range(len(r)):
	if i % 8 == 0:
		print("_", end="")
		continue
	
	#brute force
	for char in string.printable:
		x = chr((ord(char) >> (i % 8)) ^ ord(char))
		if x == r[i]:
			print(char, end="")
			break
```

Kết quả: ``` _ay I *P_EASE* h_ve the _assword_ ```

Với 1 chút guessing nữa: ``` May I *PLEASE* have the password? ```

Ồ, có vẻ như không hiệu quả. Mình đã thử thay đổi dấu câu ở cuối nhưng cũng không thấy flag đâu. Có thể do mình đã bỏ sót điều gì đó, vì thế mình kiểm tra kỹ hơn code của MessageActivity và nhận ra: hàm i() sẽ decrypt nội dung flag, nhưng hàm i() sẽ chỉ hoạt động khi 2 string ***q*** và ***s*** không rỗng. String ***s*** sẽ được set giá trị trong if 2 (***if (this.b(var2.toString()).equals(this.r))***), còn String ***q*** sẽ được set giá trị trong if 1 (***if (this.a(var2.toString()).equals(this.p))***) - mình đã bỏ qua phần này khi thấy if 2 sẽ in ra flag :v

Hàm a() hoạt động như sau:

![funcA](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb35.PNG)

Với phép xor thì **(a ^ b) ^ b = a** nên việc đảo ngược thuật toán mã hóa không khó khăn gì.

```python
p = "V@]EAASB\022WZF\022e,a$7(&am2(3.\003"
p = list(str(p))
 
for i in range(len(p) // 2):
	p[i] = chr(ord(p[i]) ^ 0x32)
	p[len(p) // 2 + 1 + i] = chr(ord(p[len(p) // 2 + 1 + i]) ^ 0x41)
 
p.reverse()
print("".join(p))
```

Kết quả: ``` Boris, give me the password ```

Giờ thì mình sẽ nhập ``` Boris, give me the password ```, sau đó nhập tiếp ``` May I *PLEASE* have the password? ```. Nếu không được thì có thể phần dấu câu ở cuối bị sai, hoặc vẫn còn gì đó bị bỏ sót,... Nhưng thật may là mọi thứ hoạt động tốt, và chúng ta đã có flag cuối.

![flag3](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/image/kgb30.PNG)

**Flag 3: FLAG{p455w0rd_P134SE}**
