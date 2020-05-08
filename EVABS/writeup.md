# EVABS

Link tải file apk: [EVABSv4.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/EVABSv4.apk)

## Level 1 - Debug Me

Sử dung **adb logcat** để xem log của ứng dụng

![logcat](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv1-0.PNG)

**Flag: EVABS{logging_info_never_safel}**

## Level 2 - File Access

![assets](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv2-0.PNG)

Theo như gợi ý thì chúng ta cần tìm flag trong **assets directory**. Chỉ cần đổi đuôi file .apk -> .zip và giải nén. Sau đó vào thư mục assets và ta thấy 1 file secret chứa flag

**Flag: EVABS{fil3s_!n_ass3ts_ar3_eas!ly_hackabl3}**

## Level 3 - Strings

![strings](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv3-0.PNG)

Quá quen thuộc, decompile bằng apktool và strings.xml thẳng tiến.

**Flag: EVABS{saf3ly_st0red_in_Strings?}**

## Level 4 - Resource

![Resource](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv4-0.PNG)

Flag giấu trong 1 file nằm tại folder res. Chạy 1 command là biết được flag đặt trong res/raw/link.txt: ``` grep -r "EVABS{" * ```

**Flag: EVABS{th!s_plac3_is_n0t_as_s3cur3_as_it_l00ks}**

## Level 5 - Shares and Preferences

![Resource](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv5-0.PNG)

Kiểm tra SharedPreferences: SharedPreferences là một API lưu trữ dữ liệu vĩnh viễn trong các file XML. Dữ liệu được lưu trữ bởi SharedPreferences object có cấu trúc dạng key - value. SharedPreferences object có thể được khai báo cho tất cả ứng dụng sử dụng, hoặc khai báo private. Dữ liệu được lưu trong các file XML tại /data/data/<package-name>/shared_prefs/*.xml

Sử dụng ``` adb shell ``` để truy cập vào hệ thống máy android. ``` cd /data/data/com.revo.evabs/shared_prefs ``` và chạy lệnh ``` grep -r "EVABS" * ``` để tìm flag giấu trong các file xml.

**Flag: EVABS{shar3d_pr3fs_c0uld_be_c0mpromiz3ds}**

## Level 6 - DB leak

![SQLite](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv6-0.PNG)

Chạy ``` adb shell "ls /data/data/com.revo.evabs/databases" ``` để kiểm tra xem có những db nào. Ở đây chỉ có 1 db là MAINFRAME_ACCESS.

Pull db đó về máy thật để mở bằng SQLite browser bằng lệnh ``` adb pull "/data/data/com.revo.evabs/databases/MAINFRAME_ACCESS" "/home/tran.minh.nhat/Downloads/MAINFRAME_ACCESS" ```

Xem các bảng thấy flag là password của user Dr.l33t có role admin.

**Flag: EVABS{sqlite_is_not_safe}**

## Level 7 - Export

