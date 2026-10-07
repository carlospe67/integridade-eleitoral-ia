-- Consulta exploratoria: executar somente depois de confirmar o nome BigQuery da tabela.
-- Nao baixar a tabela completa de 76,30 GB.
-- Substituir `PROJECT.DATASET.TABLE` pelo identificador publicado pela Base dos Dados.

SELECT
  tipo_eleicao,
  turno,
  COUNT(*) AS quantidade_linhas
FROM `basedosdados.br_tse_eleicoes.resultados_candidato_secao`
WHERE ano = 2026
  AND sigla_uf = 'RJ'
  AND id_municipio IN ('3303302', '3304904')
GROUP BY tipo_eleicao, turno
ORDER BY tipo_eleicao, turno;

SELECT
  ano,
  turno,
  tipo_eleicao,
  sigla_uf,
  id_municipio,
  id_municipio_tse,
  zona,
  secao,
  numero_candidato,
  votos
FROM `basedosdados.br_tse_eleicoes.resultados_candidato_secao`
WHERE ano = 2026
  AND sigla_uf = 'RJ'
  AND id_municipio IN ('3303302', '3304904')
  -- AND tipo_eleicao = 'presidente'
ORDER BY id_municipio, zona, secao, numero_candidato;
