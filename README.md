# humanscape-assignment

## 👨‍👨‍👧‍👦 기업과제
- 휴먼스케이프
- 기업사이트: https://humanscape.io/kr/index.html
- 기업채용공고: https://www.wanted.co.kr/wd/41413

## 👨‍👨‍👧‍👦 과제 내용

### **[필수 포함 사항]**

- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

### 확인 사항

- **ORM 사용 필수**
- **데이터베이스는 SQLite로 구현**
- **secret key, api key 등을 레포지토리에 올리지 않도록 유의**
    - README.md 에 관련 설명 명시 필요

### 도전 과제: 스스로에게도 도움이 되는 내용 + 추가 가산점

- 배포하여 웹에서 사용 할 수 있도록 제공
- 임상정보 검색 API 제공

### 과제 안내

다음 사항들을 충족하는 서비스를 구현해주세요.

- 임상정보를 수집하는 batch task
    - 참고: [https://www.data.go.kr/data/3074271/fileData.do#/API 목록/GETuddi%3Acfc19dda-6f75-4c57-86a8-bb9c8b103887](https://www.data.go.kr/data/3074271/fileData.do#/API%20%EB%AA%A9%EB%A1%9D/GETuddi%3Acfc19dda-6f75-4c57-86a8-bb9c8b103887)
- 수집한 임상정보에 대한 API
    - 특정 임상정보 읽기(키 값은 자유)
- 수집한 임상정보 리스트 API
    - 최근 일주일내에 업데이트(변경사항이 있는) 된 임상정보 리스트
        - pagination 기능
- **Test 구현시 가산점이 있습니다.**

## 👨‍👨‍👧‍👦 팀: 리스테린(Listerine)

* 팀원

| 이름 | 역할 | GITHUB | BLOG |
| :---: | :---: | :---: | :---: |
| `김주완` |  | [joowankim](https://github.com/joowankim) | https://make-easy-anything.tistory.com |
| `박은혜` |  | [eunhye43](https://github.com/eunhye43) | https://velog.io/@majaeh43 |
| `윤수진` |  | [study-by-myself](https://github.com/study-by-myself)| https://pro-yomi.tistory.com |
| `주종민` |  | [Gouache-studio](https://github.com/Gouache-studio) | https://gouache-studio.tistory.com/ |

## 구현 내용

### 이 중에서 과제에서 구현하도록 언급된 엔드포인트는 다음과 같습니다.

- `GET /list`: 전체 임상 연구 리스트를 출력할 수 있습니다. 
- `GET /trials/{trial_id}`: path parameter로 `trial_id`를 받아 특정 임상 연구 조회 할 수 있습니다.

### Unit test

테스트는 `/tests` 디렉토리에서 확인하실 수 있습니다. 그리고 루트 디렉토리에서 다음 명령어로 테스트를 실행할 수 있습니다.

```bash
# 프로젝트 루트 
$ pytest
```

## 👨‍👨‍👧‍👦 모델 관계

![image](https://user-images.githubusercontent.com/32446834/142003506-26349b83-d65a-4912-a5a9-b887d7aed36a.png)

[모델링 관련 회의내용](https://github.com/Pre-Onboarding-Listerine/humanscape-assignment.wiki.git)

### batch task

임상 연구 오픈 API를 이용해 데이터를 가져와서 저장하거나 현재 가지고 있는 데이터를 업데이트하는 배치 태스크를 구현하였습니다.
저희가 구현한 배치 태스크는 다음과 같은 특징을 갖습니다.

- 배치 태스크의 동작을 확인하기 위해 매 분마다 데이터 동기화 태스크가 동작합니다.
- 구현된 읽기 애플리케이션과는 서로 다른 컨테이너에서 서로 다른 프로세스로써 동작합니다.
- 배치 태스크는 읽기 애플리케이션과 같은 데이터베이스의 테이블을 공유합니다.
- 배치 태스크의 할당은 `run_cron.py`에서 수행되며 이를 수행하는 곳은 `tasks.py`입니다.
- 배치 태스크의 jobstore와 broker의 역할은 모두 `Redis` 서비스가 담당합니다.

## 애플리케이션 구조

애플리케이션은 기본적으로 계층화된 구조를 가지고 있습니다. 그 계층은 `presentation(routers.py)`, `application(application)`, `domain(domain)`, `persistence(infra)`로 이루어져 있습니다.
각 계층은 다음과 같은 역할을 수행합니다.

- `presentation`: 애플리케이션으로 들어온 요청을 처리할 수 있는 application 계층의 service로 전달합니다.
- `application`: domain 모델을 사용하는 클라이언트 역할을 하며 persistence 계층으로의 접근을 제어하며, 트랜잭션을 관리합니다.
- `domain`: 애플리케이션이 해결하는 문제 영역의 중심이 되는 컴포넌트들이 위치합니다.
- `persistence`: 데이터를 실제로 보관하고 있는 곳으로의 접근을 제어합니다.

### 주요 설계 포인트

#### 추상클래스를 이용한 데이터 저장소로의 접근

- 데이터로의 접근을 제어하기 위해서 `DataSource`와 `Repository` 컴포넌트를 구현했습니다.
-  각각은 필요한 메소드가 추상화된 `AbstractTrialDataSource`와 `AbstractTrialRepository`를 구현해 오픈 API와 데이터베이스에 접근할 수 있도록 구현하였습니다.

#### 작업단위(Unit of Work)를 이용한 트랜잭션 관리

- 작업단위 컴포넌트의 `__enter__`와 `__exit__` 메소드를 오버라이드해서 이를 컨텍스트 매니저로써 사용할 수 있도록 구현하였습니다.
- `__enter__` 메소드에서 세션과 `Repository`나 `DataSource` 객체를 생성해 작업단위의 컨텍스트 내에서만 데이터 저장소에 접근할 수 있도록 하였습니다.
- `__exit__` 메소드에서 `rollback`을 호출하고 세션을 닫아서 커밋되지 않은 변경사항을 롤백시킵니다.

## 👨‍👨‍👧‍👦 실행환경 설절 방법

> `git`과 `docker`, `docker-compose`가 설치되어 있어야 합니다.

1. 레포지토리 git 클론

    ```bash
    $ git clone 
    ```
   
2. `<프로젝트 루트 디렉토리>/src/configs`, 해당 경로에 `secret.py`를 생성합니다.

    ```python
    # secret.py
    DATA_SOURCE_END_POINT = "https://api.odcloud.kr/api/3074271/v1/uddi:cfc19dda-6f75-4c57-86a8-bb9c8b103887"
    DATA_SOURCE_AUTHORIZATION = "<발급받은 Encoding 인증키>"
    DATA_SOURCE_SERVICE_KEY = "<발급받은 Decoding 인증키>"
    ```

3. 애플리케이션 실행하기

    ```bash
    $ docker-compose up

    # 애플리케이션을 백그라운드에서 실행하고 싶다면
    $ docker-compose up -d
    ```

4. 로컬에서 실행된 애플리케이션에 접근하기

    ```commandline
    # 호스트 URLs
    http://localhost:8000
    ```

## 👨‍👨‍👧‍👦 과제 결과물 테스트 및 확인 방법

1. POSTMAN 확인: 

2. 배포된 서버의 주소

    ```commandline
    13.124.179.161:8000
    ```

# 👨‍👨‍👧‍👦 Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 휴먼스케이프에서 출제한 과제를 기반으로 만들었습니다.

