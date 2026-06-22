# im-not-strange-ai — 한국어 문장 다듬기 하네스

## 프로젝트 개요

Sunny식 문장 다듬기 규칙을 더한 한국어 윤문 플러그인 하네스. 번역투·영어 인용 과다·기계적 병렬·관용구·피동태 남용·접속사 남발·리듬 균일성·이모지/불릿 과다 등 AI 티 패턴을 점검하고, 문장 단위 보조 규칙을 적용한다.

## 철칙

1. **의미 불변 (Fidelity First)** — 사실·주장·수치·고유명사·인용은 100% 원문 보존.
2. **근거 기반 (Span-Grounded)** — 모든 변경은 탐지 finding에 연결. 탐지 없는 구간은 건드리지 않음.
3. **장르 유지 (Tone Match)** — 칼럼을 문학으로, 리포트를 에세이로 옮기지 않음.
4. **과윤문 금지 (No Over-Polish)** — 변경률 30% 초과 시 경고, 50% 초과 시 강제 중단.

## 디렉토리 구조

```
im-not-strange-ai/
├── CLAUDE.md                      # 본 파일 — 프로젝트 가이드
├── README.md / INSTALL.md         # 사용·설치 안내
├── .claude-plugin/                # Claude 플러그인 + 마켓플레이스 매니페스트
│   ├── plugin.json                # skills: ./.claude/skills/ · 에이전트는 루트 agents/ 자동탐색
│   └── marketplace.json           # im-not-strange-ai marketplace manifest
├── gemini-extension.json          # Gemini CLI Extension 매니페스트
├── GEMINI.md                      # Gemini 에이전트 컨텍스트 (monolith 룰 인라인)
├── commands/                      # Gemini CLI 커스텀 명령 (/im-not-strange-ai, /im-not-strange-ai-fast, /im-not-strange-ai-redo)
├── install.sh / uninstall.sh      # Claude·Codex·Gemini 전역 설치/제거 (심링크 기본)
├── agents/                        # 서브에이전트 12종 (플러그인 컨벤션 — 루트 agents/에 둬야 로드됨)
│   ├── im-not-strange-ai-monolith.md       # Fast 단일 호출
│   ├── ai-tell-detector.md · korean-style-rewriter.md
│   ├── content-fidelity-auditor.md · naturalness-reviewer.md
│   └── … taxonomist·scholar·distiller 등 지원 7종
├── .claude/skills/                # 스킬 3종 (im-not-strange-ai·im-not-strange-ai-fast·im-not-strange-ai-redo)
│   ├── im-not-strange-ai/
│   │   ├── SKILL.md               # 오케스트레이터 (quick_rules_path: ${CLAUDE_SKILL_DIR}/...)
│   │   └── references/            # SSOT — ai-tell-taxonomy·rewriting-playbook·quick-rules 등
│   ├── im-not-strange-ai-fast/
│   └── im-not-strange-ai-redo/
├── codex-plugin/skills/im-not-strange-ai/  # Codex Fast Path 스킬
│   ├── SKILL.md                   # monolith 기반 자가완결
│   └── references/                # .claude reference tree와 동일하게 유지
└── _workspace/                    # 런타임 산출물 (run_id별, gitignored)
    └── {YYYY-MM-DD-NNN}/          # 01_input.txt … final.md · summary.md
```

## 파이프라인

```
입력 텍스트
    ↓
[ai-tell-detector] — 탐지 (span·category·severity·suggested_fix)
    ↓
[korean-style-rewriter] — 윤문 (finding 기반 수술적 수정)
    ↓
[병렬 팀]
    ├─ [content-fidelity-auditor] — 의미 동등성 감사 (13항)
    └─ [naturalness-reviewer]     — 잔존 + 과윤문 판정
    ↓
[오케스트레이터 종합 판정]
    ├─ accept → final.md + summary.md
    ├─ rewrite_round_2 → 윤문가 재호출 (최대 3회)
    ├─ rollback_and_rewrite → 문제 edit 롤백
    └─ hold_and_report → 사람 검토 권고
```

