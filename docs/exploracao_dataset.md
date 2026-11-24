# Exploração inicial do dataset Olist

**Projeto:** Gestão e Análise de um E-commerce  
**Disciplina:** Sistemas de Banco de Dados — UFPB  
**Equipe:** Ana Beatriz, Maria Clara e Ayra  
**Etapa:** 1 — Escolha e exploração do dataset  
**Entrega:** 25/11/2026

## 1. Apresentação da base

O conjunto de dados escolhido é o **Brazilian E-Commerce Public Dataset by Olist**, disponibilizado publicamente no Kaggle: <https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce>.

A base reúne informações históricas de pedidos realizados em um marketplace brasileiro, predominantemente no período de 2016 a 2018. Seus arquivos permitem estudar clientes, pedidos, itens vendidos, produtos, vendedores, pagamentos, avaliações e localização geográfica.

O objetivo desta etapa é **conhecer a estrutura, identificar variáveis e ligações entre os arquivos e avaliar inicialmente a qualidade dos dados**. A definição definitiva de tabelas, chaves, cardinalidades e normalização será tratada na segunda entrega.

## 2. Inventário dos arquivos

Os resultados abaixo foram obtidos pela exploração em Python/Pandas dos CSVs originais.

| Arquivo | Registros | Colunas | Conteúdo |
|---|---:|---:|---|
| `olist_customers_dataset.csv` | 99.441 | 5 | Identificação e localização dos clientes |
| `olist_orders_dataset.csv` | 99.441 | 8 | Pedidos, status e datas de processamento/entrega |
| `olist_order_items_dataset.csv` | 112.650 | 7 | Itens, produtos, vendedores, preço e frete |
| `olist_products_dataset.csv` | 32.951 | 9 | Categorias e características dos produtos |
| `olist_sellers_dataset.csv` | 3.095 | 4 | Identificação e localização dos vendedores |
| `olist_order_payments_dataset.csv` | 103.886 | 5 | Tipos, parcelas e valores dos pagamentos |
| `olist_order_reviews_dataset.csv` | 99.224 | 7 | Notas, comentários e datas das avaliações |
| `olist_geolocation_dataset.csv` | 1.000.163 | 5 | Coordenadas e localidades por prefixo de CEP |
| `product_category_name_translation.csv` | 71 | 2 | Tradução dos nomes das categorias |

**Observação:** o volume é apresentado por arquivo; não se deve somar essas linhas para obter o número de pedidos ou consumidores, pois as tabelas representam entidades e granularidades distintas.

## 3. Variáveis relevantes e campos de ligação

| Arquivo | Principais variáveis | Possível ligação |
|---|---|---|
| Clientes | `customer_id`, `customer_unique_id`, `customer_zip_code_prefix`, `customer_city`, `customer_state` | `customer_id` com pedidos; CEP com geolocalização (com cuidados) |
| Pedidos | `order_id`, `customer_id`, `order_status`, datas de compra, aprovação e entrega | `customer_id` com clientes; `order_id` com itens, pagamentos e avaliações |
| Itens de pedidos | `order_id`, `order_item_id`, `product_id`, `seller_id`, `price`, `freight_value`, `shipping_limit_date` | `order_id`, `product_id`, `seller_id` |
| Produtos | `product_id`, `product_category_name`, medidas e peso | `product_id` com itens; `product_category_name` com tradução |
| Vendedores | `seller_id`, `seller_zip_code_prefix`, `seller_city`, `seller_state` | `seller_id` com itens; CEP com geolocalização (com cuidados) |
| Pagamentos | `order_id`, `payment_sequential`, `payment_type`, `payment_installments`, `payment_value` | `order_id` com pedidos |
| Avaliações | `review_id`, `order_id`, `review_score`, títulos, mensagens e datas | `order_id` com pedidos |
| Geolocalização | `geolocation_zip_code_prefix`, `geolocation_lat`, `geolocation_lng`, cidade e estado | Prefixo de CEP com clientes e vendedores |
| Tradução das categorias | `product_category_name`, `product_category_name_english` | `product_category_name` com produtos |

Os campos acima são **ligações potenciais observadas nos arquivos**, ainda não restrições de chave estrangeira implementadas no SGBD.

## 4. Chaves candidatas — verificação inicial

A análise foi realizada contabilizando combinações repetidas e chaves ausentes nos CSVs:

