[Quay lại trang trước](../../README.md)

# Kì 1 - "Pet" project cho những DevOps tập sự

### **Mục lục**
### [1. Sơ lược](#1-pet-project)
### [2. Thành phần](#2-dự-án-này-bao-gồm)
### [3. Sơ đồ](#3-sơ-đồ-của-dự-án)
---

## 1. "Pet" project:

Định nghĩa đơn giản: "Pet" project chính là những dự án cá nhân của các bạn, là một môi trường để các bạn tự vọc vạch, thử nghiệm các phương án mới cho hệ thống của mình, có thể là refer từ những dự án ở công ty, có thể là thử triển khai các tools mới mà các bạn thấy hay ho trên Linkedln chẳng hạn.

Quan trọng hơn hết, project này không bị giới hạn gì cả. Ví dụ nhé, khi mình triển khai một project ở công ty cũ (do mình tự nghĩ ra và đề xuất), sau này khi nhảy việc, mình có mang dự án đó ra để phỏng vấn thì anh senior có bảo: "Em đang nhồi nhét quá nhiều, dùng dao mổ trâu cho việc thịt gà đó". Tức là gì, có thể khi đi làm, các bạn gặp 1 công nghệ hay 1 tool mới rất hay, nhưng việc áp dụng nó thì không dễ tẹo nào do còn liên quan hạ tầng, chi phí, rồi ai sẽ vận hành nó... thì dự án này là sân sau, giúp các bạn thỏa sức áp dụng bất cứ thứ gì các bạn thích đó.

Trong dự án này, mình sẽ tập trung vào phần cấu hình một cụm Database đơn giản chạy ``MySQL``, 1 cụm ``Redis`` đơn giản, 1 luồng CI-CD "phổ thông" với ``Jenkins`` và 1 chút nho nhỏ ``Ansible``. Hạ tầng ở đây mình sẽ dùng ``AWS`` cho tiện và đỡ mất công phải tạo máy ảo.

## 2. Dự án này bao gồm:
   
   Như mình nói ở trên, dự án này sẽ bao gồm một source code nhỏ cuả ứng dụng ``webapp``, ở đây mình sẽ sử dụng ``python`` và ``Flask`` cho nhanh. Trong source code này mình có sưr dụng caching, để cho giống như môi trường thật nhất có thể.

   Sau đó, khối database mình có sử dụng ``MySQL`` làm CSDL chính của hệ thống và ``Redis`` làm cache để tăng hiệu suất. Tất nhiên mình chỉ hoàn toàn dùng các thành phần cũng như các tính năng cơ bản, sau này có thể trình độ cao lên thì mình sẽ sử dụng những thứ đỉnh hơn chẳng hạn.

   Khi đã có ứng dụng và CSDL, tức là chúng ta hoàn toàn có thể để users truy cập nó rồi, tuy nhiên, đó mới chỉ là 1 nửa chặng đường. Để đảm bảo mỗi khi chúng ta code, release tính năng mới thì ứng dụng đang phục vụ người dùng cũng phải ngay lập tức được cập nhập lên phiên bản mới nhất đó và quá trình cập nhập phải đảm bảo vài tiêu chí như: nhanh gọn, tự động, dễ dàng roll-back nếu có lỗi. Và đó chính là chỗ mà ``CI-CD`` nhúng tay vào. Lúc này mình sẽ sử dụng SCM và ``Jenkins`` để triển khai luồng này. Mình sẽ dùng ``GitLab`` cùng với ``Jenkins``, ``Ansible`` cho phần này. Sau này thì sẽ có thêm cả ``ArgoCD`` nữa.

   Bên cạnh việc tự động hóa hệ thống của chúng ta, việc giám sát nó một cách tự động cũng tốn khá nhiều giấy mực. Ở phần này, mình sẽ dùng stack phổ thông nhất là ``Prometheus`` và ``Grafana`` cho việc giám sát hạ tầng, ``Telegram`` cho alert và ``ELK`` cho việc tập trung quản lý logs.

   Về phần ``Platform`` thì mình sẽ chọn ``AWS`` cho nhanh, vì giờ đây thì nhu cầu sử dụng Cloud càng ngày càng cao, tuy nhiên mình cũng sẽ có tập trung cả vào phần ``on-premise`` nữa vì đó mới là nguồn cội của mọi thứ. Trong project này, ``container`` và ``Kubernetes`` cũng sẽ được sử dụng, cũng như 1 ít ``Terraform`` và ``Helm`` nữa (để tiện cho việc automation).

## 3. Sơ đồ của dự án
   Để minh họa dễ dàng hơn, mình có để ở đây sơ đồ luồng của dự án
   ![Workflow](../../Figures/tech-stack.jpg)

   Hẳn là một sơ đồ lớn và một vài những biểu tượng nhìn rối mắt, tuy nhiên, chúng ta sẽ đi qua từng khối, từng phần một, và mình mong là sau khi xong project này, các bạn đang muốn bước chân vào nghề này sẽ đại ý nắm được những công việc mà DevOps làm và đừng bỏ quên project này, có thể sau này thậm chí chúng ta thêm những phần như là EKS, Control Tower, hoặc automation test, chaos testing,...

   Mình dự định sẽ chia thành các kì như sau
   - Kì 1: Đề bài và phân tích (là post này)
   - Kì 2: Setup và cấu hình Database
   - Kì 3: Setup CI-CD
   - Kì 4: Setup Monitoring
   - Kì 5: Setup Logging
   - Kì 6: Đưa toàn bộ hệ thống lên sử dụng các stack ở Cloud
   - Kì 7: Chuyển CI-CD qua GitHub Actions, ArgoCD,...
  
  **Kì tới: Setup Database, chạy demo ứng dụng và thêm Cache cho ứng dụng**

[Top](#kì-1---pet-project-cho-những-devops-tập-sự) 