## 5인 핵심 팀 (+ 웹 아키텍트 확장)

1. **korean-ai-tell-taxonomist** — 분류 체계 SSOT 관리. 실전에서 발견된 미분류 패턴을 심사해 v1→v2 승격.
2. **ai-tell-detector** — 탐지기. span 단위 JSON 리포트 생성. 문서 레벨 패턴(리듬·구조)도 포함.
3. **korean-style-rewriter** — 윤문가. finding 기반 수술적 재작성. 변경률 모니터링.
4. **content-fidelity-auditor** — 내용 감사관. 13항 체크리스트로 의미 훼손 탐지 → 롤백 지시.
5. **naturalness-reviewer** — 자연스러움 리뷰어. 탐지기 재실행으로 잔존·과윤문 계측. 품질 등급 판정.
6. **im-not-strange-ai-web-architect** (확장용) — 웹 서비스 요청 시 Next.js 15 + Vercel 아키텍처 설계.

## 심각도 기준

- **S1 결정적**: 한 번만 나와도 AI라고 확신하게 되는 패턴. 무조건 제거.
- **S2 강함**: 1~2회 허용, 3회+ 반복 시 제거.
- **S3 약함**: 다른 패턴과 중첩될 때만 문제.

## 품질 등급

- **A**: S1 0건, S2 2건 이하, score 개선 70%+
- **B**: S1 0건, S2 4건 이하, score 개선 50%+
- **C**: S1 1~2건 또는 과윤문 시그널 2개 — 2차 윤문
- **D**: S1 3건 이상 또는 심각한 과윤문 — 사람 검토

## 사용 방법

1. 새 세션에서 오케스트레이터 스킬 트리거:
   ```
   이 AI 글 자연스럽게 윤문해줘:
   ```
   (텍스트 첨부)
2. 오케스트레이터가 run_id 생성하고 5단계 파이프라인 실행.
3. 결과 `final.md` + `summary.md` 반환.

## 파일 시스템 접근 규칙

에이전트가 파일·디렉토리에 접근할 때는 전용 도구를 우선 사용한다.
`Bash` 툴의 `ls`·`cat`·`echo`는 실행 환경(OS·경로 형식)에 따라 동작이 달라져 예측 불가한 오류를 일으킬 수 있다.

| 작업 | 올바른 방법 | 피할 방법 |
|---|---|---|
| 파일 존재 확인 | `Glob` 도구 | `Bash` 툴 `ls` |
| 디렉토리 목록 열거 | `Glob` 도구로 안의 표지 파일 매칭 (예: `*/01_input.txt`) | `Bash` 툴 `ls` |
| 파일 읽기 | `Read` 도구 | `Bash` 툴 `cat` / `head` |
| 파일 쓰기·편집 | `Write` / `Edit` 도구 | `Bash` 툴 리다이렉션 |

## 주요 금기

- 수치·단위·날짜 변경 금지.
- 고유명사·제품명·모델명 변경 금지.
- 큰따옴표 인용문 내부 변경 금지.
- 법률 조문·학술 개념어 임의 치환 금지.
- 새로운 주장·사실·예시 추가 금지.
- 원문에 있던 정보 누락 금지.

## 확장 포인트

- **웹 서비스화**: `im-not-strange-ai-web-architect` 호출 → `_workspace/web/` 산출물 → 실제 구현 엔지니어(필요 시 신규 에이전트).
- **다국어 확장**: 일본어·중국어로 확장 시 언어별 taxonomy 분리 파일 추가.
- **장르 확장**: 현재 4장르(칼럼·리포트·블로그·공적). 학술 논문·법률 문서·제품 카피 추가 가능.

## 참고

- 분류 체계: `.claude/skills/im-not-strange-ai/references/ai-tell-taxonomy.md`
- 윤문 처방: `.claude/skills/im-not-strange-ai/references/rewriting-playbook.md`
- 웹 스펙: `.claude/skills/im-not-strange-ai/references/web-service-spec.md`
