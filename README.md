# SEEYA Archive

## 컨벤션

### 브랜치 & PR

> feature/#{issue-number}-{feature-name}

- {feature-name}은 기능요약을 적는다.
- 메인 기준으로 배포 진행
- 이슈 기준으로 각 브랜치 생성
- develop 브랜치로 각 피쳐브랜치 PR / 스쿼시 머지로 진행한다.
- PR 날리면 상대방이 리뷰하고 approve되면 본인이 직접 머지한다.

### 커밋메세지

> [제목]\: [내용]

| 제목     | 내용                              |
| -------- | ---------------------------------|
| Init     | 작업 세팅 커밋 (패키지 설치 등)    |
| Implement| 큰 단위 기능 구현                  |
| Add      | 기능 추가                         |
| Fix      | 버그 수정 (in :위치, to/for: 이유)|
| Remove   | 삭제 (from: 위치)                |
| Move     | 코드, 파일 이동                   |
| Rename   | 이름 변경 (A to B 형식)           |
| Hotfix   | 급한 버그 수정                    |
| Refactor | 코드 개선                        |
| Chore    | 주석, 개행, 포맷팅 등 사소한 작업  |
| Docs     | 문서 작성                        |
