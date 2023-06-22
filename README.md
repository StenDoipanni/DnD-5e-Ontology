# DnD-5e-Ontology
An ontology for Dungeons and Drangons 5th edition


## Methodologies

Currently the methodologies adopted include: <\br>
1. SPARQLAnything from single XML files from the [Player's Handbook](https://github.com/kinkofer/FightClub5eXML/tree/main/Sources/PlayersHandbook) repository
2. RDFLib python script from the [D&D5e database](https://github.com/5e-bits/5e-database/tree/main/src) json files.


The SPARQL queries are available in the SPARQL_A files in this repository. The outcome is available as "DnD_5e_from_SPARQL_A.ttl".

The python script is available as "dnd_5edatabase2owl.py" in this repository. The outcome is available as "DnD_5e_from_rdflib.ttl".

Both the methodologies result in a first rough structure which need manual polishing and refinement.


## DnD 5e Ontology Network

The Expected final result is a network of ontological modules reusing entities leveraging the punning technique, allowing to inject great amount of knowledge for e.g. items and equipment, represented both as individuals in the RulesAsWritten (RAW) modules, and as classes of entities in the InDungeon (ID) modules.