| Arquivo | Chave avaliada | Ausentes | Repetições excedentes | Avaliação |
|---|---|---:|---:|---|
| `olist_customers_dataset.csv` | `customer_id` | 0 | 0 | Candidata inicial |
| `olist_orders_dataset.csv` | `order_id` | 0 | 0 | Candidata inicial |
| `olist_order_items_dataset.csv` | `order_id + order_item_id` | 0 | 0 | Candidata inicial |
| `olist_products_dataset.csv` | `product_id` | 0 | 0 | Candidata inicial |
| `olist_sellers_dataset.csv` | `seller_id` | 0 | 0 | Candidata inicial |
| `olist_order_payments_dataset.csv` | `order_id + payment_sequential` | 0 | 0 | Candidata inicial |
| `olist_order_reviews_dataset.csv` | `review_id` | 0 | 814 | Não é única nessa forma |
| `product_category_name_translation.csv` | `product_category_name` | 0 | 0 | Candidata inicial |

`customer_id` e `customer_unique_id` **não são equivalentes**: o primeiro identifica o registro associado ao pedido, enquanto o segundo permite reconhecer um mesmo consumidor em mais de um registro. Em verificação SQL anterior, foram observados 99.441 `customer_id` distintos e 96.096 `customer_unique_id` distintos.

A coluna `review_id` apresenta **814 repetições excedentes**: por isso, não pode ser assumida isoladamente como chave primária sem investigação e eventual definição de outro identificador ou chave composta. A tabela de geolocalização não foi incluída na validação das chaves candidatas, pois pode haver múltiplas observações do mesmo prefixo de CEP.

## 5. Verificação dos relacionamentos

Para cada ligação avaliada, foram procurados valores de origem sem correspondência no arquivo relacionado.

| Origem e campo | Referência | Sem correspondência | Campo ausente na origem |
|---|---|---:|---:|
| `olist_orders_dataset.csv` · `customer_id` | `olist_customers_dataset.csv` | 0 | 0 |
| `olist_order_items_dataset.csv` · `order_id` | `olist_orders_dataset.csv` | 0 | 0 |
| `olist_order_items_dataset.csv` · `product_id` | `olist_products_dataset.csv` | 0 | 0 |
| `olist_order_items_dataset.csv` · `seller_id` | `olist_sellers_dataset.csv` | 0 | 0 |
| `olist_order_payments_dataset.csv` · `order_id` | `olist_orders_dataset.csv` | 0 | 0 |
| `olist_order_reviews_dataset.csv` · `order_id` | `olist_orders_dataset.csv` | 0 | 0 |
| `olist_products_dataset.csv` · `product_category_name` | `product_category_name_translation.csv` | 13 | 610 |

As seis ligações de **pedidos, clientes, itens, produtos, vendedores, pagamentos e avaliações** testadas por identificadores apresentaram zero registros sem correspondência nas respectivas tabelas de referência. Isso é um resultado de verificação de valores, **não** prova de que já existem restrições de integridade referencial criadas no PostgreSQL.

Na tradução de categorias, foram encontrados **13 produtos com categoria preenchida sem correspondente** na tabela de tradução e **610 produtos sem categoria informada**. Essas duas situações devem ser tratadas separadamente.

**Atenção à geolocalização:** o prefixo do CEP pode se repetir no arquivo de coordenadas. Uma junção direta sem agregação ou regra de seleção pode multiplicar linhas. A validade desses relacionamentos geográficos ainda precisa ser avaliada para a futura modelagem.

## 6. Qualidade inicial dos dados

### 6.1. Valores ausentes e linhas exatamente duplicadas

| Arquivo | Células ausentes | Duplicatas exatas |
|---|---:|---:|
| `olist_customers_dataset.csv` | 0 | 0 |
| `olist_orders_dataset.csv` | 4.908 | 0 |
| `olist_order_items_dataset.csv` | 0 | 0 |
| `olist_products_dataset.csv` | 2.448 | 0 |
| `olist_sellers_dataset.csv` | 0 | 0 |
| `olist_order_payments_dataset.csv` | 0 | 0 |
| `olist_order_reviews_dataset.csv` | 145.932 | 0 |
| `olist_geolocation_dataset.csv` | 0 | Não aferido |
| `product_category_name_translation.csv` | 0 | 0 |

A contagem de **células ausentes não é o mesmo que a contagem de registros incompletos**: um registro pode ter mais de uma coluna vazia. Além disso, duplicata exata de linha é diferente de identificador repetido.

