# 🧴Commerce

## 프로젝트 소개

인코스런에서 진행한 화장품 커머스 웹 어플리케이션 프로젝트입니다.</br>
👉 사이트 바로가기: https://incourserun.cf

### Github Repo

* Frontend: https://github.com/INCOURSE-RUN/2-incourserun-commerce-fe
* Backend: https://github.com/INCOURSE-RUN/2-incourserun-commerce-be

## 개발 기간 및 인원

* 개발 기간: 2022.06.13 ~ 2022.07.29
* 개발 인원
    * Frontend: 1명 (박태준)
    * Backend: 2명 (모창일, 최보미)

## 사용 기술

### Frontend

<section>
<img src="https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white"/> 
<img src="https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white"/>
<img src="https://img.shields.io/badge/Javascript-F7DF1E?logo=javascript&logoColor=black" />
<img src="https://img.shields.io/badge/Typescript-3178C6?logo=typescript&logoColor=white" />
<img src="https://img.shields.io/badge/Next.js-000000?logo=Next.js&logoColor=white"/>
<img src="https://img.shields.io/badge/Chakra%20UI-319795?logo=Chakra%20UI&logoColor=white" />
<img src="https://img.shields.io/badge/React-61DAFB?logo=React&logoColor=black" />
<img src="https://img.shields.io/badge/React Hook Form-FF4154?logo=React&logoColor=white"/>
<img src ="https://img.shields.io/badge/Redux-764ABC?logo=redux&logoColor=white"/>
</section>

### Backend

<section>
<img src="https://img.shields.io/badge/Django-092E20?logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=PostgreSQL&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon%20RDS-527FFF?logo=Amazon%20RDS&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon%20S3-569A31?logo=Amazon%20S3&logoColor=white"/>
</section>

### Server

<section>
<img src="https://img.shields.io/badge/Amazon%20AWS-232F3E?logo=Amazon%20AWS&logoColor=white"/>

<img src="https://img.shields.io/badge/Docker-2496ED?logo=Docker&logoColor=white"/>
</section>

### Common

<section>
<img src="https://img.shields.io/badge/Git-F05032?logo=Git&logoColor=white" />
<img src="https://img.shields.io/badge/Github-181717?logo=Github&logoColor=white" />
<img src="https://img.shields.io/badge/Github%20Actions-2088FF?logo=GithubActions&logoColor=white" />
<img src="https://img.shields.io/badge/Swagger-85EA2D?logo=Swagger&logoColor=black" />
<img src="https://img.shields.io/badge/Postman-FF6C37?logo=Postman&logoColor=white" />
<img src="https://img.shields.io/badge/Notion-000000?logo=Notion&logoColor=white" />
<img src="https://img.shields.io/badge/Slack-4A154B?logo=Slack&logoColor=white" />
<img src="https://img.shields.io/badge/Figma-F24E1E?logo=figma&logoColor=white" />
</section>

## 구현 기능

### 🔐 로그인/회원가입

- Kakao 계정 소셜로그인으로 간편하게 회원가입이 가능합니다.
- 이후 회원가입 페이지에서 추가정보를 작성하여 회원가입을 완료하고 서비스를 이용할 수 있습니다.

👇 카카오 로그인 시퀀스 다이어그램
<section><img src="https://i.imgur.com/cSb8ElL.png" width='600'/></section>

