[Về đầu trang](../../README.md)
# Đề mục
  Đây là phần đề mục cho repository của mình. Lí do để mình viết nên repo này chính là ghi chép lại các kiến thức về DevOps mình đã học được trong quá trình 
  đi làm cũng như thực tập, phỏng vấn, thử việc, những lần tham gia thi thử v...v... 

  Vì đây chỉ là ghi chép của 1 cá nhân cũng như từ 1 người có thể được coi là ngoài ngành CNTT (mình có gốc là điện tử viễn thông) nên có thể 1 số kiến thức    
  còn sai sót hoặc chưa chính xác, rất mong mọi người có góp ý để mình có thể xây dựng repo này chi tiết và chính xác hơn.

  Mục tiêu của mình có thể còn xa hơn nữa khi mong muốn từ repo này, các bạn fresher, sinh viên mới ra trường yêu thích con đường trở thành một Cloud Ops hoặc
  một DevOps engineer có thể có những phần tham khảo chất lượng, dễ hiểu để tốn ít thời gian hơn trong việc xây dựng và hệ thống kiến thức.

  Chúc các bạn thành công trên con đường mình đã chọn.

# Mục lục

- [Đề mục](#đề-mục)
- [Mục lục](#mục-lục)
- [Cấu trúc repository](#cấu-trúc-repository)
- [Bài tập vận dụng](#bài-tập-vận-dụng)

# Cấu trúc repository
  Repository này đơn giản chỉ là nơi lưu trữ các documents dạng markdown (MD) và 1 số sơ đồ hình vẽ nhằm minh hoạ cho các bài tập, dự án mà mình có tham gia thực hành, nó có tên là [DevOps Journal](https://github.com/phungh67/devops-journal), ngoài ra, mình có chia nhỏ repository của mình ra cho tiện theo dõi như sau:

  - Đầu tiên là phần repository về database. Mình ghi chép ở đây những gì mình học được về "HA cho database" hoặc là các lý thuyết về việc thiết lập **replication** cho CSDL. Trong này mình để các config cũng như các guide đơn giản để dựng mô hình lab cụm CSDL. Truy cập repo: [DevOps database](https://github.com/phungh67/devops-database) để biết thêm chi tiết nhé.

  - Tiếp theo là phần CI-CD, do trước đây mình làm nhiều với GitHub Action và Code Family của AWS nên mình chủ yếu là follow theo các check list hoặc guide từ senior/PM của dự án đổ xuống. Lần thực tập hiện tại giúp mình có thêm một chút kinh nghiệm về việc viết Jenkinsfile cho quá trình CI-CD. Hiện giờ thì mình chưa có thời gian viết kĩ về nó, nhưng chắc chắn sẽ làm vì đây là phần khá quan trọng trong DevOps mà, gần như là linh hồn vậy [DevOps-CD/CD]() (Link chưa khả dụng đâu nhé).

  - Tiếp theo là phần IAC của mình. Làm DevOps đôi khi sẽ phải đi setup các hạ tầng, cài cắm các tools lên một số lượng lớn các servers, nhỏ thì dưới 10 còn lớn thì có khi cả nghìn cái. Vì vậy nên phần IAC khá hay, nó giúp chúng ta tiết kiệm thời gian. Trước mắt, trong repository về IAC, mình sẽ để một vài code terraform để tạo 1 vài hạ tầng đơn giản trên AWS, 1 số module mình đang thử tự viết và một số playbook dành cho Ansible. [DevOps IAC](https://github.com/phungh67/devops-IaC).

  - Cuối cùng là repository để chứa code cho một web application đơn giản của mình. Đây là phần dummy test để mình tập deploy, xây dựng một luồng deploy app hoàn chỉnh. Lý thuyết của phần này sẽ được ghi trong Repository này.

  - Các phần thêm trong tương lai của mình có thể là các Dockefile cho việc build images (bé, nhẹ và đảm bảo best practice cho security chẳng hạn) hoặc là các config, các phép tính cho việc setup monitoring hoặc alerting.

# Bài tập vận dụng
  Hầu như tất cả các hành trình học của mình đều theo phương pháp try-error-repeat, tức là mình sẽ đọc lý thuyết, sau đó tìm một đề bài tốt (hoặc tự bịa ra 1 đề bài dựa trên 1 khung nào đó có sẵn) để có thể vận dụng được những khái niệm, phương pháp mà mình đã học.

  Bài tập này mình được hướng dẫn và thực hành trong thời gian thử việc của mình. Mình sẽ chia đề tài đó thành các mức như sau, các bạn cứ thoải mái chọn mức độ của bản thân. Mình không đảm bảo có thể tạo ra một đề bài hoàn toàn như các bạn mong muốn, tuy nhiên, đây sẽ là gốc rễ để chúng ta đào sâu thành từng phần kiến thức và có được cái nhìn chung về nghề "DevOps" hoặc đúng hơn là các công việc thường ngày của 1 kĩ sư DevOps (như các công ty hay tuyển, nhưng mình nghĩ cụm từ SysOps hoặc CloudOps sẽ sát hơn)

  1. Triển khai bài tập trên 1 máy chủ duy nhất (single server): Mọi stack từ application, database, logging, monitoring, CI/CD, repository sẽ đều được lưu trữ và cài đặt trên một server duy nhất. Các này sẽ mang lại cho các bạn những lợi ích sau:
      - Dễ setup: Do tất cả các stack và các thành phần đều nằm chung 1 máy chủ, bạn chẳng phải lo gì về mangj, firewall hay connection giữa chúng, dễ dàng cài đặt, lên 1 stack là lên cả bài tập.
      - Yêu cầu tài nguyên đơn giản: Bạn chỉ cần 1 máy chủ đủ khỏe, tầm 8-12GB RAM là ổn, hầu như các  tài nguyên đều chạy ở dạng daemon của Linux nên sẽ không cần quá nhiều sức mạnh phần cứng như trong môi trường production thực tế.
      - Dễ quản lý: Dĩ nhiên rồi, việc quản lý chỉ 1 và 1 máy chủ duy nhất sẽ đơn giản hơn việc bạn phải điều khiển, quản lý và giám sát 1 hệ máy chủ.
  
  2. Triển khai hạ tầng trên nhiều máy chủ khác nhau, có chia vai trò tùy theo software stack cài đặt trên đó. Các làm này là 1 dạng mang môi trường production đến gần với các bạn hơn, vì vậy, ngoài các bài toàn về thiết lập, cài đặt các bạn còn phải làm quen về bài toán quản trị, một trong những thứ rất đau dầu của nghề Operation.
  
  3. Triển khai nhiều hạ tầng trên Cloud Provider. Đây là mức cuối, gần thực sự với những hạ tầng tại các công ty hoặc các doanh nghiệp lớn. Hầu hết bây giờ các service của họ đều chạy song song cả trên hạ tầng vật lý (mục 2) và hạ tầng đám mây. Tuy nhiên, vì chúng ta làm lab thử nghiệm, việc cài cắm và thiết lập connection giữa hạ tầng đám mây và hạ tầng vật lý thực sự sẽ tốn kém chúng ta khá nhiều nên mình khuyên các bạn thử 1 trong 2 kiểu, tránh mất quá nhiều tài chính, vì... đôi khi nó sẽ tốn rất lớn (có lần mình tốn gần 1k$ chỉ cho việc chạy hạ tầng trên AWS trong 2 ngày).
   
Và đó là những mốc mình đưa ra, các bạn có thể thoải mái lựa chọn để follow, mình cũng sẽ cố gắng viết guide hết cho mọi người ở mọi level. Sau đây là đề bài chi tiết của mình:

***Xây dựng một ứng dụng đơn giản, trong đó có cài đặt và thiết lập luồng CI/CD, logging và monitoring với những yêu cầu sau:***
  - Ứng dụng là dạng CRUD đơn giản, viết bằng Python Flask hoặc Python FastAPI hoặc bất cứ ngôn ngữ nào, bất cứ framework nào mà các bạn tự tin, thuận tay, sân nhà của các bạn... Chỉ cần đảm bảo những điều sau: có API đọc và ghi vào database, API đọc ghi vào Redis và API để thực hiện healthcheck.
  - Cụm Database và Cache phải được thiết kế riêng biệt, theo mô hình HA.
  - Thiết lập luồng CI/CD đơn giản, đảm bảo tiêu chí sau: Tự build mỗi khi có commit code mới vào source code repository (nhớ tách riêng ci-cd/manifest repository ra nhé), khi build thì image được tag dựa theo môi trường, nếu là stagging thì tag theo git commit (short) còn nếu là build thì tag theo git tag version. Quá trình deploy có thể chọn deploy bằng bash script và Jenkins, Jenkins và Ansible, Jenkins và argoCD lên cụm K8S,...
  - Có luồng gửi log về một nơi tập trung (centralized) và có thể view log từ đó (chứ không cần phải vào thủ công từng server và dùng tail, cat hoặc vim).
  - Giám sát hạ tầng bằng Prometheus và Grafana, có setup alert rule để cảnh báo sớm khi service có lỗi.

Trên đây là đề bài đơn giản của mình, đó là một phần đề tài mình thử việc, khi mình nhận đề tài này thì hầu như là mình biết hết, tuy nhiên khi từ Cloud (chỗ cũ) xuống đề tài này là dạng on-premise, mình cũng bị chững tương đối và cũng có một số cải thiện do được mentor chỉ dạy, mình sẽ cố gắng truyền tải hết trong những bài viết của mình. Cho bạn nào muốn hình dung thì đây chính là workflow hoàn chỉnh của đề tài:

![workflow-of-project](../../Figures/tech-stack.jpg)

Oke, sau đây mình sẽ đi vào dựng từng thành phần của bài tập, các bạn có thể check qua phần phân tích đề bài và chọn giải pháp ở [đây](./bài-tập.md) hoặc có thể đi sâu vào từng phần cụ thể (code, database, ...) tùy theo nhu cầu, link mình sẽ tạo sau nha:

**Phần 1:** Tạo và setup database phục vụ cho ứng dụng [Link](./phần-1-database.md)

**Phần 2:** Chạy ứng dụng CRUD với database mới setup [Link](./phần-2-application.md)


