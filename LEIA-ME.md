# Site multilíngue Need for Speed

Site estático com detecção automática de idioma e roteamento de loja por país.
Português, inglês e espanhol. Pronto para Cloudflare Pages.

## Estrutura

```
dist/
  index.html      raiz, detecta o idioma e redireciona. É o x-default do hreflang.
  pt/index.html   página completa em português
  en/index.html   página completa em inglês
  es/index.html   página completa em espanhol
data.py           todo o texto e os dados dos 25 jogos
build.py          gerador. python3 build.py refaz o dist inteiro
```

Cada idioma é um arquivo HTML de verdade, com o texto já dentro dele. Não é troca por
JavaScript. Isso é o que permite ao Google indexar as três versões separadamente e
mostrar a certa para cada busca.

## Três coisas para trocar antes de publicar

1. **Domínio.** Em `build.py`, a variável `BASE` está como `https://SEU-DOMINIO.com`.
   Troque pelo domínio real e rode `python3 build.py` de novo. Ela alimenta o
   `canonical`, o `hreflang` e as tags Open Graph, e todas precisam de URL absoluta.

2. **Códigos de afiliado.** Em `data.py`, no dicionário `STORES`, os campos `tag` estão
   como `TAG_BR`, `TAG_US` e assim por diante. Cada país da Amazon é um programa
   separado, com cadastro e código próprios. Link do Brasil não paga comissão de venda
   feita nos Estados Unidos.

3. **A imagem `og.jpg`.** Copie para dentro de `dist/`, na raiz. É a mesma que você já
   tem, 1200x630. Sem ela o preview de WhatsApp fica sem imagem.

## Como funciona a detecção

**Idioma.** A raiz lê `navigator.languages`, que é a lista que a pessoa configurou no
próprio sistema, e manda para a pasta correspondente. Se não houver tradução para o
idioma dela, cai no inglês. Quando a pessoa troca no seletor do topo, a escolha fica
gravada e passa a vencer a detecção nas próximas visitas.

Robôs que não executam JavaScript recebem a lista de idiomas em HTML na raiz, com
`hreflang`, e indexam cada versão separadamente. É por isso que a raiz tem conteúdo de
verdade e não só um redirecionamento.

**País.** É um eixo separado do idioma, porque um mexicano e um espanhol leem a mesma
página mas compram em lojas diferentes. O país sai da região do idioma do navegador
(`es-MX` vira MX), com seletor visível ao lado para corrigir. A preferência também fica
gravada.

Se quiser o país real em vez do presumido, o Cloudflare entrega isso no cabeçalho
`CF-IPCountry`, mas precisa de uma Pages Function. Do jeito atual não depende de
serviço externo nem adiciona latência.

## Publicar no Cloudflare Pages

1. Painel do Cloudflare, Workers & Pages, Create, Pages, Upload assets.
2. Arraste a pasta `dist`.
3. Custom domains, adicione o seu domínio. HTTPS é automático.

Se o domínio já estiver no Cloudflare, o DNS se resolve sozinho. Se estiver em outro
registrador, o painel mostra os nameservers para apontar.

## Acrescentar um quarto idioma

Em `data.py`:

1. Acrescente o código em `LANGS` e em `HTML_LANG`.
2. Copie um bloco de `UI` e traduza.
3. Acrescente a chave em `LANG_NAME` e em `LANG_COUNTRY`.
4. Acrescente a chave em cada `hook` dos 25 jogos, e em cada era.

Rode `python3 build.py`. O `hreflang`, o seletor e a detecção passam a incluir o novo
idioma sozinhos, sem tocar em mais nada.

## Observações

As artes dos quadros são composições originais em CSS, não capas oficiais. Foi uma
escolha deliberada: página com link de afiliado é uso comercial, e capa de jogo é obra
protegida. Se quiser imagem real de produto, o caminho limpo é puxar pela API do próprio
programa de afiliados, que fornece a imagem licenciada para esse uso.

O aviso de link patrocinado no rodapé não é enfeite. A maioria dos programas cancela a
conta quando ele não aparece, e em vários países é exigência legal. Os botões já saem
com `rel="nofollow sponsored"`.
