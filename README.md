# im-not-strange-ai — 한국어 문장 다듬기 플러그인 v2.0

`im-not-strange-ai`는 `im-not-ai`에서 영감을 받아 만든 한국어 문장 다듬기 플러그인입니다. AI(ChatGPT · Claude · Gemini 등)가 쓴 한글 글을 **내용은 보존한 채** 문체 · 리듬 · 표현만 자연스러운 한국어로 다듬습니다.

번역투, 과도한 영어 인용, 기계적 병렬 ("첫째 · 둘째 · 셋째"), "결론적으로 / 시사하는 바가 크다" 같은 AI 특유 관용구, 피동태 남용, 문두 접속사 남발, 이모지·불릿 남용 등 **10대 카테고리 × 40+ 서브 패턴**을 심각도(S1/S2/S3)로 분류해 스팬 단위로 탐지한 뒤, 윤문합니다.

현재는 로컬 개발 단계입니다. Marketplace 배포는 아직 확정하지 않았습니다.

## 왜 만들었나

`im-not-ai`가 보여준 AI 한국어 탐지 구조와 의미 보존 원칙을 바탕으로, 실제 글쓰기에서 자주 걸리는 문장 단위의 어색함을 더 작고 안전하게 고치도록 조정했습니다.

Sunny 7규칙은 발견한 표현을 무조건 지우는 치환표가 아니라 **의심 → 역할 확인 → 필요할 때만 수정**하는 보조 판단 기준입니다.

## 설치 (Install)

> **Claude Code**와 **OpenAI Codex CLI** 양쪽을 지원합니다. 전체 가이드: [`INSTALL.md`](INSTALL.md)

**Claude Code — 플러그인 마켓플레이스**

아직 배포 전입니다. 원격 저장소와 marketplace 등록을 결정한 뒤 설치 명령을 확정합니다.

**Claude Code · Codex CLI — 클론 + 스크립트**

```bash
git clone https://github.com/itssosunny/im-not-strange-ai.git
cd im-not-strange-ai
./install.sh            # 설치된 claude/codex 자동 감지 → 전역 심링크
```

- Claude: `/im-not-strange-ai` · Codex: `$im-not-strange-ai`
- 한쪽만: `./install.sh --claude-only` / `--codex-only` · 제거: `./uninstall.sh`
- **업데이트**: `./update.sh` — 새 버전 자동 감지 후 `git pull` + 재설치(`--check`는 감지만). 마켓플레이스 설치는 `/plugin update`.
- Codex는 **Fast(단일 호출) 모드만** 제공합니다. 정밀 strict 5인 파이프라인은 Claude Code 전용.

## 왜 한글 특화인가

영어권 문장 다듬기 도구(QuillBot · Hix · Undetectable AI)는 한국어에 약합니다. 한글 AI 글의 티는 대부분 **영어 번역투**에서 나옵니다.

- "AI 기술을 **통해** 효율을 높**일 수 있다**" → "AI로 효율을 높인다"
- "이에 **있어서** 중요한 **점은**" → "여기서 중요한 건"
- "~**에 의해** 생성된" → "~가 만든"
- "**결론적으로**, 이는 **시사하는 바가 크다**" → (삭제)

이 하네스는 그 한글 고유 패턴을 SSOT로 정리하고, 탐지·윤문·내용 감사·자연스러움 검증을 분리된 에이전트로 수행합니다.

## 4대 철칙

1. **의미 불변** — 사실 · 주장 · 수치 · 고유명사 · 직접 인용은 100% 원문 보존.
2. **근거 기반** — 탐지된 span에만 수술적 수정. 탐지 없는 구간은 건드리지 않음.
3. **장르 유지** — 칼럼을 문학으로, 리포트를 에세이로 옮기지 않음.
4. **과윤문 금지** — 변경률 30% 초과 시 경고, 50% 초과 시 강제 중단.

## 아키텍처 (v2.0)

**Fast 모드 (디폴트, 5,000자 이하)**

```
입력 텍스트
    ↓
[im-not-strange-ai-monolith]   ── 한 콜 안에서 탐지 → 윤문 → 자체검증 일괄
    ↓                     (도구 호출 4~5회 캡, opus, ~3분)
final.md + summary.md
```

**Strict 모드 (`--strict` 또는 8,000자+ 자동 승급)**

