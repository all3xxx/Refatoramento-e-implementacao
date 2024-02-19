from flask import Flask, jsonify, request
from singleton import Mapa
from jogador import Jogador
from territory import Territory
import json


app = Flask(__name__)
identifica_player = ['%', '$', '*', '#']
mapa = Mapa.instance()
mapa.nomeMapa = 'Nether Minecraft'

def criar_players(data):
    listPlayers = []
    for i in range(len(data['players'])):
        listPlayers.append(Jogador(identifica_player[i], data['players'][i], mapa))
    return listPlayers

def validar_player(data):
    return 0 < len(data['players']) < 4

@app.route('/setPlayers', methods=['POST'])
def setPlayers():
    try:
        data = request.json
        if validar_player(data):
            mapa.players = criar_players(data)
            resposta = {"mensagem": "Jogadores adicionados com sucesso!"}
        else:
            resposta = {"mensagem": "Número inválido de jogadores"}
        return jsonify(resposta)
    except Exception as e:
        resposta_erro = {"erro": str(e)}
        return jsonify(resposta_erro), 400


def criar_territorios():
    return [Territory(i + 1, [0, 0]) for i in range(42)]

@app.route('/setTerritories', methods=['GET'])
def setTerritories():
    mapa.territories = criar_territorios()
    resposta = {"mensagem": "Territórios criados com sucesso"}
    return jsonify(resposta)


@app.route('/sortTerritories', methods=['GET'])
def sortTerritories(): 
    result = mapa.sortTerritories()
    resposta = {"mensagem": result}
    return jsonify(resposta)

@app.route('/testeMapa', methods=['GET'])
def testeMapa(): 
    result = mapa.testMapa()
    resposta = {"mensagem": result}
    return jsonify(resposta)

@app.route('/placeArmy', methods=['POST'])
def colocar_exercito():
    try:
        data = request.json
        territorio_id = data['territorio_id']
        player_id = data['player_id']
        conta_exercito = data['conta_exercito']
        
        if player_id not in [player.id for player in mapa.players]:
            return jsonify({"mensagem": "Jogador não encontrado"}), 400
        
        territorio = next((territorio for territorio in mapa.territories if territorio.id == territorio_id), None)
        if territorio is None:
            return jsonify({"mensagem": "Território não encontrado"}), 400
        
        if territorio.owner_id is not None and territorio.owner_id != player_id:
            return jsonify({"mensagem": "Território já pertence a outro jogador"}), 400
        
        territorio.owner_id = player_id
        territorio.conta_exercito = conta_exercito
        
        return jsonify({"mensagem": "Exército colocado com sucesso!"})
    
    except Exception as e:
        resposta_erro = {"erro": str(e)}
        return jsonify(resposta_erro), 400  


if __name__ == '__main__':
    app.run(debug=True)