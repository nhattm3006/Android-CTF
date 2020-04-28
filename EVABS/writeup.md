# EVABS

Link tải file apk: [EVABSv4.apk](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/EVABSv4.apk)

## Level 1 - Debug Me

Sử dung **adb logcat** để xem log của ứng dụng

![logcat](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv1-0.PNG)

**Flag: EVABS{logging_info_never_safel}**

## Level 2 - File Access

![hint](https://github.com/MinhNhatTran/Android-CTF/blob/master/EVABS/image/lv2-1.PNG)

Theo như gợi ý thì chúng ta cần tìm flag trong **assets directory**. Chỉ cần đổi đuôi file .apk -> .zip và giải nén. Sau đó vào thư mục assets và ta thấy 1 file secret chứa flag

**Flag: EVABS{fil3s_!n_ass3ts_ar3_eas!ly_hackabl3}**

## Level 3 - Strings

