# Progresso da traducao de The Ruins Of The Lost Kingdom

Este arquivo e um resumo para continuar o trabalho em outro chat/modelo. O objetivo do usuario e traduzir para portugues brasileiro a interface e os textos que aparecem durante o jogo. Ele autorizou usar ingles quando o portugues nao couber e uma abreviacao puder prejudicar o jogo.

## Pasta de trabalho

- Raiz: `C:\Users\S3ppi\Documents\ChatGPT\tradução ROL`
- Jogo traduzido: `game\rol\`
- Arquivos do jogo: `game\rol\cr\`
- Launcher: `game\rol\Iniciar ROL PT-BR.bat` (abre `rol.exe` nessa mesma pasta)
- Cópia preparada para distribuição: `patch_ptbr\cr\`
- Wiki offline de referência dada pelo usuário: `reference_rol_gpt\RoL_Wiki_Offline_PTBR\`

O usuário já abriu a versão anterior do jogo. Depois disso, reportou que ainda via japonês nos itens; agora especificou baús, alguns itens, nomes de lugares e mapa. A rodada mais recente atualizou `a.cr`, mas ainda não foi conferida visualmente dentro do jogo. Se for necessário testar, abrir pelo launcher acima e observar especificamente o mapa, baús, inventário e nomes de área.

## O que já foi traduzido

1. `a.cr` — menus, opções e mensagens gerais, incluindo os rótulos de menu que o usuário mostrou em capturas; 24 campos de menu comprimidos e cerca de 43 outros textos de interface já tinham sido tratados em rodadas anteriores.
2. `a.cr` — 285 ocorrências de nomes de itens/equipamentos (209 nomes japoneses distintos), incluindo armas, anéis, armaduras e consumíveis. Mapeamento: `patch_ptbr\mapeamento_itens_armas.csv`.
3. `a.cr` — 441 campos de nomes de habilidades/passivas/ataques identificados em referências. Foram usados PT-BR, inglês e nomes curtos conforme o limite. Mapeamentos: `patch_ptbr\mapeamento_habilidades_a.csv` e `patch_ptbr\mapeamento_habilidades_restantes.csv`.
4. `a.cr` — nesta rodada foram traduzidos mais 1.095 campos de exploração, correspondendo a 104 pares distintos de texto original/tradução. Incluem nomes de lugares e andares, nomes e descrições de mapas, controles do minimapa, chaves/passes de acesso e mensagens de baús. Auditoria: `patch_ptbr\mapeamento_mapa_baus.csv`.
   - Exemplos: `Harlene Castle 2F`, `Ivarie Tower 2F`, `Tandridge Crypt 1F`, `Unfeed Prison B1`, `Sejenm Temple 3F`, `Raintage Hall`, `Crypt Map`, `Minimap Mode`, `%d chests nearby`, `Chest found`, `No chest here`.
5. `b.cr` — 82 textos da versão de referência do usuário, aplicados previamente.
6. `c.cr` — 263 nomes de ataques/habilidades da versão de referência, aplicados previamente.

## Como a tradução foi implementada

Os arquivos `.cr` usam registros compactados com zlib. Em `a.cr`, cada registro começa em um bloco zlib; um inteiro little-endian de 4 bytes imediatamente antes do zlib informa o tamanho compactado. O conteúdo descompactado contém campos com comprimento little-endian e texto CP932 (japonês), normalmente terminado por NUL.

A rotina de patch procura campos completos e conhecidos, não substitui sequências japonesas arbitrárias no arquivo. Para cada campo, usa a tradução em ASCII/inglês se ela couber no espaço original em bytes, atualiza o comprimento do campo e preenche o restante com NUL. Depois recompõe o registro tentando níveis zlib 1, 6 e 9. Só grava se o bloco recomposto não ultrapassar o tamanho compactado original; bytes de preenchimento preservam o tamanho do bloco e os offsets do restante do arquivo. Campos longos ou traduções que não couberam foram deixados intactos.

Essa abordagem foi validada estaticamente: todos os 1.095 textos da auditoria de mapa/baús aparecem nos campos registrados, os 15.150 blocos zlib reconhecidos continuam descompactáveis, `a.cr` mantém 2.676.130 bytes e é idêntico à cópia em `patch_ptbr\cr\a.cr`. Isso não substitui a conferência visual no jogo.

A wiki offline é a referência principal para nomes e contexto. Use os rótulos de páginas relevantes, sem assumir que rótulos globais da wiki sempre identificam corretamente um texto. Inglês curto é preferível a cortar palavras aleatoriamente.

## Estado atual e trabalho que falta

- A tradução ainda é parcial. O usuário confirmou que ainda encontra japonês em interface, baús, itens, lugares e mapa.
- A auditoria mais recente registrou 1.095 campos aplicados; 72 candidatos não foram alterados por limite de bytes ou por o bloco zlib não aceitar a tradução dentro do tamanho original. O CSV atual registra os aplicados, mas não preserva uma lista confiável dos 72 rejeitados; refaça a extração a partir do backup antes de tentar completá-los.
- Nos dois mapeamentos de habilidades ainda constam 15 ocorrências sem substituição: 13 no mapeamento inicial e 2 no complementar.
- Descrições longas, textos de ajuda, diálogo e nomes adicionais de itens ainda podem estar em japonês. Não afirmar que o jogo inteiro foi traduzido.
- Um scan de strings CP932 encontrou muitos fragmentos em `a.cr`; eles incluem campos técnicos, descrições, nomes de personagem/local e fragmentos de dados. Traduzir somente quando o campo e o contexto forem identificados.
- Um scan zlib preliminar de `map.cr`, `b.cr`, `c.cr`, `d.cr` e `eft.cr` não encontrou um conjunto grande de textos legíveis; isso não prova que todos esses arquivos estejam traduzidos. Assets e executáveis ainda não foram auditados completamente.
- Revisar com prioridade os itens que o usuário ainda vê em japonês e os lugares/legendas que restarem após abrir esta versão. Se persistirem muitos textos, pedir captura de tela do campo específico e rastrear o respectivo registro antes de editar.

## Arquivos importantes e backups

- Arquivo ativo principal: `game\rol\cr\a.cr`
- Cópia da tradução: `patch_ptbr\cr\a.cr`
- Backup imediatamente anterior à tradução de mapa/baús: `game\rol\cr\a.cr.codex-before-map-chests.bak`
- Backups anteriores também existem como `a.cr.codex-original.bak`, `a.cr.codex-before-menu-patch.bak`, `a.cr.codex-before-items-patch.bak` e `a.cr.codex-before-rest-names.bak`.
- `b.cr.codex-original.bak` e `c.cr.codex-original.bak` preservam os originais correspondentes.
- `patch_ptbr\LEIA-ME_PTBR.txt` descreve o pacote; atualizar se houver nova rodada.

## Próximo passo sugerido

1. Confirmar no jogo, usando `Iniciar ROL PT-BR.bat`, se os nomes de lugares, mapas, baús e chaves agora aparecem em inglês/português.
2. Anotar os textos que continuam japoneses, especialmente nomes de itens no inventário e rótulos dentro do mapa.
3. Localizar esses textos como campos CP932 completos em `a.cr` ou no arquivo correspondente, conferir seu contexto e capacidade de bytes, traduzir, auditar os offsets e atualizar a cópia em `patch_ptbr\cr`.
4. Não substituir blocos nem alterar a quantidade de bytes do arquivo sem entender o contêiner; manter backup e relatório de cada alteração.

## Rodada 3 (Claude) - correcoes e traducao em massa do a.cr

Feito:
1. **Bug corrigido**: 43 blocos "stored" do `a.cr` (mensagens de bau selado, selecao de nucleo de monstro etc.) tinham sido traduzidos sem atualizar o checksum Adler-32, entao o zlib os recusava ("incorrect data check"). O total real de blocos e **15.193** (nao 15.150). Todos os 15.193 agora descompactam e tem o mesmo tamanho descompactado do original.
2. **1.944 textos** traduzidos no `a.cr` (campos com prefixo de tamanho u32 + NUL, inclui constantes de strings dentro do bytecode Lua): nomes em katakana (equipamentos em ingles, nomes de personagens em romaji), descricoes de itens/classes/skills/passivas, nomes de lugares, titulos de cacadores, quests, strings de UI (formato printf preservado), tutorial de edicao de IA, mensagens de rede/erro, materiais. Lista completa em `patch_ptbr/mapeamento_rodada3_a.csv`.
3. `c.cr`: 8 nomes de missoes (`<msml name=...>`) traduzidos, com preenchimento por espacos.
4. Convencao: o prefixo de tamanho do campo e mantido, o texto vai em ASCII (sem acentos) e o resto e preenchido com NUL; blocos recomprimidos (zlib 9/6/1/0, depois zopfli) e preenchidos com NUL ate o tamanho original. Quando um bloco nao cabia, usa-se versao mais curta (`tools/rodada3/tr/fallback.py`).
5. Scripts em `tools/rodada3/` (caminhos fixos em /home/claude/rt/work: ajuste ao reutilizar). `tr/*.py` guarda as traducoes por indice de `todo.json`.

NAO tocado (de proposito):
- `name="..."` em UTF-8 dos XML de mapa (`a.cr`, 1.622 ocorrencias, ex.: `魔人：剣士I`, `塔タル`) e dos XML de IA de inimigos (`c.cr`, `act1 name="ひっかき"`): sao identificadores usados por scripts; traduzir pode quebrar o jogo.
- `map.cr`, `d.cr`, `eft.cr`, `enm.cr`, `hro.cr`, `b.cr`, `se.cr`: sem texto japones legivel encontrado.
- Executaveis (`rol.exe`, `setting.exe`) nao foram auditados.

Pendente / riscos:
- NADA disso foi testado dentro do jogo ainda. Strings de bytecode Lua foram preenchidas com NUL: se algum script comparar strings entre si, pode haver quebra. Se algo falhar, reverter com os backups `.bak` ou `git checkout`.
- Abreviacoes: varios nomes curtos (itens-chave, materiais, titulos) tem poucos bytes; ver `mapeamento_rodada3_a.csv`.
- Aumentar limites exigiria entender o indice (TOC) do container.

## Rodada 3b/3c - correcao apos testes no jogo (LEIA ANTES DE QUALQUER PATCH)

Estado: `a.cr` atual (K1) RODA no jogo (confirmado pelo usuario) com ~3250 blocos traduzidos; cabecalhos `tbl` INTACTOS; nenhum campo com tamanho alterado. ~94 blocos ainda em japones (nao couberam). `c.cr` original (nomes de missao em japones, sem teste).

Regras aprendidas (por bisecao com testes do usuario):
1. NUNCA altere o prefixo de tamanho (u32) de um campo de texto. Mantenha L original; escreva texto ASCII + espacos (ou NUL) ate L-1, mais 1 NUL final. Traducoes antigas (Codex) encurtavam L e deixavam NULs extras: isso desalinha o resto do registro e causa "Initialization failure", crash depois da intro ou erro de save.
2. NAO zere os cabecalhos `tbl\0\x01` entre blocos (conclusao errada anterior: zerar so mascarava o problema da regra 1 e quebrava o menu).
3. Cada bloco recomprimido com tamanho EXATO igual ao original (tools/rodada3b/fixL.py, exact2.py, exact4.py: varia nivel/estrategia, flushes parciais e blocos vazios ate o tamanho bater). Nao escreva nada alem do fim do stream.
4. Quando o texto nao cabe no tamanho exato: abreviar/ingles (variantes em fixL.py) ou manter o japones.
5. Saves antigos podem guardar nomes em japones; se um save der erro depois de traduzir nomes de itens/habilidades, testar com save novo.
6. Metodo de teste: usuario copia a.cr para rol\cr e abre; classificar resultado (A: nao abre, B: cai depois da intro, C: chega ao menu).
