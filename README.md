# GitHub PR 리뷰 활동 수집기

내가 작성한 **라인별 코멘트**와 **PR 리뷰**(Approve / Changes Requested / Comment)를  
GitHub API로 한 번에 모아 JSON 파일로 저장해주는 스크립트입니다.

> “내가 얼마나 리뷰했는지 한눈에 보고 싶다!”  
> → 이 스크립트 하나면 끝!

## 기능

- 모든 PR의 **라인별 리뷰 코멘트** 수집  
- 모든 PR의 **리뷰 상태**(APPROVED, CHANGES_REQUESTED, COMMENTED) 수집  
- 결과물을 `./data/내가원하는파일명.json` 으로 저장  

## 사용법

### 1. 준비물

```bash
pip3 install requests
pip3 install python-dotenv
```

### 2. 코드 수정
`.env` 파일을 루트 디렉토리에 추가해주시고 깃허브 토큰을 입력해 주세요

```.env
GITHUB_TOKEN=your_github_token
```

**Token 생성 팁**  
→ Settings → Developer settings → Personal access tokens → Tokens (classic)  
→ `repo` 스코프만 체크하면 충분합니다.

`pr_review_expoter` 파일 상단의 아래 4개 값을 본인 것으로 바꿔주세요.

```python
OWNER     = "조직 또는 사용자 이름"
REPO      = "레포지토리 이름"
MY_ID     = "본인의 GitHub 아이디"
FILE_NAME = "저장할파일명.json"              # 예: my_reviews_2025.json
```


### 3. 실행

```bash
python3 pr_review_expoter.py
```

### 4. 결과 확인

```
./data/
   └── my_reviews_2025.json   ← 여기 저장됨
```

### 출력 예시

```json
[
  {
    "type": "review",
    "pr_number": 123,
    "state": "APPROVED",
    "body": "LGTM! 배포해도 될 것 같아요",
    "submitted_at": "2025-11-01T10:23:45Z"
  },
  {
    "type": "line_comment",
    "pr_number": 124,
    "file": "src/utils.py",
    "line": 42,
    "body": "여기서 None 체크 빠졌어요!",
    "created_at": "2025-11-02T14:15:22Z"
  }
]
```

## 기여하기

- 더 많은 필드(리액션, 리뷰 요청 등) 추가하고 싶으신가요?  
- PR 환영합니다!

## 라이선스

MIT © 2025 차수연
