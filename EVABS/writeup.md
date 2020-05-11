# EVABS

Link tải file apk: [EVABSv4.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/EVABSv4.apk)

Tại thời điểm mình làm thì LAB này khá mới. Đây là 1 LAB giới thiệu qua về các điểm cần chú ý để tránh gây mất an toàn thông tin trên ứng dụng Android. Khi đã tìm được công cụ, hướng làm rồi thì LAB này không hề khó, chủ yếu để hướng cho người làm biết phải tìm hiểu vấn đề gì thôi.

Các bản mới và thông tin thêm xem tại [repo gốc](https://github.com/abhi-r3v0/EVABS).

## Level 1 - Debug Me

Sử dung **adb logcat** để xem log của ứng dụng

![logcat](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv1-0.PNG)

**Flag: EVABS{logging_info_never_safel}**

## Level 2 - File Access

![assets](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv2-0.png)

Theo như gợi ý thì chúng ta cần tìm flag trong **assets directory**. Chỉ cần đổi đuôi file .apk -> .zip và giải nén. Sau đó vào thư mục assets và ta thấy 1 file secret chứa flag

**Flag: EVABS{fil3s_!n_ass3ts_ar3_eas!ly_hackabl3}**

## Level 3 - Strings

![strings](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv3-0.png)

Quá quen thuộc, decompile bằng apktool và strings.xml thẳng tiến.

**Flag: EVABS{saf3ly_st0red_in_Strings?}**

## Level 4 - Resource

![Resource](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv4-0.png)

Flag giấu trong 1 file nằm tại folder res. Chạy 1 command là biết được flag đặt trong res/raw/link.txt: ``` grep -r "EVABS{" * ```

**Flag: EVABS{th!s_plac3_is_n0t_as_s3cur3_as_it_l00ks}**

## Level 5 - Shares and Preferences

![Resource](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv5-0.png)

Kiểm tra SharedPreferences: SharedPreferences là một API lưu trữ dữ liệu vĩnh viễn trong các file XML. Dữ liệu được lưu trữ bởi SharedPreferences object có cấu trúc dạng key - value. SharedPreferences object có thể được khai báo cho tất cả ứng dụng sử dụng, hoặc khai báo private. Dữ liệu được lưu trong các file XML tại /data/data/<package-name>/shared_prefs/*.xml

Sử dụng ``` adb shell ``` để truy cập vào hệ thống máy android. ``` cd /data/data/com.revo.evabs/shared_prefs ``` và chạy lệnh ``` grep -r "EVABS" * ``` để tìm flag giấu trong các file xml.

**Flag: EVABS{shar3d_pr3fs_c0uld_be_c0mpromiz3ds}**

## Level 6 - DB leak

![SQLite](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv6-0.png)

Chạy ``` adb shell "ls /data/data/com.revo.evabs/databases" ``` để kiểm tra xem có những db nào. Ở đây chỉ có 1 db là MAINFRAME_ACCESS.

Pull db đó về máy thật để mở bằng SQLite browser bằng lệnh ``` adb pull "/data/data/com.revo.evabs/databases/MAINFRAME_ACCESS" "/home/tran.minh.nhat/Downloads/MAINFRAME_ACCESS" ```

Xem các bảng thấy flag là password của user Dr.l33t có role admin.

**Flag: EVABS{sqlite_is_not_safe}**

## Level 7 - Export

![Exported](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv7-0.png)

Ở ngay dòng thứ 4 trong file AndroidManifest.xml đã có ngay thông tin về một Activity bị exported:
```xml
<activity android:exported="true" android:name="com.revo.evabs.ExportedActivity"/>
```

Sử dụng adb để trigger các exported activity.
```
adb shell am start -n com.revo.evabs/com.revo.evabs.ExportedActivity
```

![ExportedActivity](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv7-1.png)

**Flag: EVABS{exp0rted_activities_ar3_harmful}**

## Level 8 - Decode

![Decode](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv8-0.png)

Reverse sang code java bằng Bytecode viewer, sau đó mở file Decode.class - file code java cho level 8 thấy ngay 3 đoạn text hardcoded.

![Decode](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv8-1.png)

Decode hex 3 đoạn này được flag.

**Flag: EVABS{nev3r_st0re_s3ns!tiv3_data_1n_7h3_s0urcec0de}**

## Level 9 - Smali injection

![Smali](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv9-0.png)

Xem source code bằng bytecode viewer:
- SmaliInject.class:
![Smali](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv9-1.png)
- SmaliInject$2.class:
![Smali](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv9-2.png)

Vậy là chỉ cần sửa biến **SIGNAL** trong class SmaliInject từ "LAB_OFF" -> "LAB_ON" rồi build và sign lại app là được. Sau khi cài đặt ấn button TURN ON là sẽ nhận được flag

**Flag: EVABS{smali_inj_is_l3thals}**

## Level 10 - Intercept

![Intercept](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv10-0.png)

Theo như hint thì cần phải intercept request bằng burpsuite. Để intercept được request trên các phiên bản Android từ Android N trở lên thì phải add root CA có thời hạn ngắn. Nếu muốn đơn giản hơn thì chỉ cần cài EVABSv4 lên thiết bị có phiên bản thấp hơn Android N là sử dụng được burp CA.

Sau khi config để intercept được request rồi thì chỉ cần Send to repeater và gửi request lên là được. Trong respond có chứa flag.

![Intercept](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv10-1.png)

**Flag: EVABS{Always_p!n_SSL_C3rtificate}**

## Level 11 - Custom PERM

![useFrida](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv11-1.png)

**Flag: EVABS{always_ver1fy_packag3sa}**

Nhưng mà check thì lại báo sai ???

## Level 12 - Instrument
