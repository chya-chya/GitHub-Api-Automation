import requests
import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    print("환경변수를 설정해주세요!")
    exit()

# ==================== 설정값 입력 ====================
OWNER = "OWNER를 입력해주세요"            # 예: octocat
REPO = "REPO를 입력해주세요"              # 예: Hello-World
MY_ID = "깃허브 ID를 입력해주세요"        # 예: chya-chya
FILE_NAME = "생성할 파일명을 입력해주세요"  # 예: pr_data.json
# ====================================================

# GitHub API 기본 설정
BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_all_pull_requests() -> List[Dict[str, Any]]:
    """모든 PR(열린 + 닫힌)을 페이지네이션으로 가져옵니다."""
    prs = []
    page = 1
    per_page = 100  # 최대 100

    while True:
        url = f"{BASE_URL}/pulls"
        params = {
            "state": "all",   # open, closed, all
            "per_page": per_page,
            "page": page
        }
        response = requests.get(url, headers=HEADERS, params=params)
        
        if response.status_code != 200:
            raise Exception(f"PR 목록 조회 실패: {response.status_code} {response.text}")
        
        data = response.json()
        if not data:
            break
            
        prs.extend(data)
        print(f"페이지 {page} 완료 – 가져온 PR 수: {len(data)}")
        page += 1
    
    return prs

def filter_my_prs(prs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """MY_ID가 비어있지 않으면 본인의 PR만 필터링합니다."""
    if not MY_ID:
        return prs
    return [pr for pr in prs if pr["user"]["login"].lower() == MY_ID.lower()]

def main():
    if TOKEN == "깃허브 토큰을 입력해주세요" or not TOKEN:
        print("ERROR: GitHub Personal Access Token을 입력해주세요.")
        return

    if OWNER == "OWNER를 입력해주세요" or not REPO:
        print("ERROR: OWNER와 REPO 이름을 정확히 입력해주세요.")
        return
    
    if FILE_NAME == "생성할 파일명을 입력해주세요" or not FILE_NAME:
        print("ERROR: 파일명을 입력해주세요.")
        return
    try:
        print(f"{OWNER}/{REPO} 레포지토리의 Pull Request 데이터를 가져오는 중...")
        all_prs = get_all_pull_requests()
        print(f"총 {len(all_prs)}개의 PR을 조회했습니다.")
        
        # 필요하면 본인 PR만 필터링
        prs = filter_my_prs(all_prs)
        print(f"필터링 후 {len(prs)}개 남았습니다.")

				# PR 데이터를 필요한 정보만 추출
        data = []
        for pr in prs:
          data.append({
						"number": pr["number"],
						"title": pr["title"],
						"body": pr["body"],
						"state": pr["state"],
						"created_at": pr["created_at"],
						"merged_at": pr["merged_at"],
					})
				
        # JSON 파일로 저장
        os.makedirs("./data", exist_ok=True)
        with open(f"./data/{FILE_NAME}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"성공적으로 '{FILE_NAME}' 파일에 저장했습니다.")
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()