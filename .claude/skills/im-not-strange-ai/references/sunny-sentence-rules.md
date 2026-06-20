# Sunny Sentence Rules — sentence-level polish supplement

This file distills the unique sentence-polish rules from the local
`im-not-strange-full` reference set into a small supplement for
`im-not-strange-ai`.

It is not a second skill and does not replace `quick-rules.md` or
`rewriting-playbook.md`. Use it only when a sentence feels awkward after the
main AI-tell patterns have been handled.

## Scope

- Preserve meaning, claims, facts, names, numbers, quotation, and register.
- Prefer deletion or simplification over decorative rewriting.
- Apply only to the local span that triggered the rule.
- Do not force a rule when the original sentence already reads naturally.
- Treat rules 1-7 as role checks, not blanket deletion rules. Keep the expression
  when it carries meaning, rhythm, emphasis, technical precision, or genre fit.

## Active Rules 1-7

Use these seven checks before broader sentence polishing. The question is not
"can this word be removed?" but "does this word do a job here?"

| Rule | Target | Keep when | Revise when | Example |
|---|---|---|---|---|
| 1. `-적` | `효율적`, `구조적`, `실질적`처럼 `-적`이 붙은 말 | concept label, field term, contrast, or concise register depends on it | it only makes the phrase abstract or stiff | `효율적인 방식으로 해결했다` -> `효율적으로 해결했다` / keep `구조적 문제` if it is the concept |
| 2. `-의` | possessive or noun-linking `의` | ownership, source, title, fixed term, or ambiguity control depends on it | stacked `의` makes the sentence translated or loose | `서비스의 개선의 방향` -> `서비스 개선 방향` |
| 3. `들` | plural suffix on nouns | real plurality, distribution, contrast, or emphasis matters | the noun is generic and plurality adds nothing | `사용자들의 반응을 봤다` -> `사용자 반응을 봤다` |
| 4. `것` | dependency noun `것` and `것이다` endings | it points to a real object, quoted idea, or needed abstraction | it only delays the predicate or repeats the previous clause | `중요한 것은 실행이다` -> keep / `문제라는 것이다` -> `문제다` |
| 5. `있는/있다는` | modifier forms built on `있다` | presence, possession, ongoing state, or contrast is the point | it only pads a noun phrase | `가능성이 있다는 점` -> `가능성` |
| 6. `있었다` | sentence-final or clause-final `있었다` | it marks a real past existence, location, possession, or state | it trails after a noun/action that already carries the meaning | `변화가 있었다` -> `변했다` / keep `책상 위에 있었다` |
| 7. awkward `있다` patterns | `관계에 있다`, `에게 있어`, `하는 데 있어`, `함에 있어`, `있음에 틀림없다` | the phrase is a fixed institutional or technical expression and simpler wording would distort it | the phrase hides a simpler relation or predicate | `성공에 있어 중요한 요소` -> `성공에 중요한 요소` |

## Fast Application Order

1. Mark candidate spans for rules 1-7.
2. Ask what job each span does: meaning, rhythm, emphasis, precision, or genre.
3. Keep spans that do a real job.
4. Revise only spans that add fog, delay the predicate, or make the sentence
   translated/stiff.
5. Re-read once. If the sentence now sounds plain and accurate, stop.

## Do Not Over-Apply

- Keep `-적`, `-의`, `것`, `있다`, and passive voice when they carry real
  meaning or match the genre.
- Do not flatten every sentence. Some friction is voice, formality, or domain
  precision rather than bad writing.
- Do not turn a formal report into casual prose.
- Do not add examples, metaphors, emotion, or claims that were not present.
- If a change would alter technical meaning, leave the original span unchanged
  and note it in the summary.
