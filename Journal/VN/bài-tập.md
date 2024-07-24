[Quay về phần dẫn](./đề-mục.md)

---
# Mục lục
---




---
# 1. Phân tích đề tài
  Về đề tài, các bạn đã nắm được đề bài rồi, vậy để đơn giản và đỡ dài dòng, mình xin được tóm tắt những điểm cần cần phân tích của từng block như sau (mình chia thành các block - task) cho đơn giản ha:
  - CRUD application: Cái này thì về source code có rất nhiều trên các trang mạng của cả viblo hoặc các page khác như medium, digitalocean,... điều mình cần thêm vào là ``caching`` và ``healthcheck``. Vì đây là một ứng dụng đơn giản, chúng ta sẽ bỏ qua (tạm) các khái niệm kiểu ``session caching`` cho đỡ phức tạp, thì vai trò của ``cache`` ở đây chỉ đơn giản là lưu kết quả của các câu query từ database thôi, như thế này này:
  ![caching-mechanism](../../Figures/caching-workflow.png)
  Còn healthcheck thì tùy mọi người triển khai, có thể từ những healthcheck đơn giản xem service sống hay chết cho đến các case phức tạp như monitor từng sites của application.

  - Về database, để đảm bảo yêu cầu HA, chúng ta cần một số khái niệm cũng như hiểu biết trước, cái này mình sẽ có bài viết dẫn link chi tiết nhé. Còn hiện giờ, các bạn sẽ chỉ cần hiểu yêu cầu đại ý là: một cụm database để làm sao khi nhỡ ra có sự cố thì app của chúng ta không chết, tiếp tục hoạt động  và vẫn đáp ứng nhu cầu truy cập dữ liệu. Tương tự như thế với cụm cache.

  - Về phần CI/CD, để thỏa mãn yêu cầu của phần này, chúng ta cần những stack đơn giản, nhưng phổ biến trong DevOps, như mình sẽ dùng Jenkins + Ansible và ArgoCD. ``Ansible`` sẽ giúp mình deploy lên môi trường test đơn giản, còn ``ArgoCD`` giúp mình deploy ứng dụng lên môi trường "production" với các deployment, các daemonset,...

  - Phần monitoring và logging thì đơn giản hơn, chúng ta dùng stack ELK và Prometheus + Grafana là xong thôi.

# 2. Lựa chọn các toolchain cho đề tài
  Sau khi phân tích xong, mình sẽ đi đến chốt các tool chain, sắp xếp các luồng để chúng ta tạo nên ứng dụng. Các bạn có thể sử dụng như 1 bộ khung nếu muốn customized hoặc là follow theo để hiểu trước cũng được á.

  - Application: mình chọn Python và Flask cho đơn giản, và mình dự sẽ dùng container để triển khai lên môi trường test, production thì mình sẽ xây cụm kubernetes bằng ``kubeadm``. 
  - Database mình sẽ chọn ``MySQL`` với ``Galera`` để config cluster, mình cũng sẽ hướng dẫn qua cách config bằng tay nữa, tuy nhiên production thì không khuyến khích lắm nha. Cache thì mình chọn ``Redis``.
  - Luồng CI/CD như đã nói ở trên, ``Jenkins`` sẽ là ngôi sao chính của mình, bên cạnh đó còn ``Ansible`` và ``ArgoCD`` nữa.
  - Stack logging thì mình chọn agent là ``filebeat`` còn bộ xử lý - lưu trữ - thể hiện thì là ``ELK``.
  - Monitoring dùng ``Prometheus`` và ``Grafana`` kết hợp với ``AlertManager`` và ``Telegram`` để tạo 1 con bot chuyên cảnh báo. Đúng vậy, chúng ta sẽ tạo 1 con bot đơn giản cho việc này.

# 3. Bắt tay vào làm thôi

  Hướng dẫn chi tiết của từng phần được cập nhập ở [đây](./đề-mục.md)