### 6.2. Campos com ausência relevantes

| Arquivo | Campo | Ausentes | Percentual |
|---|---|---:|---:|
| `olist_orders_dataset.csv` | `order_approved_at` | 160 | 0.16% |
| `olist_orders_dataset.csv` | `order_delivered_carrier_date` | 1.783 | 1.79% |
| `olist_orders_dataset.csv` | `order_delivered_customer_date` | 2.965 | 2.98% |
| `olist_products_dataset.csv` | `product_category_name` | 610 | 1.85% |
| `olist_products_dataset.csv` | `product_name_lenght` | 610 | 1.85% |
| `olist_products_dataset.csv` | `product_description_lenght` | 610 | 1.85% |
| `olist_products_dataset.csv` | `product_photos_qty` | 610 | 1.85% |
| `olist_products_dataset.csv` | `product_weight_g` | 2 | 0.01% |
| `olist_products_dataset.csv` | `product_length_cm` | 2 | 0.01% |
| `olist_products_dataset.csv` | `product_height_cm` | 2 | 0.01% |
| `olist_products_dataset.csv` | `product_width_cm` | 2 | 0.01% |
| `olist_order_reviews_dataset.csv` | `review_comment_title` | 87.658 | 88.34% |
| `olist_order_reviews_dataset.csv` | `review_comment_message` | 58.274 | 58.73% |

As ausências em datas de envio e entrega podem corresponder a pedidos que não chegaram a essas etapas, mas isso precisará ser verificado usando o status do pedido. Nas avaliações, os textos de título e mensagem são opcionais, de modo que sua ausência não deve ser tratada automaticamente como falha.

A tabela de clientes não apresentou valores nulos nem campos vazios nos testes realizados. Na verificação SQL inicial, todos os prefixos de CEP importados tinham cinco caracteres, mas **o comprimento, isoladamente, não confirma fidelidade ao CSV original**; por isso, é recomendável preservar CEPs como texto e comparar algumas amostras com a fonte.

A análise de duplicatas exatas da tabela de geolocalização não foi concluída no relatório exportado, portanto não atribuímos resultado zero a ela.

## 7. Possibilidades de análise para as próximas etapas

- **Comercial:** categorias com maior receita, faturamento por vendedor, ticket médio, distribuição por estado e tipos de pagamento.
- **Logística:** duração da entrega e comparação entre data efetiva e data prevista, por vendedor ou região.
- **Satisfação:** notas atribuídas pelos compradores e comparação das avaliações com atrasos de entrega.

Para consultas financeiras será necessário distinguir o valor dos itens (`price`), o frete (`freight_value`) e o valor de pagamentos (`payment_value`), pois essas métricas têm significados e granularidades diferentes.

## 8. Conclusão da exploração

A base Olist mostrou-se apropriada ao projeto de Sistemas de Banco de Dados porque contém diversos arquivos relacionados por identificadores, atributos comerciais, logísticos e de avaliação e um volume significativo de registros. Os dados possibilitam a criação futura de um modelo relacional com pelo menos cinco tabelas, consultas SQL e uma aplicação de operações CRUD.

Nesta etapa foram inventariados os arquivos, identificadas as variáveis, avaliadas chaves candidatas e verificadas relações e ausências. Permanecem como cuidados: as repetições de `review_id`, as lacunas na tradução de categorias, a multiplicidade dos registros de geolocalização e a interpretação de dados opcionais ou de pedidos ainda não entregues.

**Decisão preliminar:** dataset adequado, **com limitações conhecidas**. A modelagem física e a normalização ficam para as próximas etapas.

## 9. Reprodutibilidade e arquivos de apoio

- Dataset: <https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce>
- Repositório: <https://github.com/anabiasena/gestao-e-analise-ecommerce>
- Dados locais: `data/raw/`
- Notebook da exploração: `notebooks/Exploracao_Inicial_Olist_Etapa1.ipynb`
- Saídas produzidas pelo notebook: `inventario.csv`, `dicionario_variaveis.csv`, `qualidade_arquivos.csv`, `qualidade_colunas.csv`, `chaves_candidatas.csv` e `relacionamentos.csv`, geradas em `docs/resultados_etapa1/`.

> **Nota de escopo:** este documento registra resultados de exploração. Não constitui ainda um diagrama entidade-relacionamento definitivo nem substitui o relatório final da disciplina.