```
입력 텍스트
    ↓
[ai-tell-detector]        ── 탐지 (span · category · severity)
    ↓
[korean-style-rewriter]   ── finding 기반 수술적 윤문
    ↓
[병렬 검증 팀]
    ├─ [content-fidelity-auditor]  ── 13항 체크리스트로 의미 동등성 감사
    └─ [naturalness-reviewer]      ── 탐지 재실행으로 잔존·과윤문 판정
    ↓
[오케스트레이터 종합]
    ├─ accept              → final.md + summary.md
    ├─ rewrite_round_2     → 2차 윤문 (최대 3회)
    ├─ rollback_and_rewrite → 문제 edit 롤백
    └─ hold_and_report     → 사람 검토 권고
```

## 7인 에이전트

| 에이전트 | 모드 | 역할 |
|---------|---|------|
| `im-not-strange-ai-monolith` | **Fast 디폴트** | 단일 호출 윤문 (탐지·윤문·자체검증 일괄, 도구 호출 4~5회 캡) |
| `ai-tell-detector` | Strict | span 단위 JSON 탐지 리포트 생성 |
| `korean-style-rewriter` | Strict | finding 기반 수술적 윤문, 변경률 모니터링 |
| `content-fidelity-auditor` | Strict | 의미 동등성 감사 (13항), 훼손 시 롤백 지시 |
| `naturalness-reviewer` | Strict | 잔존 AI 티 · 과윤문 · 자연도 판정, 품질 등급 A~D |
| `korean-ai-tell-taxonomist` | 별도 명령 | 분류 체계(SSOT) 관리, 신규 패턴 심사 승격 |
| `im-not-strange-ai-web-architect` | 옵션 | Next.js 15 + Vercel 웹 서비스 확장 설계 |

## AI 티 분류 체계 (요약)

| ID | 대분류 | 대표 서브 패턴 |
|----|-------|---------------|
| A | 번역투 | "~를 통해", "~에 대해", "~에 있어서", 이중 피동 "~되어진다", "가지고 있다", **"그/그녀" 강박적 사용 (A-16)**, **관계절 좌향 수식 (A-18)**, **"~에서의/~에로의" 이중 조사 (A-19)** |
| B | 영어 인용·용어 과다 | 과도한 괄호 병기, 번역 가능한 영어 그대로 |
| C | 구조적 AI 패턴 | 기계적 "첫째/둘째/셋째", 과도한 불릿·헤딩·이모지, 연결어미 뒤 쉼표 (C-11) |
| D | AI 특유 관용구 | "결론적으로", "시사하는 바가 크다", "주목할 만하다", "혁신적인" |
| E | 리듬 균일성 | 문장 길이 표준편차 낮음, 동일 종결어미 반복, **청자 경어법 일관성 손실 (E-7)** |
| F | 수식·중복 | "매우", "정말", 동의어 이중 수식, "~적/~성/~화/-tion/-ment" 남발 |
| G | Hedging 남용 | "~할 수 있을 것으로 보인다" 다중 완곡 |
| H | 접속사 남발 | 문두 "또한/따라서/즉/나아가" 연속 |
| I | 형식명사 과다 | "것이다", "점", "수", "바", "~할 필요가 있다" |
| J | 시각 장식 남용 | 과도한 **볼드**, "따옴표", 대시(—) 남발 |

전체 60+ 서브 패턴과 처방: [`ai-tell-taxonomy.md`](.claude/skills/im-not-strange-ai/references/ai-tell-taxonomy.md) · [`rewriting-playbook.md`](.claude/skills/im-not-strange-ai/references/rewriting-playbook.md) · 학술 인용 외부 SSOT: [`scholarship.md`](.claude/skills/im-not-strange-ai/references/scholarship.md)

### Sunny 7규칙 — 문장 단위 보조 레이어

A~J가 AI 티 패턴을 잡는 본체라면, Sunny 7규칙은 문장 안의 작은 어색함을 마지막에 점검하는 보조 레이어입니다. 정식 기준은 [`quick-rules.md`](.claude/skills/im-not-strange-ai/references/quick-rules.md)와 [`sunny-sentence-rules.md`](.claude/skills/im-not-strange-ai/references/sunny-sentence-rules.md)에 두고, README에는 요약만 둡니다.

