import pytest

from src.trials.domain.models import Trial


@pytest.fixture
def data():
    return [
        {
          "과제명": "조직구증식증 임상연구 네트워크 구축 및 운영(HLH)",
          "과제번호": "C130010",
          "연구기간": "3년",
          "연구범위": "국내다기관",
          "연구종류": "관찰연구",
          "연구책임기관": "서울아산병원",
          "임상시험단계(연구모형)": "코호트",
          "전체목표연구대상자수": "120",
          "진료과": "Pediatrics"
        },
        {
          "과제명": "대한민국 쇼그렌 증후군 코호트 구축",
          "과제번호": "C130011",
          "연구기간": "6년",
          "연구범위": "국내다기관",
          "연구종류": "관찰연구",
          "연구책임기관": "가톨릭대 서울성모병원",
          "임상시험단계(연구모형)": "코호트",
          "전체목표연구대상자수": "500",
          "진료과": "Rheumatology"
        },
        {
          "과제명": "Lymphoma Study for Auto-PBSCT",
          "과제번호": "C100002",
          "연구기간": "1년",
          "연구범위": "단일기관",
          "연구종류": "관찰연구",
          "연구책임기관": "가톨릭대 서울성모병원",
          "임상시험단계(연구모형)": "코호트",
          "전체목표연구대상자수": "",
          "진료과": "Hematology"
        }
    ]


@pytest.fixture
def trials(data):
    return list(map(
            lambda trial: Trial(
                trial_id=trial["과제번호"],
                name=trial["과제명"],
                period=trial["연구기간"],
                scope=trial["연구범위"],
                category=trial["연구종류"],
                institution=trial["연구책임기관"],
                stage=trial["임상시험단계(연구모형)"],
                subjects_count=int(trial["전체목표연구대상자수"]) if trial["전체목표연구대상자수"] else 0,
                department=trial["진료과"]
            ),
            data
        ))
