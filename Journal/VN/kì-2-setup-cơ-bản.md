[Kì trước: Sơ lược về dự án](./kì-1-đề-tài.md)

# Kì 2 - Setup cơ bản môi trường chạy application và database

### **Mục lục**

[1. Tạo môi trường cho ứng dụng](#1-setup-môi-trường-chạy-application)

[2. Chạy thử application ở chế độ "vô hại"](#2-chuẩn-bị-hạ-tầng)

[3. Nối ứng dụng với 1 database](#3-cài-đặt-và-cấu-hình-database)

[4. Chúng ta làm gì ở kì tiếp](#4-kết)


---

## 1. Setup môi trường chạy application

Trong Pet "project" này, chúng ta sẽ sử dụng ngôn ngữ ``Python`` và một framework khá phổ biến đó là ``Flask`` để tạo một ``CRUD`` web-application đơn giản. Cho bạn nào quên hoặc chưa rõ khái niệm ``CRUD`` là gì thì đó là những chữ cái đầu của những ``method`` mà ứng dụng đó cần đáp ứng được là ``Create``, ``Read``, ``Update`` và ``Delete``.

Mình không phải là một developer chuyên nghiệp cũng như chỉ được đào tạo sơ qua về phần mềm và chuyên môn thì cũng không phải Dev, nên trong hoàn cảnh như thế này, nhanh nhất là đi luộc 1 một source code nào đó rồi biến tấu thành của mình là được :D.

Tuy nhiên, để cho project này giống với các product nhất có thể chúng ta sẽ thêm 2 API nhỏ nữa vào đó là:
    - ``/healthcheck`` đây là API sẽ trả về code ``200`` nếu được gọi là khi gọi vào không nhận được ``200`` thì tức là app của chúng ta đã hẹo.
    - API ghi vào ``redis``. Hầu như các ứng dụng production đều có một API để lưu kết quả các câu query vào cache để sau này nếu cần gọi đến thì chỉ cần vào cache lấy kết quả chứ không cần truy cập trực tiếp database.

Trong bài này, mình sẽ đi nhanh qua việc tạo app, chạy app và tạo một database nhỏ; mục tiêu là đến cuối bài, mọi người dựng được application lên là được.

## 2. Chuẩn bị hạ tầng

Tất nhiên là để chạy được application, chúng ta cần tối thiểu một server để host ``Python Flask``. Không cần quá mạnh, trong trường hợp này, mình khuyến khích dùng 1 server ảo trên ``Oracle Virtual Box``, tầm ``1vCPU + 2GB RAM`` là đủ.

Tuy nhiên, như đã đề cập ở trên, chúng ta còn setup database nữa nên là nếu có thể thì mọi người nên nâng cấu hình máy ảo lên ``2vCPU + 4GB RAM`` thì sẽ ổn hơn

Đầu tiên chúng ta sẽ đi clone repository chứa application [ở đây](https://github.com/phungh67/devops-sample-application)

Tuy nhiên, để hiểu rõ ràng hơn về app và có cái nhìn tốt hơn khi triển khai API ``/healthcheck`` cũng như thiết lập ``redis`` cho app thì mình khuyển khích mọi người đọc thêm [ở đây](https://viblo.asia/p/xay-dung-ung-dung-web-crud-voi-python-va-flask-phan-mot-naQZRyydKvx)

Trong phần về app, mình có nói qua về cách chạy, tuy nhiên, cho tiện mình sẽ nói lại qua việc chạy app. Chúng ta những bước cở bản sau (lưu ý, mình chạy trên hệ điều hành ``Linux`` nhé):
- Cài đặt ``python3``, ``pip3`` và ``python-venv``. Lí do thì đơn giản, ``pip`` là một ``package manage`` của riêng ``python`` còn ``venv`` là cho một môi trường cô lập để chạy app, thỏa thích cài mà không sợ ảnh hưởng đến hệ thống chính.
- Clone repository về máy.
- Tạo ra một ``venv`` mới với câu lệnh:
    
```bash
    python3.8 -m venv env
    env/bin/active
```
- Cài đặt các ``package`` cần thiết:
```bash
    pip install -r requirements.txt
```
- Tạo thư mục có tên là ``instance`` trong ``dir`` mà bạn mới clone về, sau đó thêm những dòng này vào file ``instance/config.py``:
```bash
# instance/config.py

SECRET_KEY = 'abc' # input some secret here
SQLALCHEMY_DATABASE_URI = 'lib:user:pass:IP:port:database' # input the connection URI for database
```
- Set biến môi trường trước khi chạy app:
```bash
export FLAKS_CONFIG=development
export FLASK_APP=run.py
```
- Chạy thử app thôi:
```bash
flask run
```

Lúc này khi bạn truy cập vào địa chỉ ``localhost:3000`` thì bạn sẽ web application đã chạy, tuy nhiên, đừng dại mà làm gì cả, vì sẽ lỗi ngay. Lý do là gì? Là chưa có database. Vì thế, chúng ta sẽ đi cài đặt database ngay bây giờ để hoàn thiện ``demo``.

## 3. Cài đặt và cấu hình database

Để cho bất cứ một ứng dụng nào chạy một cách bình thường, chúng ta đều không thể thiếu phần ``database``, vì đơn giản, trừ những phần mềm theo kiểu ``tool`` hay là ``hello-world`` thì cơ sở dữ liệu luôn cần để quản lý, sắp xếp các dữ liệu phục vụ cho việc chạy app.

Ở kì này hay đúng hơn là vài kì đầu, mình chủ yếu tập trung vào việc chạy được app đã, sẽ tạm thời bỏ qua vài khái niệm hay ho như ``fail-over`` hay là ``high availability``, mấy cái này mình sẽ cố gắng viết ở kì tiếp.

Tạm thời chạy đã nhé. Mình cũng chia task này thành nhiều bước:
- Đầu tiên, cài MySQL, tất nhiên rồi, mình sẽ không đi cụ thể, vì lằng ngoằng lắm, nên các bạn sẽ theo guide ở [đây nhé](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04). Nhớ làm theo các bước, đặc biệt là phần  ``secure-install`` vì phần đó sẽ rất quan trọng trong môi trường ``prod``.
- Sau khi cài xong, chúng ta sẽ sửa đổi config một chút xíu. Những sửa đổi trong này để nhằm các mục đích sau:
  - Tuân thủ **best-practice** để bảo mật hạ tầng nhiều lớp nhất có thể.
  - Làm quen với những ``concept`` của môi trường thực tế.
  - Tiện setup - nâng cấp dự án sau này.
  Đây là file config mà các bạn cần sửa: ``/etc/mysql/my.cnf``. Khi chạy thì ``mysql`` nó sẽ đọc các file config có trong đường dẫn ``/etc/mysql/conf/`` và file ``my.cnf`` và file này có thứ tự ưu tiên cao hơn, nên chỉ cần sửa ở file này là được.
  ```bash
  [mysqld]
    server-id               = 1                       # indentical for server ID
    log-bin                 = "mysql-bin"             # bin log prefix
    relay-log               = "mysql-relay-log"       # relay log for replication
    bind-address            = 0.0.0.0                 # bin port, because MySQL bind to localhost by default
    port                    = 13306                   # change listening port to 13306
  ```
  Mình sẽ giải thích kĩ càng khi đi đến những phần sau, còn ở bước này thì cứ copy paste đã.
  - Sau khi xong thì nhớ ``restart`` lại để ``MySQL`` nhận config mới:
  ```bash
  sudo service mysql restart
  ```

- Lúc này, các bạn có thể quay lại phần [setup application](#2-chuẩn-bị-hạ-tầng) để chạy các task migration cho database các kiểu, sau đó restart lại app là được. Nhớ rằng, ở ``connection_string`` trong file ``instance/config.py`` thì ``database_ip`` sẽ thay bằng ``localhost``, ``port``, ``username`` và ``password`` sẽ thay bằng ``password`` do chính bạn đặt, ``port`` thì ở file config. Chắc sẽ khó hiểu nhưng mà tìm tòi là một phẩm chất mà ``DevOps`` nên có :D
- Xong xuôi thì reload lại ứng dụng và hưởng thành quả thôi.

## 4. Kết

Ở phần này, chúng ta chưa đi sâu vào những gì mà các bạn sẽ làm khi là một ``DevOps`` engineer, hay là một ``SystemAdmin`` cả, nhưng đừng lo, ngay kì sau chúng ta sẽ bắt đầu học và làm quen với những task đầu tiên (mà mình được giao trong hành trình làm ``DevOps`` cuả mình): setup một cụm database HA.

Trong phần đó, ngoài việc hướng dẫn các bạn setup, mình sẽ nói qua những mô hình hay được sử dụng nhất, use case và những gì mình được các senior chia sẻ.

Sau đó thì chúng ta sẽ test thử trên pet project này luôn.

Keyword của kì sau: ``Load Balancer``, ``HAProxy``, ``Keepalived`` và ``Master-slave``


[Quay về đầu trang](#kì-2---setup-cơ-bản-môi-trường-chạy-application-và-database)

[Quay về kì trước](kì-2-setup-cơ-bản.md)