| ID | 의심 표현 | 예시 | 왜 고치나 | 유지 조건 |
|---|---|---|---|---|
| SUNNY-1 | `-적`이 붙은 말 | "전략적 중요성을 가지고 있다" → "전략상 중요하다" | 추상 명사가 겹치면 술어가 약해지고 글이 보고서 번역투처럼 흐려집니다. | 개념어·전문어·대조에 필요하면 유지 |
| SUNNY-2 | 조사 `의` | "서비스의 사용의 편의성" → "서비스 사용 편의성" | `의`가 겹치면 관계가 선명해지는 게 아니라 명사 더미만 길어집니다. | 소유·출처·고정 용어면 유지 |
| SUNNY-3 | 접미사 `들` | "사용자들은 이 기능들을 자주 쓴다" → "사용자는 이 기능을 자주 쓴다" | 한국어는 문맥으로 복수가 드러나는 경우가 많아, 불필요한 `들`은 영어식 복수 표시처럼 보입니다. | 실제 복수·분포·강조가 필요하면 유지 |
| SUNNY-4 | 의존명사 `것` | "이 기능을 추가하는 것은 도움이 된다" → "이 기능을 추가하면 도움이 된다" | `것`이 술어를 뒤로 밀면 문장이 한 박자 늦고 딱딱해집니다. | 실제 대상·인용된 생각·필요한 추상화면 유지 |
| SUNNY-5 | `있는/있다는` | "문제를 해결할 수 있는 방법" → "문제를 해결할 방법" | 의미 없이 끼는 `있는`은 명사 앞 완충재가 되어 문장의 힘을 뺍니다. | 존재·소유·진행 상태가 핵심이면 유지 |
| SUNNY-6 | 사족 `있었다` | "어제 장애 발생이 있었다" → "어제 장애가 발생했다" | 사건을 명사로 만들고 `있었다`로 받으면 책임·동작·시간이 흐릿해집니다. | 과거 존재·위치·소유·상태를 말하면 유지 |
| SUNNY-7 | 어색한 `있다` 패턴 | "사용자에게 있어 속도는 중요하다" → "사용자에게 속도는 중요하다" | `관계에 있다`, `~에 있어` 같은 표현은 쉬운 관계를 관료적 번역투로 만듭니다. | 고정·기술 표현이거나 존재 의미가 분명하면 유지 |

## 심각도 & 품질 등급

**심각도**

- **S1 결정적**: 한 번만 나와도 AI 확신. 무조건 제거.
- **S2 강함**: 1~2회 허용, 3회+ 반복 시 제거.
- **S3 약함**: 다른 패턴과 중첩될 때만 문제.

**품질 등급 (윤문 후)**

- **A**: S1 0건, S2 ≤2건, 점수 개선 70%+
- **B**: S1 0건, S2 ≤4건, 개선 50%+
- **C**: S1 1~2건 or 과윤문 시그널 2개 → 2차 윤문
- **D**: S1 3건+ or 심각한 과윤문 → 사람 검토

## 사용법 — 5분이면 따라합니다