👇 로그인 → 회원가입 → 메인페이지 → 로그아웃</br>
![](https://i.imgur.com/GZKTfcc.gif)

### 🍔 햄버거탭

- 메뉴바를 열어서 홈, 상품보기, 마이페이지로 이동할 수 있습니다.

### 👀 상품보기

* 상품 목록
    - 상품 목록의 상품카드들을 보고 상품의 간략한 정보를 알 수 있습니다.
    - 상품카드를 클릭하면 상품 상세페이지로 이동합니다.

* 상품 상세페이지
    - 상품의 상세정보, 구매정보 그리고 리뷰를 확인할 수 있습니다.

👇 메인페이지 → 상품목록 → 상세페이지</br>
![](https://i.imgur.com/NKbocPE.gif)

### 🛒 장바구니

- 장바구니에서 상품보기에서 담은 상품들을 확인할 수 있습니다.
- 주문할 상품을 선택 및 수량 변경을 하고 결제하기 버튼을 눌러 주문결제로 넘어갑니다.

👇 장바구니 전체삭제 → 빈 장바구니 → 상품목록에서 장바구니 담기</br>
![](https://i.imgur.com/YF9u2WB.gif)

### 📦 주문하기

- 상품선택 → 바로구매 또는 장바구니 → 결제하기로 주문을 진행할 수 있습니다.

👇 장바구니 → 주문 → 메인페이지</br>
![](https://i.imgur.com/DoOjLfq.gif)

👇 상품 상세페이지 → 바로구매 → 주문목록</br>
![](https://i.imgur.com/wqa3mc3.gif)

### 👤 마이페이지

* 회원정보 수정
    - 프로필사진, 닉네임 등의 회원정보를 수정할 수 있습니다.
* 주문내역
    - 날짜별, 주문별로 주문내역을 확인할 수 있습니다.
* 내상품 리뷰
    - 배송완료된 상품에 대해 리뷰를 작성할 수 있습니다.
    - 주문별로 각 상품에 대해 1회만 작성 가능합니다.
* 회원탈퇴
    - 탈퇴 사유 및 '인코스런' 텍스트를 입력해야 탈퇴가 가능합니다.
    - 탈퇴하기 버튼을 누르면 탈퇴 사유가 저장되고 사용자 정보는 초기화되며, 카카오 계정 연동도 자동으로 해제됩니다.
* 로그아웃
    - 로그아웃 시 '로그아웃 하시겠습니까?'라는 팝업창이 뜹니다.
    - 확인 버튼을 누르면 로그아웃되고 로그인 화면으로 넘어갑니다.

👇 로그인 → 마이페이지 → 회원정보수정 → 로그아웃</br>
![](https://i.imgur.com/sc1Cw3M.gif)

👇 메인페이지 → 마이페이지 → 주문내역 → 주문취소 → 리뷰작성 → 리뷰내역</br>
![](https://i.imgur.com/VmugQoj.gif)

👇 마이페이지 → 탈퇴 → 재가입</br>
![](https://i.imgur.com/RbREGyn.gif)

# 보일러플레이트 가이드

## 개발 및 배포 환경

- Ubuntu 20.04.4 LTS
- python 3.8
- pip 21.2.4
- Django 3.2.7
- Django Rest Framework 3.12.4

## API 명세서

https://api.incourserun.cf/swagger/

## 0. 프로젝트 구조

**commerce**

**backend*

- `./app`
    - `[App name]`
        - `migrations`
        - `views.py`or`viewsets.py`
        - `urls.py`
        - `serializers.py`
        - `models.py`
        - `signals.py`
        - `admins.py`
    - `urls.py`
- `./config`
    - `settings`
        - `base.py`
        - `dev.py`
        - `prod.py`

---

**AWS 배포 및 서버 세팅*

- `.ebextension`
- `.github/workflow`

## 1. 프로젝트 기본 구성 폴더

### 1) app

장고의 app 폴더들이 있습니다.

urls.py는 app의 API url들을 config/urls/api 에 연결할 url들을 설정한 파일입니다.

#### (1) app

app 폴더는 모델(model.py)과 그 모델의 API(views.py) 그리고 모델의 종속적인 모델을 함께 포함하고 있습니다. app 폴더는 모델 혹은 기능을 기준으로 분리되어 있습니다.

app 폴더의 하위 폴더로 migrations 폴더가 있습니다. DB와 관련된 파일로, 수정할 경우 DB 오류가 발생합니다.

### 2) config

config 폴더는 프로젝트의 구성 파일들을 관리하는 폴더입니다.

#### (1) settings

settings 폴더는 프로젝트의 세팅 파일들을 관리합니다.

#### (2) urls

urls는 루트 urls 폴더입니다. hosts.py로 서브 도메인에 따라 분리되어 있습니다.

### 3) .ebextension

Elastic Beanstalk 관련 파일이 있습니다.

### 4) .github/workflow

Github action 관련 파일이 있습니다.

## 2. app 기본 구성 파일

### 1) views.py(viewsets.py)

API가 구현되어 있는 파일입니다.

### 2) urls.py

views.py에서 구현된 API들을 어떤 url에서 호출할 것인지 명시되어 있는 파일입니다.

기본적으로 프로젝트의 url은

```jsx
{project name}.co.kr/api/v1/{app name}/...
```

형태로 연결됩니다. (*프로젝트에 따라 변동 될 수 있습니다.)

### 3) serializers.py

API 별로 필요한 serailizer들을 구현한 파일입니다.

Django Rest Framework의 serializer는 DB에서 조회한 object를 JSON 형태로 변환하거나, Request의 JSON 데이터를 python data type으로 변환합니다.

### 4) models.py

모델(table)이 선언되어 있습니다.

### 5) admins.py

관리자 페이지에서 해당 모델의 페이지를 어떻게 구성할 것인지 구현되어 있습니다.

### 6) signals.py

app 모델의 데이터 수정 혹은 생성에 따라 실행되는 함수가 구현되어 있습니다.

## 3. app 폴더 별 설명

### 1) user

* 사용자 관련 모델이 있는 앱
* 모델
    - User: 사용자 모델
    - Social: 소셜로그인 모델
    - Withdrawal: 탈퇴 모델

### 2) product

* 상품 관련 모델이 있는 앱
* 모델
    - Product: 상품 모델

### 3) cart

* 장바구니 관련 모델이 있는 앱
* 모델
    - Cart: 장바구니 모델

### 4) order

* 주문 관련 모델이 있는 앱
* 모델
    - Order: 주문 모델
    - OrderProduct: 주문-상품 모델
* Custom Command
    - seed_orders.py: 주문 데이터 자동 생성 커맨드

### 5) review

* 리뷰 관련 모델이 있는 앱
* 모델
    - Review
    - Photo
    - Reply