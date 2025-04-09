# ufsc-computer-graphics
Repository created with the objective of sharing programs developed in the Computer Graphics course taught by professors Prof. Aldo v. Wangenheim.

## Para rodar o watchdog nos projetos (Ubuntu/WSL)


### 1. Ative o ambiente virtual (na raiz do projeto que deseja executar)
```
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instale as dependencias
`pip install -r requirements.txt`

#### Caso deseje sair do ambiente virtual execute o seguinte comando no terminal:
`deactivate`

### 3. Agora execute o script auto_reload.py
`python3 auto_reload.py`

### 4. Pronto agora você terá um desenvolvimento em tempo real sem a necessidade de reiniciar seu programa manualmente para verificar as modificações