> **전역 설치([설치](#설치-install))를 마쳤다면** 1~2단계(클론·폴더 진입)는 건너뛰고, 아무 폴더에서나 바로 **3단계**로 가세요. 아래는 설치 없이 리포에서 곧바로 체험하는 흐름입니다.

### 0. 전제

[Claude Code](https://claude.com/claude-code)가 설치돼 있어야 합니다. Mac · Windows · Linux 모두 지원합니다.

설치 확인:
```bash
claude --version
```

> Claude Code는 터미널에서 Claude(Anthropic의 AI)와 대화하며 파일을 같이 편집하는 CLI입니다. 이 리포의 스킬·에이전트는 Claude Code에서만 작동합니다. (웹 버전 Claude.ai나 일반 ChatGPT에서는 안 됩니다.)

### 1. 리포 받기

```bash
git clone https://github.com/itssosunny/im-not-strange-ai.git
cd im-not-strange-ai
```

### 2. Claude Code 켜기

```bash
claude
```

> **전역 설치를 했다면** 아무 폴더에서나 켜도 `/im-not-strange-ai`이 동작합니다([설치](#설치-install) 참고).
> **설치 없이 체험만 하려면** `im-not-strange-ai` 폴더 **안에서** 실행하세요(프로젝트 로컬 스킬이 로드됩니다). 다른 위치에서 켜면 일반 Claude Code처럼 동작합니다.

### 3. AI가 쓴 한글 글 붙여넣고 부탁하기

Claude Code에서는 아래 방법 중 편한 쪽으로 사용합니다. Codex 사용자는 **방법 D**를 참고하세요.

**방법 A — 자연어 한 문장 (가장 쉬움)**

평소 말투 그대로 쓰면 됩니다:

```
이 AI 글 자연스럽게 윤문해줘:

[ChatGPT / Claude / Gemini 초안 여기에 붙여넣기]
```

아래 표현 중 아무거나 쓰면 스킬이 자동 발동합니다:
- "AI 티 없애줘"
- "GPT 문체 제거해줘"
- "사람이 쓴 것처럼 윤문해줘"
- "번역투 제거"
- "한글 AI 윤문"

**방법 B — 슬래시 커맨드**

```
/im-not-strange-ai-fast [윤문할 텍스트 또는 파일 경로]
```

옵션을 인자 끝에 자연어로 적을 수 있습니다: `장르: 칼럼`, `강도: 적극`, `최소심각도: S1`. 결과가 마음에 안 들면 `/im-not-strange-ai-redo "번역투만 다시"` 같은 식으로 재실행. 두 진입점은 이제 스킬입니다: [`im-not-strange-ai-fast`](.claude/skills/im-not-strange-ai-fast/SKILL.md) · [`im-not-strange-ai-redo`](.claude/skills/im-not-strange-ai-redo/SKILL.md)

**방법 C — Plugin / 마켓플레이스**

`im-not-strange-ai`는 아직 marketplace에 배포하지 않았습니다. 원격 저장소와 배포명을 결정한 뒤 명령을 확정합니다.

스킬 3개 + 서브에이전트 12개가 함께 설치됩니다. 자세한 옵션·스크립트 설치는 [설치](#설치-install) 섹션과 [`INSTALL.md`](INSTALL.md) 참고.

**방법 D — Codex CLI (공식, Fast 모드)**

본체가 이제 Codex CLI Skills를 **공식 지원**합니다. 리포 클론 후 한 줄이면 `~/.codex/skills/`에 연결됩니다:

```bash
cd im-not-strange-ai
./install.sh --codex-only
```

Codex에서 `$im-not-strange-ai`으로 발동합니다(또는 `/skills` 메뉴). Codex는 단일 호출 **Fast 모드**만 제공하며, 정밀 strict 5인 파이프라인은 Claude Code 전용입니다.

### 4. 결과 확인

Claude Code가 입력 길이·옵션에 따라 두 모드 중 하나로 처리합니다.

**Fast 모드 (디폴트, 5,000자 이하 · ~3분)** — `im-not-strange-ai-monolith` 한 콜이 메모리 안에서 탐지·윤문·자체검증을 모두 끝냅니다. 산출물은 `_workspace/{실행날짜-번호}/`에 두 파일:

| 파일 | 내용 |
|------|------|
| `01_input.txt` | 원문 그대로 |
| `final.md` | 윤문본 + 본문 끝 `<!-- IM_NOT_STRANGE_AI_SUMMARY -->` 주석 블록(메트릭·카테고리 탐지 before/after·자체검증 6항·등급·주요 변경 하이라이트). HTML 주석이라 마크다운 뷰어·웹 게시·복사 시 본문에만 노출 |

**Strict 모드 (`--strict` 또는 8,000자+ 자동 승급 · 더 정밀)** — 5인 파이프라인이 단계별 산출물을 분리해 저장합니다:

| 파일 | 내용 |
|------|------|
| `01_input.txt` | 원문 그대로 |
| `02_detection.json` | AI 티 탐지 리포트 (위치·종류·심각도) |
| `03_rewrite.md` | 윤문본 |
| `04_fidelity_audit.json` | 내용 훼손 감사 결과 |
| `05_naturalness_review.json` | 자연도 재측정 결과 |
| `final.md` + `summary.md` | 최종 윤문본 + 점수·주요 변경·등급 요약 |

부분 재실행("이 카테고리만 다시"·"2차 윤문")은 strict 모드로 자동 전환됩니다.

### 5. 결과가 맘에 안 들면

그대로 말씀하시면 됩니다. 재실행·수정 명령을 따로 외울 필요 없습니다:

- **"이 문단만 다시 윤문해줘"** — 해당 구간만 재시도
- **"번역투만 더 손봐줘"** (또는 "관용구만 다시") — 특정 카테고리만 재처리
- **"윤문 강도 낮춰줘"** — 보수적 윤문 (결정적 패턴만 제거)
- **"원문 톤을 더 살려줘"** — 변경률 상한을 낮춰 원문 유지
- **"2차 윤문해줘"** — 현재 결과를 한 번 더 다듬기

### 6. 다른 글로 또 돌리고 싶을 때

Claude Code 세션 안에서 새 글을 붙여넣고 똑같이 부탁하면 됩니다. 실행마다 새 `_workspace/{날짜-번호}/` 폴더가 만들어져 이전 결과와 섞이지 않습니다.

## Do-NOT List (탐지·윤문 대상 제외)

- 수치 · 단위 · 날짜
- 고유명사 · 인명 · 제품명 · 모델명
- 큰따옴표 내부 직접 인용
- 법률 · 규정 조문
- 학술 개념어 (불가피한 경우)

## 웹 서비스 확장 (옵션)

`im-not-strange-ai-web-architect` 에이전트가 Next.js 15 App Router + Vercel Fluid Compute + AI Gateway 기반 웹앱 설계를 담당한다. UX는 4화면(입력 → 탐지 하이라이트 → 좌우 diff → 윤문본 복사). 상세: [`web-service-spec.md`](.claude/skills/im-not-strange-ai/references/web-service-spec.md).


## 현재 버전 — v2.0

이 README는 현재 `im-not-strange-ai`의 동작 기준만 설명합니다. 참고했던 프로젝트의 상세 버전사는 여기 싣지 않습니다.

- **AI 티 분류 본체**: A~J 10대 카테고리로 번역투, 과도한 영어 인용, 구조적 AI 패턴, 관용구, 리듬, 수식, hedging, 접속사, 형식명사, 시각 장식을 탐지합니다.
- **Sunny 7규칙**: `-적`, `의`, `들`, `것`, `있는/있다는`, `있었다`, 어색한 `있다` 패턴을 문장 단위로 점검합니다. 삭제 규칙이 아니라 역할 확인 절차입니다.
- **Fast 모드**: `im-not-strange-ai-monolith`가 탐지, 윤문, 자체검증을 한 번에 처리합니다.
- **Strict 모드**: detector, rewriter, auditor, reviewer를 분리해 긴 글이나 민감한 글을 더 정밀하게 검토합니다.
- **검증 기준**: 의미 불변, 근거 기반 수정, 장르 유지, 과윤문 금지를 통과해야 최종 결과로 인정합니다.

## 라이선스 & 윤리

- **MIT 라이선스** — [`LICENSE`](LICENSE) 참조. 코드·스킬·에이전트 정의·분류 체계 문서를 포함한 본 리포 전체에 적용됩니다. 외부 패키지 통합·fork·상용 활용 모두 허용되며, 저작권 표기와 라이선스 사본을 함께 배포하면 됩니다.
- `im-not-strange-ai`는 `im-not-ai` 기반 fork이므로 원 저작권(`epoko77-ai`)과 수정 저작권(`itssosunny`) 표기를 함께 보존합니다.
- 외부 contribution(PR·Issue 등)은 GitHub 기본 inbound = outbound 원칙에 따라 동일한 MIT 라이선스로 contribution됩니다.
- 본 도구는 "AI 탐지기 우회(Undetectable AI)"가 아니라 **한글 글쓰기 품질 개선**을 목적으로 합니다.
- 학술 제출·저널리즘 진실성 보증 도구가 아닙니다.
- 분류 체계(`ai-tell-taxonomy.md`)는 연구·교육·도구 통합 목적 자유 이용 가능합니다(MIT 범위 내).

## 기여

새로운 AI 티 패턴이나 회귀 사례를 발견했다면 [Issue](https://github.com/itssosunny/im-not-strange-ai/issues)로 보고해 주세요. 실증 사례 2건 이상(가능하면 서로 다른 모델·장르·작가)이 함께면 분류학자 에이전트가 본진([`ai-tell-taxonomy.md`](.claude/skills/im-not-strange-ai/references/ai-tell-taxonomy.md)) 반영 여부를 점검합니다.

다른 형태(외부 회귀 케이스 제공·슬래시 커맨드·Plugin 통합·다국어 확장 등)도 환영합니다. 기여자 명단은 [`CONTRIBUTORS.md`](CONTRIBUTORS.md)를 참고해주세요.

## Contributors

전체 명단과 기여 내역은 [`CONTRIBUTORS.md`](CONTRIBUTORS.md)에 보존합니다.

---

Built with [Claude Code](https://claude.com/claude-code) + https://github.com/revfactory/harness 하네스 아키텍처 기반 프로젝트.
