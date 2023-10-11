## 길동화

## 실행 방법
1. 업로드 되어 있는 파일을 다운로드 후 원하는 ide 를 사용하여 실행시킨다.
2. python manage.py runserver 명령어를 사용하여 서버를 실행시킨다. (주의 : board/settings.py 속 DATABASES, SECRET_KEY 및 ALGORITHM 값은 local 혹은 사용 환경에 맞게 수정해야한다)
3. Postman 실행 후 workspace 에서 알맞은 HTTP method 와 엔드포인트를 적어준 뒤 Body -> raw -> JSON 으로 설정한 뒤 필요한 값을 입력 후 send 버튼을 클릭한다. (엔드포인트 타입은 아래 API 명세서 참조)

## ERD
![Cap 2023-08-15 19-40-26-202](https://github.com/7sungcola/wanted-pre-onboarding-backend/assets/10840728/f0fcc5b4-982f-4251-ac22-bd31d9149c9c)

## 데모 영상
[Demo Video](https://youtu.be/RoqSaHUz_2o)

## 구현 방법 및 이유
이메일 및 비밀번호 유효성 검사 부분의 경우 회원가입과 로그인 기능 두 곳 다 사용이 필요하여 validators.py 를 개별적으로 생성하여 import 하였음.
Pagination 의 경우 초기에는 paginator 를 import 하여 사용하려했지만, 리턴시 JsonResponse 로 리턴할 수 없는 객체 값으로 결과값이 생성되어 우회하여 다른 방법을 택함.

## API 명세서
[API Document](https://documenter.getpostman.com/view/18557656/2s9Xy6ppo1)
