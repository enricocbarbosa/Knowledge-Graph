from rdflib import Graph

g = Graph()
g.parse("carioca_2026_fase_final_ontologia.ttl", format="turtle")

# 1. Consulta simples de seleção
# Lista o nome de todos os times do campeonato.
q1 = """
PREFIX ex: <http://example.org/carioca2026/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?nomeTime WHERE {
    ?time a ex:Time ;
          rdfs:label ?nomeTime .
}
"""
print("Query 1: ")
for row in g.query(q1):
    print(row.nomeTime)
print()


# 2. Consulta com FILTER numérico
# Gols marcados depois do minuto 60.

q2 = """
PREFIX ex: <http://example.org/carioca2026/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?nomeJogador ?minuto WHERE {
    ?gol a ex:Gol ;
         ex:marcouGol ?jogador ;
         ex:ocorreuNoMinuto ?minuto .
    ?jogador rdfs:label ?nomeJogador .
    FILTER (?minuto > 60)
}
ORDER BY ?minuto
"""
print("Query 2: ")
for row in g.query(q2):
    print(row.minuto, "-", row.nomeJogador)
print()


# 3. Consulta com regex e flag "i"
# Jogadores cujo nome contém "ferreira", ignorando maiúsculas/minúsculas.

q3 = """
PREFIX ex: <http://example.org/carioca2026/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?nome WHERE {
    ?jogador a ex:Jogador ;
             rdfs:label ?nome .
    FILTER regex(str(?nome), "ferreira", "i")
}
"""
print("Query 3: ")
for row in g.query(q3):
    print(row.nome)
print()


# 4. Consulta com negação (FILTER NOT EXISTS)
# Jogos que não tiveram nenhum pênalti registrado.

q4 = """
PREFIX ex: <http://example.org/carioca2026/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?label WHERE {
    ?jogo a ex:Jogo ;
          rdfs:label ?label .
    FILTER NOT EXISTS { ?jogo ex:temPenalti ?pen }
}
"""
print("Query 4:")
for row in g.query(q4):
    print(row.label)
print()


# 5. Consulta com subconsulta
# Pega o jogador que marcou mais gols (usando subquery para calcular o máximo).

q5 = """
PREFIX ex: <http://example.org/carioca2026/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?nomeJogador ?totalGols WHERE {
    ?jogador rdfs:label ?nomeJogador .
    {
        SELECT ?jogador (COUNT(?gol) AS ?totalGols) WHERE {
            ?gol a ex:Gol ;
                 ex:marcouGol ?jogador .
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


# Extra — usando OPTIONAL
# Lista os jogos mostrando o público quando existir (alguns jogos não têm ex:publico registrado).

q_extra = """
PREFIX ex: <http://example.org/carioca2026/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?label ?publico WHERE {
    ?jogo a ex:Jogo ;
          rdfs:label ?label .
    OPTIONAL { ?jogo ex:publico ?publico }
}
"""
print("Query extra:")
for row in g.query(q_extra):
    print(row.label, "-", row.publico if row.publico else "sem registro")
