# Sistema de gestão de banco de sangue

Esse é um sistema de gestão de banco de sangue composto por um conjunto de tabelas que representam doações de sangue, contendo tabelas como: Bancos de sangue, Doadores e doações. 

O sistema exige que as tabelas existam e estejam em funcionamento, para isso basta executar o script Python a seguir para criação das tabelas e preenchimento dos dados necessarios:

(https://github.com/lgsn0w/TrabalhoC2_BD/blob/main/sql/tabelas.sql)

Para executar o sistema basta executar o script Python a seguir:

(https://github.com/lgsn0w/TrabalhoC2_BD/blob/main/src/main.py)

## Organização
- [diagramas](diagramas): Nesse diretório está o [diagrama relacional](https://github.com/lgsn0w/TrabalhoC2_BD/blob/main/diagramas/DIAGRAMA_RELACIONAL_BANCO_DE_SANGUE.pdf) do sistema.
    * O sistema possui três entidades: DOADORES, BANCO_DE_SANGUE, DOAÇÕES. 
- [sql](sql): Nesse diretório estão os scripts para criação das tabelas.
    * [tabelas.sql](sql/tabelas.sql): script responsável pela criação das tabelas, relacionamentos e criação de permissão no esquema LabDatabase.
- [src](main): Nesse diretório estão os scripts do sistema.
      
------------------------------------------------------------------------------------------------------------------------------

    * [sql](src/sql/): Nesse diretório encontram-se os scripts utilizados para geração dos relatórios a partir da [tabelas.sql]    
    * [main.py](src/main.py): Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.

### Bibliotecas Utilizadas
- [requirements.txt](src/requirements.txt): `pip install -r requirements.txt`

### Video 

https://github.com/lgsn0w/TrabalhoC2_BD/assets/112468011/1df875e4-a3ab-4bac-b63a-307c79b9742a

