# Đề mục
  Đây là phần đề mục cho repository của mình. Lí do để mình viết nên repo này chính là ghi chép lại các kiến thức về DevOps mình đã học được trong quá trình 
  đi làm cũng như thực tập, phỏng vấn, thử việc, những lần tham gia thi thử v...v... 

  Vì đây chỉ là ghi chép của 1 cá nhân cũng như từ 1 người có thể được coi là ngoài ngành CNTT (mình có gốc là điện tử viễn thông) nên có thể 1 số kiến thức    
  còn sai sót hoặc chưa chính xác, rất mong mọi người có góp ý để mình có thể xây dựng repo này chi tiết và chính xác hơn.

  Mục tiêu của mình có thể còn xa hơn nữa khi mong muốn từ repo này, các bạn fresher, sinh viên mới ra trường yêu thích con đường trở thành một Cloud Ops hoặc
  một DevOps engineer có thể có những phần tham khảo chất lượng, dễ hiểu để tốn ít thời gian hơn trong việc xây dựng và hệ thống kiến thức.

  Chúc các bạn thành công trên con đường mình đã chọn.

# Mục lục

1. [Quay về đầu trang](#đề-mục)
2. [Cấu trúc của repository](#cấu-trúc-repository)

# Cấu trúc repository
  Repository này đơn giản chỉ là nơi lưu trữ các documents dạng markdown (MD) và 1 số sơ đồ hình vẽ nhằm minh hoạ cho các bài tập, dự án mà mình có tham gia thực hành, nó có tên là [DevOps Journal](https://github.com/phungh67/devops-journal), ngoài ra, mình có chia nhỏ repository của mình ra cho tiện theo dõi như sau:

  - Đầu tiên là phần repository về database. Mình ghi chép ở đây những gì mình học được về "HA cho database" hoặc là các lý thuyết về việc thiết lập **replication** cho CSDL. Trong này mình để các config cũng như các guide đơn giản để dựng mô hình lab cụm CSDL. Truy cập repo: [DevOps database](https://github.com/phungh67/devops-database) để biết thêm chi tiết nhé.

  - Tiếp theo là phần CI-CD, do trước đây mình làm nhiều với GitHub Action và Code Family của AWS nên mình chủ yếu là follow theo các check list hoặc guide từ senior/PM của dự án đổ xuống. Lần thực tập hiện tại giúp mình có thêm một chút kinh nghiệm về việc viết Jenkinsfile cho quá trình CI-CD. Hiện giờ thì mình chưa có thời gian viết kĩ về nó, nhưng chắc chắn sẽ làm vì đây là phần khá quan trọng trong DevOps mà, gần như là linh hồn vậy [DevOps-CD/CD]() (Link chưa khả dụng đâu nhé).

  - Tiếp theo là phần IAC của mình. Làm DevOps đôi khi sẽ phải đi setup các hạ tầng, cài cắm các tools lên một số lượng lớn các servers, nhỏ thì dưới 10 còn lớn thì có khi cả nghìn cái. Vì vậy nên phần IAC khá hay, nó giúp chúng ta tiết kiệm thời gian. Trước mắt, trong repository về IAC, mình sẽ để một vài code terraform để tạo 1 vài hạ tầng đơn giản trên AWS, 1 số module mình đang thử tự viết và một số playbook dành cho Ansible. [DevOps IAC](https://github.com/phungh67/devops-IaC).

  - Cuối cùng là repository để chứa code cho một web application đơn giản của mình. Đây là phần dummy test để mình tập deploy, xây dựng một luồng deploy app hoàn chỉnh. Lý thuyết của phần này sẽ được ghi trong Repository này.

  - Các phần thêm trong tương lai của mình có thể là các Dockefile cho việc build images (bé, nhẹ và đảm bảo best practice cho security chẳng hạn) hoặc là các config, các phép tính cho việc setup monitoring hoặc alerting.


