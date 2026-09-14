# Handoff — contrato para a próxima sessão

**Branch:** `main`. **HEAD:** ver `git log -1`.
**Suítes no HEAD:** `python3 -m unittest discover -s tests -t tests` → 526 OK.
`cd assets/starters/canvas-arcade && npm test` → 516 OK.

Inspecione o working tree **antes** de confiar neste texto. Se algo aqui
estiver velho, corrija aqui — este arquivo é o contrato, e um contrato
desatualizado orienta a sessão seguinte a repetir o que já foi encerrado.

O histórico de versões fica em [`adoption.md`](adoption.md). Não duplique
aquela tabela aqui.

---

## Objetivo

Criar jogos com IA deve ser **fácil**, e o resultado deve alcançar qualidade
**AAA**, com honestidade epistêmica: não prometer o que o harness não verifica.

O piso do starter continua **protótipo**, porque só `release` está em
`prototype`. Não redefina sucesso pelo que já passou nos testes.

---

## Invariantes — não violar

- Nenhum comando observa, joga, ouve, sente ou mede o jogo no dispositivo.
- Nunca emitir `verified` como status. `verify --proves` → `claimed`.
- `granted`, `validated`, `observed`, `heard`, `approved`, `felt`, `trusted`,
  `measured`, `consistent`, `enough`, `shipped`, `elsewhere` e `outsider`
  são sempre `false` nos leitores correspondentes.
- Não importar limiares (16 ms, 100 ms, 4,5:1, 93%, "cinco usuários", draw
  calls, −14 LUFS) como critério ou aprovação.
- Relatórios (`peak`, `mix`, `budget`, `contrast`, `probe`, `size`, `session`)
  não afirmam aprovação no stdout. Os testes do starter recusam `aprovado`,
  `verified`, `LUFS` e a razão de contraste `4.5:1`. **Ancore o padrão à
  unidade**: um `-14` solto casava com toda data de dia 14 e derrubava a suíte
  uma vez por mês.
- Não promover degraus sem a observação que o critério pede. `release` não
  sobe sem outra máquina.
- Não implementar should-meet de Cooper.
- Após `init` ou `start`, `next` exige `playable.unplayed` primeiro, enquanto
  não houver `note`.

---

## Barra vigente do starter

Piso percebido = **mínimo**. O `bar` nomeia o mínimo que a barra já declara.

| Dimensão | Degrau |
| --- | --- |
| feel | playable |
| legibility | playable |
| performance | playable |
| art_direction | slice |
| audio_mix | slice |
| pacing | slice |
| state_trust | slice |
| accessibility | slice |
| content_scale | shippable |
| release | **prototype** |

A lacuna de cada dimensão sai de `game.py bar <projeto>`, que lê o disco. Não
mantenha aqui uma lista paralela: ela envelhece e incha.

---

## O gate anti-slop

`scripts/slop_gate.py` recusa o crescimento auto-referente — texto que só
confirma texto. O baseline (`scripts/slop_baseline.json`) é um **cliquet**: as
métricas só descem. Subir exige editar o JSON no mesmo PR, onde aparece no
diff.

| métrica | o que mede |
| --- | --- |
| `phrase_assertions` | asserções que confirmam que uma frase aparece |
| `adoption_sections` | seções de versão em `adoption.md` |
| `adoption_one_word_lines` | linhas de uma palavra (texto sem reflow) |
| `formula_phrases` | frases-molde em `scripts/` |
| `skill_entry_lines` | tamanho da entrada da skill (teto fixo) |

Quando `adoption.md` cresce em saldo, o PR precisa de um **registro de
execução**: um recibo `.json` com `schema_version` e `recorded_at`, ou um
`docs/stories/<AAAA-MM-DD>-<assunto>.md` com corpo.

---

## O critério de aceite

**Toda melhoria precisa de um recorte jogável como prova**: criar um vertical
slice, alterar uma mecânica existente, ou retomar um projeto com continuidade
correta. Documentação e testes, sozinhos, não atendem ao objetivo.

O PR #6 foi fechado sem merge por violar isto: 2.091 de 2.204 funções novas
seguiam três moldes, e 6.946 asserções confirmavam frases. Ver a justificativa
no próprio PR.

---

## O que NÃO fazer

- Não acrescentar uma função, um teste e uma entrada de versão por palavra
  recusada. Foi o ciclo que produziu o #6.
- Não escrever "a família X está saturada" e procurar a próxima família. Esse
  registro é o motor do ciclo, não a memória dele.
- Não medir progresso por contagem de testes ou de versões.
- Não casar nome onde é preciso verificar a propriedade. Três defeitos reais
  vieram daí: o `-14` da data, `PERSIST_VERSION` cego a `schemaVersion`, e a
  checagem de evidência que aceitava qualquer arquivo tocado.

---

## O que está aberto

1. **287 frases-molde em `scripts/`** e **476 seções** em `adoption.md`.
   Consolidar em poucos contratos claros, com a suíte como rede.
2. **Curadoria dos packs.** A frase de abertura do starter está repetida nos
   23 gêneros. Falta delimitar versões contempladas, data de revisão e limites
   conhecidos. Comece pelos packs que o estúdio usa.
3. **Carregamento sob demanda dos packs.** Hoje são 41 arquivos e ~110 KB; a
   prioridade é selecionar o pertinente, não transportar.
4. **Gênero não é inferido.** `context` seleciona plataforma e escala sozinho,
   mas o gênero exige `--genre`.

---

## Como retomar

```sh
git -C <repo> checkout main && git pull
python3 -m unittest discover -s tests -t tests
cd assets/starters/canvas-arcade && npm test
python3 scripts/slop_gate.py
```

Um salto por vez, commit descritivo, e a prova de execução junto.
