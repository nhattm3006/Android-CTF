# Android-CTF

Hệ điều hành: Windows hay Linux đều cài đặt được các tool và môi trường.

Danh sách các tool sử dụng:
- [Java 8u241](https://java.com/en/download/manual.jsp): đa số các tool cho android viết bằng java, bản thân app android cũng viết bằng java. Cài môi trường java 8u241 để dùng được cả các phần mềm Cr@cK, bản java cao hơn không dùng được. 
- [Virtualbox](https://www.virtualbox.org/wiki/Downloads): máy ảo để chạy genymotion, chỉ cần cài virtualbox để cài genymotion là được. Tải riêng bằng link này, hoặc trong link tải genymotion chọn phần "download with virtualbox"
- [Genymotion](https://www.genymotion.com/download/): môi trường chạy file
- ADB: Android Debug Brige - công cụ giúp kết nối với máy ảo Android. ADB có sẵn trong thư mục tools của genymotion, đường dẫn mặc định trên windows là **C:/Program Files/Genymobile/Genymotion/tools**.
- [Apktool](https://ibotpeaches.github.io/Apktool/install/): decompile và build file apk.
- [Dex2jar](https://github.com/pxb1988/dex2jar): chuyển file .dex sang file .class (chuyển file apk sang file jar - có thể đọc được code)
- [JD-gui](http://java-decompiler.github.io/): đọc code file jar
- [Bytecode Viewer](https://bytecodeviewer.com/): "hợp thể" của Dex2jar và JD-gui
- Burp Suite: dùng bản community hoặc tìm các bản Cr@cK trên mạng. Chạy burp Cr@cK bằng java 8u241, bản community dùng java nào cũng được.
- Text editor: sử dụng các text editor hỗ trợ đọc file .smali và .xml tốt (đề nghị dùng [VScode](https://code.visualstudio.com/download) + cài thêm các extension highlight code)

Writeup cho các bài Android CTF:
- Picoctf 2019:
  - [Droids0](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/zero/writeup.md)
  - [Droids1](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/one/writeup.md)
  - [Droids2](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/two/writeup.md)
  - [Droids3](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/three/writeup.md)
  - [Droids4](https://github.com/MinhNhatTran/Android-CTF/blob/master/pico2019/four/writeup.md)
- [KGB messenger](https://github.com/MinhNhatTran/Android-CTF/blob/master/KGB%20messenger/writeup.md)
