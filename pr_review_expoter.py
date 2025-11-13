import requests
import json
import os

# 내가 작성한 리뷰를 가져오는 코드

TOKEN = "깃허브 토큰을 입력해주세요"
OWNER = "OWNER를 입력해주세요"
REPO = "REPO를 입력해주세요"
MY_ID = "깃허브 ID를 입력해주세요"
FILE_NAME = "생성할 파일명을 입력해주세요"
headers = {"Authorization": f"token {TOKEN}"}

# -------------------------------------
# 📦 공통: 페이지네이션 처리 함수
# -------------------------------------
def fetch_all_pages(url):
    """모든 페이지의 데이터를 한 번에 가져오는 함수"""
    all_data = []
    page = 1
    while True:
        res = requests.get(f"{url}&per_page=100&page={page}", headers=headers)
        if res.status_code != 200:
            print(f"⚠️ 요청 실패 ({res.status_code}): {res.text}")
            break
        data = res.json()
        if not data:
            break
        all_data.extend(data)
        page += 1
    return all_data

# -------------------------------------
# 1️⃣ 라인별 리뷰 코멘트 가져오기
# -------------------------------------
print("📥 라인별 리뷰 코멘트 수집 중...")
comments_url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/comments?"
comments = fetch_all_pages(comments_url)

my_line_comments = [
    {
        "type": "line_comment",
        "pr_number": c["pull_request_url"].split("/")[-1],
        "file": c["path"],
        "line": c["line"],
        "body": c["body"],
        "created_at": c["created_at"]
    }
    for c in comments
    if c.get("user", {}).get("login") == MY_ID
]

print(f"✅ 라인 코멘트 {len(my_line_comments)}건 수집 완료.")

# -------------------------------------
# 2️⃣ PR 단위 리뷰 가져오기 (approve / request changes 등)
# -------------------------------------
print("📥 PR 목록 및 리뷰 수집 중...")
prs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls?state=all"
prs = fetch_all_pages(prs_url)

my_reviews = []
for pr in prs:
    pr_number = pr["number"]
    reviews_url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pr_number}/reviews?per_page=100"
    reviews = fetch_all_pages(reviews_url)
    
    for r in reviews:
        if r.get("user", {}).get("login") == MY_ID:
            my_reviews.append({
                "type": "review",
                "pr_number": pr_number,
                "state": r["state"],  # APPROVED / CHANGES_REQUESTED / COMMENTED
                "body": r["body"],
                "submitted_at": r["submitted_at"]
            })

print(f"✅ PR 리뷰 {len(my_reviews)}건 수집 완료.")
# -------------------------------------
# 3️⃣ 통합 및 파일 저장
# -------------------------------------
all_activities = my_reviews + my_line_comments

os.makedirs("./data", exist_ok=True)
with open(f"./data/{FILE_NAME}", "w", encoding="utf-8") as f:
    json.dump(all_activities, f, ensure_ascii=False, indent=2)

print(f"✅ 내 리뷰 활동 {len(all_activities)}건이 {FILE_NAME} 파일로 저장되었습니다.")
