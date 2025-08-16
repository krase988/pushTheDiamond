
# Push The Diamond

## 🎮 게임을 즐기는 분들을 위한 안내

### 소개
Push The Diamond는 Python tkinter로 제작된 퍼즐 게임입니다. 각 레벨마다 다른 규칙과 퍼즐이 등장하며, 플레이어는 다이아몬드(◆) 버튼을 찾아 다음 레벨로 진행해야 합니다.

### 실행 방법
1. Python 3.x가 설치되어 있어야 합니다.
2. `push_the_diamond.py` 파일이 있는 폴더에서 아래 명령어로 실행하세요:

    ```bash
    python push_the_diamond.py
    ```

### 게임 규칙 및 조작법
- 각 레벨마다 버튼의 배치와 규칙이 다릅니다.
- 힌트(Hint) 버튼을 누르면 5초간 힌트가 표시됩니다.
- Exit 버튼을 누르면 종료 확인 창이 뜹니다.
- 실패 시 랜덤 메시지와 함께 해당 레벨이 다시 시작됩니다.
- 모든 버튼은 ID(1~27)가 부여되어 있으며, 일부 레벨에서는 버튼의 이름과 상태가 동적으로 변경됩니다.

### 레벨 구성
- START: 게임 시작 화면
- LEVEL 1~5: 점점 난이도가 올라가는 퍼즐
- LEVEL X: 축하 스테이지
- YOU BEST: 엔딩 화면

---

## 🛠️ 개발자/기여자를 위한 안내

### 코드 구조
- 메인 클래스: `PushTheDiamond`
- 주요 함수:
   - `create_all_buttons`: 버튼 전체 생성
   - `remove_all_buttons`: 버튼 전체 삭제
   - `add_missing_buttons`: 누락된 버튼만 생성
   - `reset_buttons`, `set_button_name`, `remove_merged_buttons` 등
- 레벨별 로직: `level1`, `level2`, ..., `level_best` 함수에서 관리

### 커스터마이즈/유지보수 팁
- 레벨 추가/수정은 각 레벨 함수에서 구현
- 버튼 생성/삭제/상태 변경은 utility 함수로 관리
- 힌트, 실패 처리, UI 리셋 등은 별도 함수로 분리되어 있음

### 의존성 및 환경
- Python 3.x
- 표준 라이브러리(tkinter, random)

### 기여 및 문의
- 개발자: krase988
- 이슈 및 제안은 GitHub 저장소 Issue 또는 Pull Request로 남겨주세요.
