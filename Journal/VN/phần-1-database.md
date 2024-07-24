[Về đầu trang](../../README.md)
[Về đề mục](./đề-mục.md)
[Về phần bài tập](./bài-tập.md)

# Mục lục
[Mở đầu](#mở-đầu)
[1. Chuẩn bị](#phần-1-chuẩn-bị)
[2. Setup và Config](#phần-2-cài-đặt-và-setup-mysql-server-trên-linux)
[3. Phân quyền user](#3-user-cho-việc-tạo-replica)




---
# Mở đầu
  Đề cho ứng dụng của chúng ta hoạt động đúng như mong muốn, một database dành cho việc lưu trữ các dữ liệu là việc cần thiết. Phần này sẽ hướng dẫn chi tiết cách thiết lập 1 database với mô hình master-slave đơn giản dể đảm bảo tính HA cho CSDL.
  Trong phần này, các kiến thức cơ bản về Linux và MySQL là cần thiết để hiểu kĩ hơn các bước hướng dẫn.

# Phần 1: Chuẩn bị
  - Một server Linux để chạy database, tối thiếu 1GB RAM và có 1 CPU.
  - Mở firewall của Port ``13306``.

# Phần 2: Cài đặt và setup MySQL Server trên Linux
  Đầu tiên chúng ta sẽ cài đặt MySQL thông qua ``apt`` package magement của Linux.
  ```sh
  sudo apt update
  sudo apt install -y mysql
  ```
  Sau khi chạy 2 câu lệnh trên, MySQL sẽ được cài đặt vào máy. Tuy nhiên, cần 1 số bước cấu hình để đảm bảo server của chúng ta hoạt động như 1 database thực thụ.

  Setup để MySQL luôn khởi động cùng với hệ điều hành (để nếu trong quá trình chạy, server nếu có bị reboot thì MySQL sẽ luôn được start lại mà không cần phải bật thủ công)
  ```sh
  sudo systemctl enable mysql
  sudo systemctl start mysql
  ```
  Lúc này, các bạn có thể kiểm tra trạng thái của MySQL bằng cách dùng ``service`` hoặc ``systemctl``
  ```sh
  sudo service mysql status
  sudo systemctl status mysql
  ```
  Nếu ``mysql`` đang running thì cả 2 câu lệnh sẽ cho về cùng 1 kết quả như nhau, trạng thái sẽ là ``running``.

  Hiện tại ``mysql`` đã chạy, tuy nhiên chúng ta cần ``login`` và bắt đầu tạo các user ban đầu, do khi tạo ra thì CSDL chỉ có duy nhất một user là ``root``, có toàn quyền và đây là điều không nên. Vì vậy, chúng ta sẽ tạo ra một user mới cũng như thiết lập thêm 1 số biện pháp bảo mật cần thiết cho database của chúng ta.

  ```sh
  sudo mysql
  ```

  ```sql
  ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
  ```

  Sau command này, chúng ta có thể login vào ``mysql`` bằng account tên là ``root`` với mật khẩu là ``password``:
  ```sh
  mysql -u root -p
  ```

  Giờ thì database của chúng ta đã đi vào hoạt động, tuy nhiên, nếu các bạn dùng 1 trong số các command để kiểm tra, sẽ chỉ thấy port ``3306`` - port mặc định của ``mysql`` được gắn vào network ``localhost`` hoặc ``127.0.0.1``. Điều đó có nghĩa là, hiện, tại, mọi truy cập đến database đều phải bắt nguồn từ server này, từ các server khác sẽ đều không truy cập được, mà điều đó khá là bất tiện khi web application của chúng ta sẽ triển khai trên 1 server khác còn dataabase sẽ được cài đặt ở các server khác.

  Vậy lúc này chính là lúc sửa file config của ``mysql`` đi một chút cho phù hợp.
  Mọi người tìm đến đường dẫn sau ``/etc/mysql/my.cnf`` và sửa để cho file có nội dung như sau:
  ```cnf
   [mysqld]
    log-bin                         = mysql-bin
    server-id                       = 1
    port                            = 13306
    bind-address                    = 0.0.0.0
    binlog-format                   = row
    gtid_mode                       = on
    enforce-gtid-consistency        = on
  ```

  Trong những config trên, có 1 số config hiện tại mình sẽ chưa giải thích để tránh nhiều thông tin quá, tuy nhiên có 1 số thông số mà mọi người nên nhớ:
  - ``server-id``: là ID của server database, sau này khi dùng nhiều server chạy database cùng 1 lúc, chúng ta nên đặt id khác nhau để tránh xung đột dữ liệu.
  - ``port``: là cổng mặc định mà ``mysql`` sẽ chấp nhận các connection từ client đến. Mặc định sẽ là ``3306`` tuy nhiên mình sẽ đổi thành ``13306`` do best practice là không nên để port mặc định để tránh port-scanning attack và để sau này mình sẽ host một con load balancer trên port đó (mình sẽ nói chi tiết sau).
  - ``bind-address``: chính xác là địa chỉ IP mà ``mysql`` sẽ host trên đó, bình thường nếu để là ``localhost`` thì ``mysql`` sẽ bind vào loopback interface, trong case này, để cho các server khác có thể gọi đến được, mình sẽ để nó bind vào địa chỉ public IP hoặc đơn giản thì mọi người cứ để ``0.0.0.0`` tức là ``mysql`` sẽ bind với mọi network interface tồn tại trên máy.
  
  Sau khi config xong, chúng ta cần restart lại để ``mysql`` nhận config mới.
  ```sh
  sudo service mysql restart
  ```
  Các bạn có thể dùng ``systemctl`` còn do mình quen ``service`` hơn nên các guide của mình sẽ hầu như dùng ``service`` nhé.

# Phần 3: Tạo các users cần thiết và database cho application
  Chúng ta sẽ có 1 database cần thiết cho việc chạy application.
  Ngoài ra, để đảm bảo best security: "Chỉ cấp quyền ít nhất và vừa đủ cho mỗi user theo tiêu chí least privileges", chúng ta sẽ tạo các user khác nhau dành cho các việc khác nhau từ việc cho phép client gọi connection đến database, quản trị (DBA), replica_user cho việc sao lưu dữ liệu giữa các server với nhau ...
  Kết luận, chúng ta sẽ có 1 database là:
  - flask_application dành cho việc lưu trữ dữ liệu của app.
  
  Chúng ta sẽ có ít nhất 3 user là:
  - administrator: dành cho việc quản trị database, chúng ta sẽ không dùng ``root`` vì lí do bảo mật.
  - flask: dành cho việc chạy application, đây là user mà application sẽ dùng để kết nối đến database.
  - replica_user: dành cho quá trình replica dữ liệu giữa master và slave.
  
  ### 1. User và database cho việc chạy app.

  Tạo database cho việc chạy app rất đơn giản, do framework của Python sẽ xử lý hết phần tạo bảng, setup primary key,... nên chúng ta chỉ cần tạo sẵn database và user để đó thôi.

  ```sql
    CREATE USER 'flask'@'%' IDENTIFIED BY 'flask_application@2204';
	CREATE DATABASE flask_application;
	GRANT ALL PRIVILEGES ON flask_application . * TO 'flask'@'%';
  ```

  Trong khối lệnh ở phía trên ``%`` kí hiệu rằng tài khoản ``flask`` có thể truy cập database từ bất kì địa chỉ IP nào, kí tự ``%`` giống như kí tự wildcard ``*`` trong xử lý xâu kí tự vậy. Để giới hạn hơn, chúng ta có thể dùng dải IP, như trong bài lab của mình, mình đã sử dụng giải IP là ``172.16.%.%``.
  Account ``flask`` sẽ có toàn quyền trong database ``flask_application``, đảm bảo nó không vượt quá quyền hạn hoặc nếu app của chúng ta bị chiếm quyền thì phần nào đó CSDL sẽ được bảo vệ.

  ### 2. User cho việc quản trị

  User này sẽ có đầy đủ các quyền như ``root``, tuy nhiên chúng ta sẽ thêm 1 số policy cho nó, ví dụ như password sẽ hết hạn sau 90 ngày,...

  ```sql
  create user 'administartor'@'%' identified by 'adminpassword@2024';
  grant all privileges on *.* to 'administrator'@'%';
  alter user 'administrator'@'%' password expire interval 90 day;
  ```

  User này sẽ có đầy đủ quyền trên mọi tables thuộc mọi databases và có password bị ràng buộc (90 ngày đổi 1 lần).

  ### 3. User cho việc tạo replica

  User này sẽ được slave dùng để truy cập và lấy binlog từ master, phục vụ cho quá trình replica dữ liệu.

  ```sql
    CREATE USER 'repl'@'%' IDENTIFIED BY 'password';
    GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
  ```

  Có một điểm đặc biệt là thông tin về user cũng như password của quá trình replica này sẽ được lưu dưới dạng plain text không mã hóa, hoàn toàn có thể đọc được dễ dàng, vì vậy, câu lệnh ``grant replication slave`` là 1 cách để giới hạn quyền của user này lại, chỉ gói gọn trong đọc binlog. Các bạn có thể check thêm ở document chính thức trên page của ``mysql``.

  ---
  Sau tất cả các bước trên thì giờ đây database của chúng ta đã đi vào hoạt động, mọi người nên note lại IP của server cài đặt database, vì khi viết app, URI string cho việc kết nối với database sẽ có dạng: ``<IP_Database_server>:<Port>:<User>:<Password>``

  ---

  [Back to top](#mở-đầu)
  Phần tiếp theo: [Application](./phần-2-application.md)