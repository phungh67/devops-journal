[Về đầu trang](../../README.md)

[Về đề mục](./đề-mục.md)

[Về phần bài tập](./bài-tập.md)

# Mục lục

[Mở đầu](#mở-đầu)

[1. Chuẩn bị](#phần-1-chuẩn-bị)

[2. Setup môi trường]()

[3. Lưu ý]()




---
# Mở đầu
  Sau khi hoàn thành phần 1 và 2, lúc này, web app của chúng ta đã hoàn toàn có thể đảm bảo được chức năng hoạt động bình thường, tuy nhiên, nhiệm vụ của ``DevOps`` vẫn còn ở phía trước, đó chính là tạo cầu nối, mang quá trình ``commit`` phiên bản mới của application và ``deploy`` phiên bản đó lên môi trường ``production`` đến gần nhau hơn, tự động hóa quá trình đó. Hiện nay, có khá nhiều bộ tool có thể được sử dụng trong quá trình này, một trong số đó, khá nổi tiếng chính là ``Jenkins``. Kết hợp cùng ``Jenkins``, chúng ta còn các tool khác như ``Ansible``, ``Rundeck``, ``Spinaker``, ``GitHub Action``,... Tuy nhiên, để đơn giản hóa và để cho các bạn có 1 ``hand-ons`` lab dễ hiểu, mình sẽ chỉ sử dụng ``Jenkins`` và có chăng là thêm 1 chút ``Ansible`` cơn bản trong phần này.
  
  Phần này sẽ khá dài, do đó, các bạn hãy tập trung, ghi chép lại nếu cần và nếu có đóng góp, thắc mắc,... thì có thể contact với mình hoặc để lại comment trên GitHub issue nhé.

# Phần 1: Chuẩn bị
  Mình muốn chia phần này thành 2 mục nhỏ, đầu tiên là thiết lập và cấu hình ``SCM`` hay nôm na là tạo repository trên ``Git``. Các bạn có thể xài ``GitLab`` hoặc ``GitHub`` tùy theo độ thành thạo. Ờ guide này, mình sẽ tự host 1 con GitLab để lưu trữ source code của mình cũng như là các file manifest hay config của luồng CI-CD.
  

  Để các bài cài đặt được GitLab (bản community) và đảm bảo server của các bạn ít bị lag nhất có thể thì nên chọn máy ảo có cấu hình nhỏ nhất là 4GB RAM.

# Phần 2: Cài đặt môi trường chạy application
  Application này là một ứng dụng CRUD đơn giản, mình lấy từ nguồn này [Link](https://viblo.asia/p/xay-dung-ung-dung-web-crud-voi-python-va-flask-phan-mot-naQZRyydKvx)
  Các bạn có thể vào link này và làm theo hướng dẫn, trong quá trình làm nếu có khó khăn thì chỉ cần đọc guide này là được. Hiện source code của mình cũng gần như tương tự, chỉ khác 1 số phần như API healthcheck hay các API hỗ trợ đọc/ghi từ Redis cache.

  Còn nếu mọi người muốn tận dụng luôn source code của mình thì có thể dùng ``git clone`` như sau:

  ```sh
  git clone https://github.com/phungh67/devops-sample-application.git
  
  cd devops-sample-application

  python3 -m venv env

  ./env/bin/activate

  pip install -r requirements.txt
  ```

  Sau 1 chuỗi các câu lệnh trên, mọi người sẽ ``git clone`` y nguyên source code của mình về, sau đó tạo ra một ``venv`` và cài đặt các thư viện, package cần thiết để application chạy.
  Trong thư mục app, mọi người nhớ sửa file ``instance/config.py`` để truyền URI phục vụ cho việc connect với database nhé. nó sẽ có dạng như thế này:
  ```py
  mysql+pymysql://flask:App%402024@172.16.98.200:13306/flask_application
  ```

  Format của URI là ``<tên_user_chạy_app``:``<password>``@``<IP_của_Database>``:``<Port>``/``<tên_Database>``
  Kí tự ``@`` trong password sẽ bị conflict với kí tự ``@`` để tách user/password với IP của database nên mọi kí tự ``@`` nếu có trong password sẽ được thay bằng chuỗi ``%40``.

  Tuy nhiên, để chạy thử application, các bạn cần setup 2 biến môi trường đề ``Flask`` nhận diện cho đúng ``config`` và đúng file chạy app.

  ```sh
  export FLASK_CONFIG=development
  export FLASK_APP=run.py
  
  flask run
  ```

  Nếu như đã setup thành công và không có lỗi nào cả thì các bạn chỉ cần mở browser ra và gõ URL ``http://localhost:5000``, dashboard của app sẽ hiện ra.


# Phần 3: Một số lưu ý
  Có thể quá trình chạy app thuần trên server sẽ gặp khó khăn và có thể xuất hiện lỗi. Để tiện lợi hơi, các bạn có thể dùng ``Docker`` để chạy app.
  Trước khi chạy app ở dạng ``container``, các bạn cần build ``image``. Mình đã viết sẵn ``Dockerfile`` cho image, chỉ cần build và chạy thôi.

  ```sh
  sudo docker build -t sample-application .

  sudo docker run -d --name sample-app -p 5000:5000 -e "FLASK_CONFIG=development" -e "FLASK_APP=app.py" sample-application
  ```
 ``http://localhost:5000`` để kiểm tra.

  ---
  Sau khi application của chúng ta đã chạy thành công, bước tiếp theo là triển khai Redis cache để tăng performance của app và để đảm bảo đúng yêu cầu của đề bài.
  Redis xong xuôi thì sẽ đến phần dựng server Jenkins và viết ``Jenkinsfile`` phục vụ quá trình CI-CD.
  ---

  [Back to top](#mở-đầu)

  Phấn trước: [Database](./phần-1-database.md)

  Sau khi chạy thành công ``container``. cũng làm tuơng tự như trên, truy cập vào
  Phần tiếp theo: 