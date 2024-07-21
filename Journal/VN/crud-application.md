[Đề mục](./đề-mục.md)
[Phân tích đề bài](bài-tập.md)

# 1. Nhắc lại qua về kiến trúc thư mục
  Như bạn đã thấy ở trong directory của repo ``devops-application`` mà mình dẫn link ở trên, có rất nhiều thư mực, nhiều file. Tất cả mục đích của chúng cũng đều được mô tả trong guide ở Viblo, tuy nhiên mình cũng sẽ nhắc lại thêm 1 chút để các bạn có thể nắm được kĩ càng hơn:
  - ``app.py`` là file chính để chúng ta chạy ứng dụng, khi các bạn dùng command ``flask run``, Python-Flask sẽ tìm đúng đến file đó để thực thi và chạy web application của chúng ta.
  - ``__init.py__`` là file khởi tạo, trong file này chúng ta định nghĩa 1 vài thư viện, các biến toàn cục, v...v...
  - ``model`` là thư mục chứa thông tin về tất cả các đối tượng mà chúng ta dùng, ví dụ như ``employee``, ``department``,...
  - ``views`` là thư mục chứa thông tin về các lớp hiển thị của từng site trong web application của chúng ta.
  - ``template``, ``base.html`` là các file template frontend của chúng ta, bằng HTML đơn giản thôi.
  - ``instance`` chứa config của các biến, các secret của môi trường hiện tại chạy app, khuyến khích không đưa thư mục này vào trong SCM vì nó chứa thông tin nhạy cảm (user, password để vào database).
  - ``config.py`` là file cấu hình truyền vào cho application biết là nên chọn các config nào cho phù hợp với môi trường hiện tại.

# 2. Cài đặt và setup môi trường để chạy webapp.
  Như đã nói ở trên, nếu các bạn follow theo bài viết ở link gốc thì mọi người có thể bỏ qua phần này. Tuy nhiên, mình sẽ nhắc lại 1 số luu ý.
  Để chạy được ứng dụng này trên Ubuntu thì chúng ta cần vài bước setup.
  - Đầu tiên là cài đặt các packages cần thiết cho ``python``, đặc biệt là ``python-venv`` khi giờ đây, với các bản ubuntu từ 22 trở đi, mỗi khi cài thư viện cho ``python`` nó sẽ bắt chúng ta active 1 venv, nên là cứ cài venv cho chắc ăn vậy. Ngoài ra có vài package khác nữa nhưng mà mình đã viết kĩ ở file ``requirements.txt`` rồi nên các bạn chỉ cần chạy lệnh cài theo file là okela nha.
  - Các bạn cũng nhớ cập nhập lại connection URI của database và chạy câu lệnh ``flask migrate`` trước để nó tạo bảng trong database của chúng ta trước nha, nếu không sẽ bị lỗi.
  - Tuy nhiên, trước đó, chúng ta phải tạo database và user trước.
  ```sql
    CREATE USER 'application_account'@'%' IDENTIFIED BY 'password';
	CREATE DATABASE application_database;
	GRANT ALL PRIVILEGES ON application_database . * TO 'application_account'@'%';
  ```

  - Sau đó mới thực hiện migrate
  ```sh
  	flask db init    # init the database object
	flask db migrate # create migrate event
	flask db upgrade # execute to database
  ```

  Nếu như các bạn không thích chạy dạng application (vì phải cài nhiều thư viện quá, rồi setup cả một mớ các thứ khác) thì các bạn có thể dùng container image và file SQL backup sẵn của mình, tuy nhiên, nếu vậy thì có thể nó sẽ không được như các bạn mong muốn lắm, nên tùy theo nhu cầu nha.

  Đây là dockerfile để build của mình
  ```Dockerfile
  FROM python:3.8-slim-buster

  COPY requirements.txt requirements.txt
  RUN pip3 install -r requirements.txt

  COPY . .
  CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0."]
  ```

  - Để có image thì đầu tiên các bạn ``clone`` repository của mình về, build và đánh tag là được nha:
  ```sh
  git clone https://github.com/phungh67/devops-sample-application.git
  cd devops-sample-application
  docker build -t sample-app:1.0 .

  docker run -d --name sample-app -e "FLASK_CONFIG=development" -e "FLASK_APP=run.py" -p 5000:5000 sample-app:1.0
  ```

  - Lúc này applicaiton đã bắt đầu chạy, tuy nhiên nếu các bạn thử luôn thì có thể bạn sẽ gặp cảnh ``HTTP: 500`` do database chưa lên, vậy nên nhớ setup database trước nha.