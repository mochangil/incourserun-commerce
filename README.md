# Project Name

(*프로젝트 요약)

## 개발 및 배포 환경

- Ubuntu 20.04.4 LTS
- python 3.8
- pip 21.2.4
- Django 3.2.7
- Django Rest Framework 3.12.4

## API 명세서

postman link

# 0. 프로젝트 구조

**Project Name**

**백엔드* 

- `./api`
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

* *AWS 배포 및 서버 세팅*

- `.ebextension`
- `.github/workflow`
- `.platform`

# 1. 프로젝트 기본 구성 폴더

## 1. api

 api 폴더는 장고의 app 폴더들이 있습니다.

 urls.py는 app의 API url들을 config/urls/api 에 연결할 url들을 설정한 파일입니다.

### 1. app

 app 폴더는 모델(model.py)과 그 모델의 API(views.py) 그리고 모델의 종속적인 모델을 함께 포함하고 있습니다. app 폴더는 모델 혹은 기능을 기준으로 분리되어 있습니다.

 app 폴더의 하위 폴더로 migrations 폴더가 있습니다. DB와 관련된 파일로, 수정할 경우 DB 오류가 발생합니다.

## 2. config

 config 폴더는 프로젝트의 구성 파일들을 관리하는 폴더입니다.

### 1. settings

settings 폴더는 프로젝트의 세팅 파일들을 관리합니다.

### 2. urls

urls는 루트 urls 폴더입니다. hosts.py로 서브 도메인에 따라 분리되어 있습니다.

## 3.  .ebextension

Elastic Beanstalk 관련 파일이 있습니다.

## 4. .github/workflow

Github action 관련 파일이 있습니다.

## 5. .platform

Elastic Beanstalk 관련 파일이 있습니다.

# 2. app 기본 구성 파일


## 1. views.py(viewsets.py)

API가 구현되어 있는 파일입니다.

## 2. urls.py

 views.py에서 구현된 API들을 어떤 url에서 호출할 것인지 명시되어 있는 파일입니다.

기본적으로 프로젝트의 url은

```jsx
{project name}.co.kr/api/v1/{app name}/...
```

  형태로 연결됩니다. (*프로젝트에 따라 변동 될 수 있습니다.)

## 3. serializers.py

 API 별로 필요한 serailizer들을 구현한 파일입니다.

 Django Rest Framework의 serializer는 DB에서 조회한 object를 JSON 형태로 변환하거나, Request의 JSON 데이터를 python data type으로 변환합니다.

## 4. models.py

모델(table)이 선언되어 있습니다. 

## 5. admins.py

관리자 페이지에서 해당 모델의 페이지를 어떻게 구성할 것인지 구현되어 있습니다.

## 6. signals.py

app 모델의 데이터 수정 혹은 생성에 따라 실행되는 함수가 구현되어 있습니다.

# 3. app 폴더 별 설명


(*각 프로젝트마다 app별로 서술)