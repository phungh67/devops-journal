
# Thế nào là 1 database HA
  Như yêu cầu của đề bài, chúng ta cần 1 database cluster HA, vậy HA là  gì? HA chính là viết tắt của "High availability" tức là tính sẵn sàng cao, nghe thì có vẻ hơi mơ hồ, nhưng hãy hình dung đơn giản một case nhỏ như thế này nhé.

  Giả sử application của bạn phục vụ cho khác hàng không chỉ từ Việt Nam mà còn từ châu Âu, châu Mỹ chẳng hạn, vì thế lượng người dùng sẽ vô cùng lớn, tức là lượng request đọc, ghi vào database cũng không thể gọi là nhỏ được. Vậy, nếu một ngày đẹp trời, database của bạn lăn ra hẹo, thế chuyện gì sẽ xảy ra? Dĩ nhiên là ứng dụng không đáp ứng được nhu cầu của người dùng, feedback kém và đủ thứ khác kéo theo. Vậy để tránh case này, database của bạn phải có tính sẵn sàng, tức là khi có sự cố, lập tức 1 bản backup, 1 con database khác phải được đưa vào lấp chỗ trống ngay lập tức, càng giảm thời gian down (downtime) giữa lúc recovery và đưa con mới vào hoạt động thì hệ thống càng tốt. Và đó chính là tính High availability - sãn sàng cao, sẵn sàng đáp ứng nhu cầu người dùng và có thể back-to-serve trong 1 khoảng thời gian ngắn ngủi nếu xuất hiện tình trạng service down.

  Suy nghĩ đầu tiên, đơn giản nhất đó chính là tạo ra nhiều server database, 1 server có thể sập, nhưng nếu chúng ta tạo ra nhiều hơn 1, có thể là 2,3,5,... thì sẽ tăng khả năng chịu lỗi và tăng tính bền vững của server.

  Điều đó dẫn đến 1 trong những vấn đề tiếp theo, và có thể nói là muôn thuở của các DevOps engineer (hoặc đúng hơn là của các DBA - Database Administrator engineer): làm thế nào để đảm bảo dữ liệu giữa các server luôn đồng bộ và luôn giốn nhau?

  Điều đó dẫn đến một trong các task đơn giản, căn nguyên và cũng tốn nhiều công sức nhất: "Setup replication for Database cluster".

  Đúng vậy, phải có replication - sự sao lưu, đồng bộ dữ liệu giữa các server database với nhau thì chúng ta mới có thể đạt được tính HA. Tuy nhiên, phần đó mình sẽ viết ở một lúc khác, còn bây giờ, hãy đi vào cách thiết lập 1 database đơn giản cho bài tập của chúng ta.

# Thiết lập replication đơn giản
  Đúng như tên gọi, để đơn giản hóa hết mức có thể, mình sẽ chỉ đi vào với mô hình 1 master (hoặc gọi là controller, source,...) và 1 là replica.

  Trước tiên, có một số khái niệm, định nghĩa nhỏ cần biết, đó là replica và controller - source.

  **Controller** là database được coi là nguồn của dữ liệu, database này hành động như 1 người chỉ huy, chứa mọi dữ liệu và tiếp nhận các write request từ các user hoặc client. Tên chính xác của nó trong các cách gọi cũ là master.

  **Replica** là 1 bản copy hoàn toàn từ master, tức là, master có dữ liệu gì thì replica sẽ có y hệt như thế (có thể có ngày lập tức hoặc không, tùy theo cách các bạn setup).

  **Second-behind-master** đây là một thông số quan trọng trong việc thiết lập đồng bộ giữa các server database. Nó cho chúng ta giám sát được hiện tại, ở trên master, có bao nhiêu transactions mà relica chưa có. Tuy nhiên, thông số này không quá chính xác, sẽ có trường hợp, khi lượng dữ liệu lớn và số lệnh update trong 1 giây quá nhiều sẽ xảy ra trường hợp ``second-behind-master`` bằng 0 nhưng dataset trên 2 server không giống nhau. Vậy bản chất chỉ số này cho biết hiện tại, replica đã nhận được bao nhiêu dữ liệu từ master và đã apply thành công bao nhiêu phần so với lượng nhận được, chứ không phải là thực tế thua thiệt bao nhiêu so với master.
  

  Đó là những khái niệm cơ bản cần biết trước khi chúng ta thực hiện setup database, mình sẽ có 1 ghi chép chi tiết hơn về vấn đề này sau, còn chúng ta sẽ đi vào thực chiến trước.

  1. Chúng ta cài đặt MySQL theo guide trên mạng, mình khuyến khích xài guide này vì nó dễ hiểu: [Guide](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04).
  2. Sau khi cài đặt xong, bạn nên thiết lập lại MySQL của bạn như sau:
     ```conf
     [mysqld]
     log-bin                  = mysql-bin
     server-id                = 1
     port                     = 13306
     bind-address             = 0.0.0.0
     binlog-format            = row
     gtid_mode                = on
     enforce-gtid-consistency = on
     ```