# Picoctf 2019: Droids4

Link tải file apk: [four.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/four.apk)

## Tìm hiểu ứng dụng

Các chức năng của ứng dụng không có gì thay đổi so với bài Droid0. Vẫn là 1 trường input, 2 phần text và 1 button.

Khi click vào button sẽ hiện text "don't wanna", và hint là "you got this".

## Tìm flag

Hiện tại mình chưa thấy được thông tin gì từ những dữ kiện trên, vì thế mình sẽ tiếp tục reverse app. Cấu trúc file vẫn tương tự các bài trước đó, và chúng ta kiểm tra class FlagStaffHill.

![FlagstaffHill](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/image/four0.PNG)

Nhìn qua thì cũng không có gì khó khăn lắm hoặc sử dụng các hàm lạ cần tra google. Giờ mình sẽ chỉnh sửa code 1 chút để dễ đọc hơn.

![modify](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/image/four1.PNG)

Ok password đã có, nhập thử thì cũng đúng, in ra "call it" nhưng mà không biết để làm cái gì ??? (không tìm đc password vẫn biết nó in ra "call it" mà :v) Lúc này mình "nghi ngờ" cụm từ ***alphabetsoup*** và tra google thì được một số kết quả sau:

![alphabetsoup](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/image/four2.PNG)

![callit](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/image/four3.PNG)

![letterrip](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/image/four4.PNG)

Khá là khó chơi đấy, but no :D :D :D

![facepalm](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/image/facepalm.jpg)

Các bạn có chú ý cái ảnh thứ 2 không ? cái ảnh mà mình đã chỉnh sửa code và gạch chân đỏ để chú ý đó ? Các bạn có chú ý đến những chỗ không được gạch đỏ không ?

Nếu câu trả lời là có thì chúc mừng, chúng ta giống nhau. Có một hàm **cardamom(String var0)** không được gọi, mặc dù hàm đó cũng nhận input giống hàm getFlag. Giờ chúng ta cần patch file apk, sửa code smali để hàm cardamom() được gọi.

> Ai chưa hiểu rõ thì quay lại đọc kỹ bài [Droid3](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/writeup.md) nhé

#### Decompile

```
java -jar apktool_2.4.1.jar d four.apk
```

#### Sửa code smali

Sửa:

```smali
const-string v5, "call it"
```

Thành:

```smali
invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->cardamom(Ljava/lang/String;)Ljava/lang/String;

move-result-object v5
```

Vì sao lại sửa như vậy ? Đầu tiên chúng ta cần chú ý rằng khi chưa hiểu rõ cách code smali hoạt động thì nên hạn chế tối đa những dòng code cần sửa.

Smali code ban đầu là:

```smali
if-eqz v5, :cond_0

const-string v5, "call it"

return-object v5

.line 37
:cond_0
const-string v5, "NOPE"

return-object v5
```

Trong cả hai trường hợp đều có **return-object v5**, vì vậy chúng ta sẽ giữ nguyên dòng này, chỉ sửa dòng **const-string v5, "call it"** thôi. Nhưng sửa như thế nào ?

Dựa vào các file smali của những bài Droids2 Droids3 trước đó và các file smali của bài Droids4 chúng ta dễ thấy được khi gọi thẳng 1 hàm sẽ sử dụng **invoke-static**. Còn khi gọi dùng dấu ``` . ``` theo kiểu ***var0.equals()*** hay ***"".concat()*** thì sẽ là **invoke-virtual**.

Dù gọi hàm kiểu gì thì sau đó cũng phải return kết quả của hàm hết. Để đưa kết quả return của hàm được gọi vào nơi gọi nó chúng ta sẽ sử dụng **move-result-object**.

Điều thứ 3 là các biến chỉ được thể hiện dưới dạng ký hiệu thôi, mà sửa nhầm tên biến thì kiểu gì cũng không build lại được, vì thế chúng ta phải quan sát và chọn những trong file FlagstaffHill.smali thỏa mãn yêu cầu nhận kết quả return từ hàm. Lúc này mình để ý đến lời gọi constructor init() ở ngay đầu file sử dụng {p0} để nhận kết quả return từ hàm init().

![init](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/image/four6.PNG)

Mình đoán 2 điều:
- Biến p0 này có thể sử đụng để nhận dữ liệu return từ hàm được
- Nó không thấy được sử dụng lại nên có ghi đè vào cũng chẳng chết ai.

Từ những suy luận đó mình sửa file smali, may là chạy được. Lúc build xong mình thấy lúc đấy hơi ngu, lại đi sửa ở nhánh "call it", thế là tí nữa phải nhập đúng pass. Tất nhiên các bạn có thể thử sửa ở nhánh "NOPE" để nếu sửa đúng thì chẳng cần nhập gì vào, cứ bấm nút là ra flag.

Code mới sau khi sửa các bạn có thể xem tại đây: [FlagstaffHill.smali](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/FlagstaffHill.smali)

#### Build apk

```
java -jar apktool_2.4.1.jar b four
```

#### Sign apk

```
sign-apk.bat four.apk
```

Sau đó tiến hành cài đặt và nhập password **alphabetsoup** để lấy flag

![flag](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/image/four5.PNG)

**Flag: picoCTF{not.particularly.silly}**
