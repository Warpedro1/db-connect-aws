import mysql.connector

def get_connection():
    connection = mysql.connector.connect(host='database-1-popg.cwfltud3hwzs.sa-east-1.rds.amazonaws.com',
                                         database='popgrac',
                                         user='popgrac',
                                         password='popgrac123456')
    return connection

def close_connection(connection):
    if connection:
        connection.close()

def get_empregados_por_departamento():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        select_query = """
            SELECT d.Nome as Departamento, 
                   COUNT(e.Matricula) as Total_Empregados,
                   GROUP_CONCAT(e.Primeiro_Nome) as Empregados,
                   AVG(e.Salario) as Media_Salarial
            FROM Departamento d
            LEFT JOIN Empregado e ON d.Codigo = e.Departamento_Codigo
            GROUP BY d.Codigo, d.Nome
            ORDER BY d.Nome
        """
        cursor.execute(select_query)
        records = cursor.fetchall()
        print("Empregados agrupados por Departamento:")
        print("-" * 50)
        for row in records:
            print(f"Departamento: {row[0]}")
            print(f"Total de Empregados: {row[1]}")
            print(f"Empregados: {row[2] if row[2] else 'Nenhum empregado'}")
            print(f"Média Salarial: R$ {row[3]:.2f}" if row[3] else "Média Salarial: R$ 0.00")
            print("-" * 50)
        close_connection(connection)
    except (Exception, mysql.connector.Error) as error:
        print("Erro ao retornar dados:", error)

get_empregados_por_departamento()
