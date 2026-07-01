from rdflib import Graph

g = Graph()
g.parse("carioca_2026_grafo.ttl", format="turtle")

# 1. Consulta simples de seleção
# Todos os jogos com mandante, visitante e placar, ordenados por data.
q1 = """
PREFIX ex: <http://example.org/>
SELECT ?data ?nomeMandante ?golsMandante ?golsVisitante ?nomeVisitante WHERE {
    ?partida a ex:Partida ;
             ex:mandante ?timeMandante ;
             ex:visitante ?timeVisitante ;
             ex:golsMandante ?golsMandante ;
             ex:golsVisitante ?golsVisitante ;
             ex:data ?data .
    ?timeMandante ex:nome ?nomeMandante .
    ?timeVisitante ex:nome ?nomeVisitante .
    FILTER (lang(?nomeMandante) = "pt")
    FILTER (lang(?nomeVisitante) = "pt")
}
ORDER BY ?data
"""
print("Query 1:")
for row in g.query(q1):
    print(row.data, "-", row.nomeMandante, row.golsMandante, "x", row.golsVisitante, row.nomeVisitante)
print()


# 2. Consulta com FILTER numérico
# Gols marcados após o minuto 60, com o nome do jogador.
q2 = """
PREFIX ex: <http://example.org/>
SELECT ?nomeJogador ?minuto WHERE {
    ?partida a ex:Partida ;
             ex:temEvento ?evento .
    ?evento a ex:Gol ;
            ex:envolveJogador ?jogador ;
            ex:minuto ?minuto .
    ?jogador ex:nome ?nomeJogador .
    FILTER (?minuto > 60)
}
ORDER BY ?minuto
"""
print("Query 2:")
for row in g.query(q2):
    print(f"{row.minuto}' - {row.nomeJogador}")
print()


# 3. Consulta com regex e flag "i"
# Jogadores cujo nome contém "pedro", ignorando maiúsculas/minúsculas.
q3 = """
PREFIX ex: <http://example.org/>
SELECT ?nome WHERE {
    ?jogador a ex:Jogador ;
             ex:nome ?nome .
    FILTER regex(str(?nome), "pedro", "i")
}
"""
print("Query 3:")
for row in g.query(q3):
    print(row.nome)
print()


# 4. Consulta com negação (FILTER NOT EXISTS)
# Partidas sem árbitro principal registrado.
q4 = """
PREFIX ex: <http://example.org/>
SELECT ?nomeMandante ?nomeVisitante ?data WHERE {
    ?partida a ex:Partida ;
             ex:data ?data ;
             ex:mandante ?timeMandante ;
             ex:visitante ?timeVisitante .
    ?timeMandante ex:nome ?nomeMandante .
    ?timeVisitante ex:nome ?nomeVisitante .
    FILTER NOT EXISTS { ?partida ex:arbitroPrincipal ?arbitro }
    FILTER (lang(?nomeMandante) = "pt")
    FILTER (lang(?nomeVisitante) = "pt")
}
ORDER BY ?data
"""
print("Query 4:")
for row in g.query(q4):
    print(f"{row.data} - {row.nomeMandante} x {row.nomeVisitante}")
print()


# 5. Consulta com subconsulta
# Jogador que marcou mais gols em toda a competição.
q5 = """
PREFIX ex: <http://example.org/>
SELECT ?nomeJogador ?totalGols WHERE {
    ?jogador ex:nome ?nomeJogador .
    {
        SELECT ?jogador (COUNT(?gol) AS ?totalGols) WHERE {
            ?partida a ex:Partida ;
                     ex:temEvento ?gol .
            ?gol a ex:Gol ;
                 ex:envolveJogador ?jogador .
        }
        GROUP BY ?jogador
        ORDER BY DESC(?totalGols)
        LIMIT 1
    }
}
"""
print("Query 5:")
for row in g.query(q5):
    print(row.nomeJogador, "-", row.totalGols, "gols")
print()


# 6. Consulta sobre cartões
# Lista os cartões registrados, com a partida, o jogador, o minuto e o tipo do cartão.
q6 = """
PREFIX ex: <http://example.org/>
SELECT ?partida ?nomeMandante ?nomeVisitante ?nomeJogador ?minuto ?tipoCartao WHERE {
    ?partida a ex:Partida ;
             ex:mandante ?timeMandante ;
             ex:visitante ?timeVisitante ;
             ex:temEvento ?evento .
    ?evento a ex:Cartao ;
            ex:envolveJogador ?jogador ;
            ex:minuto ?minuto ;
            ex:tipoCartao ?tipoCartao .
    ?timeMandante ex:nome ?nomeMandante .
    ?timeVisitante ex:nome ?nomeVisitante .
    ?jogador ex:nome ?nomeJogador .
    FILTER (lang(?nomeMandante) = "pt")
    FILTER (lang(?nomeVisitante) = "pt")
    FILTER (lang(?nomeJogador) = "pt")
}
ORDER BY ?partida ?minuto
"""
print("Query 6:")
for row in g.query(q6):
    print(f"{row.minuto}' - {row.nomeJogador} ({row.tipoCartao}) - {row.nomeMandante} x {row.nomeVisitante}")
print()


# Extra — lang()
# Lista os clubes mostrando apenas o nome em português, aproveitando que ex:Maracana tem dois labels de idiomas diferentes em ex:nome.
q_extra = """
PREFIX ex: <http://example.org/>
SELECT ?nomeClube WHERE {
    ?clube a ex:Clube ;
           ex:nome ?nomeClube .
    FILTER (lang(?nomeClube) = "pt")
}
ORDER BY ?nomeClube
"""
print("Query Extra:")
for row in g.query(q_extra):
    print(row.nomeClube)
print()
