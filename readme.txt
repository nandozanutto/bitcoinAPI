-Resumo
Este código utiliza a api disponível em: https://coinmarketcap.com/api/documentation/v1/ para pegar
os dados atualizados sobre criptomoedas. São utilizados dois endpoints: /v1/cryptocurrency/listings/latest
e /v2/cryptocurrency/info. O primeiro retorna dados financeiros da moeda, como capitalização de mercado
e preço, enquanto o segundo retorna meta dados, como o nome da moeda, o símbolo, a categoria e website.

-Estratégia
Foi implementada a seguinte estratégia:
A cada chamada do código, novas informações financeiras das principais moedas são extraídas da api e
armazenadas em uma tabela no banco de dados mysql, com o nome coins_prices. Após isso, é checado se 
para moedas adicionadas já existe a descrição da moeda na tabela coins_names, caso não exista, a api é
consultada para pegar os meta dados da moeda e uma nova linha na tabela coins_names é criada com tal
informação. Portanto, a tabela coins_names salva apenas 1 vez a descrição das moedas.
As chamadas de api foram feitas em batch, para demonstrar como eu lidaria com limitações da api e
retornos paginados. A variável batch_size define a quantidade de moedas a seres pesquisadas a cada chamado.

-Como rodar
1. Instalar mysql, criar um usuário e uma database
2. configurar o arquivo db_config.ini com suas informações do banco de dados
3. colocar a chave da api em api_key.json
4. pip install -r ./requirements.txt
5. python3 main.py 
