# ZeConfig [EN](README.md)   -   [BR](README_BR.md)
[![Buid](https://github.com/uadson/ZeConfig/actions/workflows/zconf-build.yml/badge.svg)](https://github.com/uadson/ZeConfig/actions/workflows/zconf-build.yml)
[![Tests](https://github.com/uadson/ZeConfig/actions/workflows/zconf-tests.yml/badge.svg)](https://github.com/uadson/ZeConfig/actions/workflows/zconf-tests.yml)
[![Release](https://github.com/uadson/zeconfig/actions/workflows/release.yml/badge.svg)](https://github.com/uadson/zeconfig/actions/workflows/release.yml)

ZeConfig é uma biblioteca Python projetada para gerenciar configurações de aplicativos, facilitando o manuseio de dados confidenciais e configurações específicas do ambiente. Ela oferece suporte a arquivos de configuração nos formatos TOM, JSON, YAML, YML e ENV.

## Recursos

- Detecção automática do local do arquivo de configuração dentro do diretório atual ou seus subdiretórios.
- Suporte para arquivos de configuração TOML, JSON, YAML, YML e ENV.
- Fácil acesso a chaves e valores específicos do ambiente.

## Instalação

```bash
pip install zeconfig
```

## Uso

### 0. Criando um arquivo de configuração
Na raiz do projeto, crie um arquivo com uma das extensões .toml, .json, .yaml, .yml ou .env.

Por exemplo: config.json

### 1. Formato do arquivo de configuração

### Exemplo `config.json`

```json
{
    "DATABASE_URL":  "sqlite:///dev.db",
    "SECRET_KEY": "dev-secret"
}
```

### 2. Inicializar ZeConfig

```python
from ze import config
```

### 3. Gerenciar configurações de ambiente

Retrieve a value for a specific key in the current environment:

```python
DATABASE_URL = config("DATABASE_URL")
print(f"Database URL: {DATABASE_URL}")

>>> OUTPUT: 
    sqlite:///dev.db
```

## Tratamento de erros

ZeConfig gera exceções descritivas para problemas comuns:


- `KeyError`: Ambiente ou chave ausente no arquivo de configuração.

## Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contribuindo

Contribuições são bem-vindas! Abra um problema ou envie uma solicitação de pull no [repositório GitHub](https://github.com/uadson/zeconfig).

## Contato

Para perguntas ou suporte, entre em contato com [uadsonpy@gmail.com](mailto:uadsonpy@gmail.com).
