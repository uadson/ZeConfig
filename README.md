# ZeConfig

ZeConfig é uma classe de gerenciador de configurações para aplicações Python. Este pacote foi criado para simplificar o acesso a dados de configuração sensíveis, como credenciais de banco de dados e informações de configuração que precisam ser lidas de forma segura e estruturada. ZeConfig suporta arquivos de configuração nos formatos **TOML** e **JSON**.

## Recursos

- **Leitura de arquivos TOML e JSON**: Identifica automaticamente o formato do arquivo de configuração e o carrega conforme necessário.
- **Acesso facilitado a dados sensíveis**: Centraliza e estrutura as informações de configuração da aplicação.
- **Interface simples**: Métodos intuitivos para acessar e manipular as configurações.

## Instalação

Para usar o ZeConfig, você pode copiar o código diretamente para seu projeto ou instalá-lo a partir do PyPI, quando disponível:

```bash
pip install zeconfig
```
ou

```bash
poetry add zeconfig
```

## Uso
Exemplo básico de uso da classe ZeConfig:

```bash
    from zeconfig import ZeConfig

    # Inicializa o gerenciador de configurações com o caminho para o arquivo
    zconf = ZeConfig("config.toml")

    # Carrega as configurações do arquivo
    config = zconf.config()

    # Exibe as configurações
    print(config)
```

## Estrutura da Classe
### ZeConfig

A classe principal do pacote, responsável por:

    Identificar o formato do arquivo de configuração com base em sua extensão.
    Carregar dados de arquivos JSON e TOML.
    Retornar as configurações de maneira estruturada.

Principais Métodos

    config(): Carrega e retorna o conteúdo do arquivo de configuração.
    get_file_extension(): Retorna a extensão do arquivo de configuração.
    file_reader(): Lê e retorna os dados do arquivo de configuração, lançando um erro caso o tipo de arquivo não seja suportado.

Formatos de Arquivo Suportados

ZeConfig oferece suporte para arquivos nos seguintes formatos:

    TOML (.toml)
    JSON (.json)

## Exemplo de Configuração

Exemplo de arquivo config.toml:

```bash
    [database]
    host = "localhost"
    port = 5432
    user = "admin"
    password = "senha_segura"
```

Exemplo de arquivo config.json:


```bash
    {
        "database": {
            "host": "localhost",
            "port": 5432,
            "user": "admin",
            "password": "senha_segura"
        }
    }
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
Licença

Este projeto é licenciado sob a licença MIT License - consulte o arquivo LICENSE para mais detalhes.

_Uadson Feitosa_
