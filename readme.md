## 동작 방법

### SQL
 - 자신이 사용하는 SQL에 스키마를 생성 후 emotion.sql 코드를 복사 붙혀놓기 후 실행
 - (필자는 MySQL을 사용함)

### Spring
- application.properties 설정 (적은 부분만 변경하면 됨)
2. spring.datasource.url=jdbc:mysql://localhost:(포트번호)/(스키마)?useSSL=false&characterEncoding=UTF-8&serverTimezone=UTC
3. spring.datasource.username=(DB 이름)
4. spring.datasource.password=(DB 패스워드)

 - maven update 실행
 - 내장 톰켓 실행 EmotionApplication 실행하면 구동