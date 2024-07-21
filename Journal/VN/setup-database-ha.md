
# Thế nào là 1 database HA
  Như yêu cầu của đề bài, chúng ta cần 1 database cluster HA, vậy HA là  gì? HA chính là viết tắt của "High availability" tức là tính sẵn sàng cao, nghe thì có vẻ hơi mơ hồ, nhưng hãy hình dung đơn giản một case nhỏ như thế này nhé.

  Giả sử application của bạn phục vụ cho khác hàng không chỉ từ Việt Nam mà còn từ châu Âu, châu Mỹ chẳng hạn, vì thế lượng người dùng sẽ vô cùng lớn, tức là lượng request đọc, ghi vào database cũng không thể gọi là nhỏ được. Vậy, nếu một ngày đẹp trời, database của bạn lăn ra hẹo, thế chuyện gì sẽ xảy ra? Dĩ nhiên là ứng dụng không đáp ứng được nhu cầu của người dùng, feedback kém và đủ thứ khác kéo theo. Vậy để tránh case này, database của bạn phải có tính sẵn sàng, tức là khi có sự cố, lập tức 1 bản backup, 1 con database khác phải được đưa vào lấp chỗ trống ngay lập tức, càng giảm thời gian down (downtime) giữa lúc recovery và đưa con mới vào hoạt động thì hệ thống càng tốt. Và đó chính là tính High availability - sãn sàng cao, sẵn sàng đáp ứng nhu cầu người dùng và có thể back-to-serve trong 1 khoảng thời gian ngắn ngủi nếu xuất hiện tình trạng service down.

  