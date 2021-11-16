# humanscape-assignment

## 8️⃣ 기업과제
- 휴먼스케이프
- 기업사이트: https://humanscape.io/kr/index.html
- 기업채용공고: https://www.wanted.co.kr/wd/41413

## 8️⃣ 과제 내용

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

## 8️⃣ 팀: 리스테린(Listerine)

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
- `GET /trials/{int:trial_id}`: path parameter로 trial_id를 받아 특정 임상 연구 조회 할 수 있습니다.

### Unit test

테스트는 `/tests` 디렉토리에서 확인하실 수 있습니다. 그리고 루트 디렉토리에서 다음 명령어로 테스트를 실행할 수 있습니다.

```commandline
$ 
```

## 8️⃣ 모델 관계

![image](https://user-images.githubusercontent.com/32446834/141780326-f5aa1c00-d417-4452-aeef-a6c2f2ca6fdb.png)

[모델링 관련 회의내용](https://github.com/Pre-Onboarding-Listerine/humanscape-assignment.wiki.git)

### batch task

- 임상 연구 오픈 API를 이용해 데이터를 저장하거나 업데이트 시켜 출력하는 기능을 구현하였습니다.
-
-

## 애플리케이션 구조


## 8️⃣ 실행환경 설절 방법

> `git`과 `docker`, `docker-compose`가 설치되어 있어야 합니다.

1. 레포지토리 git 클론

    ```bash
    $ git clone 
    ```

2. 애플리케이션 실행하기

    ```bash
    $ docker-compose up

    # 애플리케이션을 백그라운드에서 실행하고 싶다면
    $ docker-compose up -d
    
    # 어플리케이션이 실행이 되고 난 후에 데이터베이스 migration이 필요하다면
    $ docker-compose exec api
    ```

3. 애플리케이션에 접근하기

    ```
   
    ```

## 8️⃣ 과제 결과물 테스트 및 확인 방법

1. POSTMAN 확인: 

2. 배포된 서버의 주소

    ```commandline

    ```

# 8️⃣ Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 휴먼스케이프에서 출제한 과제를 기반으로 만들었습니다.

