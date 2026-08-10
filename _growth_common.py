"""count/percent 그래프 스크립트가 공유하는 데이터셋 설정."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# cur_time이 초 단위로 저장된 데이터셋은 60으로 나눠 분 단위로 맞춘다.
DATASET_DIV = {
    "gossipcop": 60.0,
    "politifact": 60.0,
    "pheme": 1.0,
    "Twitter15": 1.0,
    "Twitter16": 1.0,
}

# dataviz 팔레트 슬롯 1-5 (categorical, light mode)
DATASET_COLORS = {
    "gossipcop": "#2a78d6",
    "politifact": "#eb6834",
    "pheme": "#1baf7a",
    "Twitter15": "#eda100",
    "Twitter16": "#e87ba4",
}
