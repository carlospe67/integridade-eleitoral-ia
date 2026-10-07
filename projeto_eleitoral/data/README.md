# Dados

- `raw/`: arquivos originais autorizados, sem edição manual.
- `processed/`: dados padronizados e derivados.
- Dados pessoais, credenciais e tokens não devem ser armazenados nesta pasta.
- O primeiro experimento usa dados sintéticos gerados por `src/synthetic_pipeline.py`.

## Política de armazenamento

Para bases eleitorais grandes, prefira Google Drive, Google Cloud Storage ou outro repositório autorizado. Use `raw/` localmente apenas para amostras pequenas, testes e arquivos temporários.

Antes de processar uma base remota, registre:

- fonte oficial e URL de obtenção;
- eleição, abrangência geográfica e nível de agregação;
- data de download, tamanho e checksum;
- formato e esquema das colunas;
- licença, termos de uso e eventuais restrições.

O Colab pode montar o Drive e executar os notebooks sem copiar a base inteira para o disco local. Tokens, cookies, chaves de API e arquivos pessoais ficam fora deste diretório.
