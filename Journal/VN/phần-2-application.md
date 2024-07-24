[Về đầu trang](../../README.md)

[Về đề mục](./đề-mục.md)

[Về phần bài tập](./bài-tập.md)

# Mục lục

[Mở đầu](#mở-đầu)

[1. Chuẩn bị](#phần-1-chuẩn-bị)

[2. Setup môi trường](#phần-2-cài-đặt-môi-trường-chạy-application)

[3. Lưu ý](#phần-3-một-số-lưu-ý)




---
# Mở đầu
  Ở phần trước, chúng ta đã thiết lập xong database và setup những user cần thiết tùy theo mục đích sử dụng, ở phần này, chúng ta sẽ viết một web application đơn giản để tiến thêm 1 bước trong việc hoàn thiện dự án nhé.

# Phần 1: Chuẩn bị
  Application sẽ được viết bằng Python, vậy nên việc cài đặt trước ``python3`` là cần thiết, với các phiên bản Ubuntu mới gần đây như ``22.04`` và ``24.04`` thì ``python3`` đã được cài sẵn, nên các bạn có thể skip qua bước này.

  Cài đặt Python và Virtual Environment cho việc chạy app:
  ```sh
  sudo apt install -y python3-pip
  sudo pip3 install virtualenv
  ```

  Lệnh trên giúp ta cài đặt ``pip``, một package management riêng của ``python``, sau này ta sẽ dùng ``pip`` để cài đặt các thư viện cũng như framework của application.
  ``virtualenv`` chính là tên gói của ``python3-venv``, giúp chúng ta tạo 1 môi trường ảo, nôm na gần giống như virtual box để chúng ta có thể thoải mái cài đặt các thư viện, setup các biến môi trường mà không lo ảnh hưởng đến server của chúng ta.

  Sau khi đã cài đặt xong các gói, chúng ta sẽ tạo một ``venv`` bằng câu lệnh:

  ```sh
  python3 -m venv env
  ```

  Câu lệnh trên tạo 1 môi trường ảo với tên là ``env``.
  Để truy cập/ activate môi trường đó, chúng ta dùng command:

  ```sh
  ./env/bin/activate
  ```

  Nếu muốn thoát thì chỉ cần dùng command:

  ```sh
  deactivate
  ```

  Dĩ nhiên để application có thể chạy trơn tru thì các bạn cần setup database xong xuôi và trơn tru như ở phần hướng dẫn [này](./phần-1-database.md)

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

  Sau khi chạy thành công ``container``. cũng làm tuơng tự như trên, truy cập vào ``http://localhost:5000`` để kiểm tra.

  ---
  Sau khi application của chúng ta đã chạy thành công, bước tiếp theo là triển khai Redis cache để tăng performance của app và để đảm bảo đúng yêu cầu của đề bài.
  Redis xong xuôi thì sẽ đến phần dựng server Jenkins và viết ``Jenkinsfile`` phục vụ quá trình CI-CD.
  ---

  [Back to top](#mở-đầu)

  Phấn trước: [Database](./phần-1-database.md)

  Phần tiếp theo: 