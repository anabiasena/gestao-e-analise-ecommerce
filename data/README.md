# Dados

Este diretório reúne as orientações para obter e organizar os dados utilizados no projeto **Gestão e Análise de E-commerce**.

Os arquivos CSV originais são mantidos localmente e **não são versionados no GitHub**. Assim, todas as integrantes do grupo podem trabalhar com o mesmo conjunto de dados sem adicionar arquivos pesados ao repositório.

## 1. Baixar o conjunto de dados

1. Acesse o [Brazilian E-Commerce Public Dataset by Olist no Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
2. Entre na sua conta do Kaggle.
3. Clique em **Download** para baixar o arquivo compactado.
4. Extraia o conteúdo do arquivo ZIP.

## 2. Preparar a pasta do projeto

Se você ainda não clonou o repositório, execute no terminal:

```bash
git clone https://github.com/anabiasena/gestao-e-analise-ecommerce.git
cd gestao-e-analise-ecommerce
```

Dentro da pasta do projeto, crie a pasta destinada aos dados brutos:

```bash
mkdir -p data/raw
```

Mova ou copie os arquivos CSV extraídos do Kaggle para dentro de `data/raw/`.

A estrutura local deverá ficar semelhante a esta:

```text
gestao-e-analise-ecommerce/
└── data/
    ├── README.md
    └── raw/
        ├── olist_customers_dataset.csv
        ├── olist_orders_dataset.csv
        ├── olist_order_items_dataset.csv
        ├── olist_products_dataset.csv
        ├── olist_sellers_dataset.csv
        ├── olist_order_payments_dataset.csv
        ├── olist_order_reviews_dataset.csv
        ├── olist_geolocation_dataset.csv
        └── product_category_name_translation.csv
```

**Atenção:** os nomes acima representam os arquivos esperados. Confira os nomes e a quantidade de arquivos na versão efetivamente baixada.

## 3. Conferir se os arquivos estão no lugar certo

No terminal, já dentro da pasta principal do projeto, execute:

```bash
ls data/raw
```

O terminal deverá listar os arquivos CSV que você colocou na pasta.

## 4. Por que os CSVs não aparecem no GitHub?

A pasta `data/raw/` e os arquivos brutos são ignorados pelo Git por meio do arquivo `.gitignore`. Isso evita enviar os dados originais ao repositório e mantém o projeto mais leve.

Por esse motivo, quando outra integrante clonar o repositório, ela receberá este README, mas precisará baixar o conjunto de dados no Kaggle e repetir as etapas acima para ter os CSVs no próprio computador.

Não remova a regra de `data/raw/` do `.gitignore` nem faça commit dos arquivos CSV originais.

## 5. Fonte dos dados

OLIST. **Brazilian E-Commerce Public Dataset**. Kaggle. Disponível em: [https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Acesso em: 2026.
