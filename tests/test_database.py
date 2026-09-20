from backend.database.database import engine


try:
    with engine.connect():
        print("Conexão com MySQL realizada com sucesso!")

except Exception as e:
    print("Erro ao conectar ao MySQL:")
    print(e)