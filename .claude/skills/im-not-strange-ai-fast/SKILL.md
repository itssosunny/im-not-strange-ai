---
name: im-not-strange-ai-fast
description: AI가 쓴 한글 텍스트를 자연스럽게 윤문하는 빠른 진입 명령. im-not-strange-ai 파이프라인을 Fast 모드로 실행하고 `--strict`면 정밀 파이프라인으로 넘긴다. 트리거 — "/im-not-strange-ai-fast".
argument-hint: "[윤문할 텍스트 또는 파일 경로]"
disable-model-invocation: true
---

# /im-not-strange-ai-fast — 빠른 한국어 문장 다듬기

`im-not-strange-ai` 스킬을 발동해 인자로 전달된 한글 텍스트(또는 파일)에 윤문을 실행한다.

## 입력
$ARGUMENTS

## 동작
1. 인자가 비면: "윤문할 텍스트를 붙여넣어 주세요" 안내 후 종료.
2. 인자가 파일 경로(.txt/.md)면 `Read`로 본문 로드.
3. 인자가 텍스트면 그대로 입력으로 사용.
4. `im-not-strange-ai` 스킬 SKILL.md 절차(Phase 0 -> 결과 전달)를 따른다. 기본은 **Fast 모드**, `--strict` 시 strict 파이프라인.
5. 결과 전달:
   - 한 줄 상태(변경률 / 등급 / 자체검증 통과)
   - 윤문본 본문(마크다운 블록)
   - 카테고리별 탐지 건수 before/after
   - 주요 변경 하이라이트 3~5건
   - 등급 B 이하면 "`/im-not-strange-ai-redo`로 2차 윤문 가능" 안내

## 옵션 (인자 끝에 자연어로)
- `장르: 칼럼|리포트|블로그|공적` — 장르 명시 (생략 시 첫 300자로 자동 추정)
- `강도: 보수|기본|적극` — 윤문 강도 (기본값: 기본)
- `최소심각도: S1|S2|S3` — 탐지 임계값 (기본값: S2)
- `--strict` — 정밀 파이프라인 강제

## 참고
- 분류 체계: `im-not-strange-ai/references/ai-tell-taxonomy.md`
- 윤문 처방: `im-not-strange-ai/references/rewriting-playbook.md`
