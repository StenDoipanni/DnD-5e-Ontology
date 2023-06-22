### D&D ontology generation from json


import json
from rdflib import Graph, Literal, Namespace, RDF, URIRef

def generate_ontology(json_file):
    # Create a new RDF graph
    graph = Graph()

    # Define namespaces
    ns = Namespace("http://www.ontologydesignpatterns.org/ont/dnd5e/classes#")
    ont = Namespace("http://www.ontologydesignpatterns.org/ont/dnd5e/classes#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    owl = Namespace("http://www.w3.org/2002/07/owl#")

    # Bind namespaces to the graph
    graph.bind("", ns)
    graph.bind("rdf", rdf)
    graph.bind("rdfs", rdfs)
    graph.bind("owl", owl)
    ont.count = URIRef("http://www.ontologydesignpatterns.org/ont/dnd5e/classes#count")

    # Load JSON data
    with open(json_file, "r") as file:
        data = json.load(file)

        for item in data:
            index = item["index"]
            name = item["name"]

            # Create an individual for the class
            individual = ns[index.replace('-', '_')]
            graph.add((individual, RDF.type, ont.DnD_Entity))
            graph.add((individual, rdfs.label, Literal(name)))

            # Process other properties

            # Hit Die
            if "hit_die" in item:
                hit_die = item["hit_die"]
                graph.add((individual, ont.hit_die, Literal('d'+str(hit_die))))

                graph.add((ont.hit_die, RDF.type, owl.DatatypeProperty))

            # Proficiency Choices
            if "proficiency_choices" in item:
                proficiency_choices = item["proficiency_choices"]
                for i, choice in enumerate(proficiency_choices):
                    choice_individual = ns[index + "_proficiency_choice_" + str(i+1)]
                    graph.add((individual, ont.hasProficiencyChoice, choice_individual))
                    graph.add((choice_individual, RDF.type, ont.DnD_Entity))
                    graph.add((choice_individual, rdfs.comment, Literal(choice["desc"])))
                    graph.add((choice_individual, ont.choose, Literal(choice["choose"])))
                    graph.add((choice_individual, ont.type, Literal(choice["type"])))

                    # Specify the type of the introduced properties
                    graph.add((ont.choose, RDF.type, owl.DatatypeProperty))
                    graph.add((ont.hasProficiencyChoice, RDF.type, owl.ObjectProperty))
                    graph.add((ont.choose, RDF.type, owl.ObjectProperty))

                    options_array = choice["from"]["options"]
                    options_array_individual = ns[index + "_proficiency_choice_" + str(i+1) + "_options_array"]
                    graph.add((choice_individual, ont.hasOptionsArray, options_array_individual))
                    graph.add((ont.hasOptionsArray, RDF.type, owl.ObjectProperty))
                    graph.add((options_array_individual, RDF.type, ont.DnD_Entity))

                    for j, option in enumerate(options_array):
                        if "item" in option:
                            option_individual = ns[option["item"]["index"]]
                            graph.add((options_array_individual, ont.hasOption, option_individual))
                            graph.add((option_individual, RDF.type, ont.DnD_Entity))
                            graph.add((option_individual, ont.optionType, Literal(option["option_type"])))
                            graph.add((option_individual, rdfs.label, Literal(option["item"]["name"])))
                            graph.add((option_individual, ont.url, Literal(option["item"]["url"])))


            # Proficiencies
            if "proficiencies" in item:
                proficiencies = item["proficiencies"]
                for proficiency in proficiencies:
                    proficiency_individual = ns[proficiency["index"]]
                    graph.add((individual, ont.hasProficiency, proficiency_individual))
                    graph.add((ont.hasProficiency, RDF.type, owl.ObjectProperty))
                    graph.add((proficiency_individual, RDF.type, ont.DnD_Entity))
                    graph.add((proficiency_individual, rdfs.label, Literal(proficiency["name"])))
                    graph.add((proficiency_individual, ont.url, Literal(proficiency["url"])))



            # Saving Throws
            if "saving_throws" in item:
                saving_throws = item["saving_throws"]
                for saving_throw in saving_throws:
                    saving_throw_individual = ns[saving_throw["index"]]
                    graph.add((individual, ont.hasSavingThrow, saving_throw_individual))
                    graph.add((saving_throw_individual, RDF.type, ont.DnD_Entity))
                    graph.add((saving_throw_individual, rdfs.label, Literal(saving_throw["name"])))
                    graph.add((saving_throw_individual, ont.url, Literal(saving_throw["url"])))

                    graph.add((ont.hasSavingThrow, RDF.type, owl.ObjectProperty))

            # Starting Equipment
            if "starting_equipment" in item:
                starting_equipment = item["starting_equipment"]
                starting_equipment_individual = ns[index + "_starting_equipment"]
                graph.add((individual, ont.hasStartingEquipment, starting_equipment_individual))
                graph.add((starting_equipment_individual, RDF.type, ont.DnD_Entity))

                graph.add((ont.hasStartingEquipment, RDF.type, owl.ObjectProperty))


                for equipment in starting_equipment:
                    equipment_individual = ns[equipment["equipment"]["index"]]
                    graph.add((starting_equipment_individual, ont.hasEquipment, equipment_individual))
                    graph.add((ont.hasEquipment, RDF.type, owl.ObjectProperty))
                    graph.add((equipment_individual, RDF.type, ont.DnD_Entity))
                    graph.add((equipment_individual, rdfs.label, Literal(equipment["equipment"]["name"])))
                    graph.add((equipment_individual, ont.url, Literal(equipment["equipment"]["url"])))
                    graph.add((equipment_individual, ont.quantity, Literal(equipment["quantity"])))

                    graph.add((ont.quantity, RDF.type, owl.DatatypeProperty))


            # Starting Equipment Options
            if "starting_equipment_options" in item:
                starting_equipment_options = item["starting_equipment_options"]
                starting_equipment_options_individual = ns[index + "_starting_equipment_options"]
                graph.add((individual, ont.hasStartingEquipmentOptions, starting_equipment_options_individual))
                graph.add((starting_equipment_options_individual, RDF.type, ont.DnD_Entity))

                graph.add((ont.hasStartingEquipmentOptions, RDF.type, owl.ObjectProperty))


                for i, option in enumerate(starting_equipment_options):
                    choice_individual = ns[index + "_starting_equipment_option_" + str(i+1) + "_choice"]
                    graph.add((starting_equipment_options_individual, ont.hasChoice, choice_individual))
                    graph.add((choice_individual, RDF.type, ont.DnD_Entity))

                    graph.add((ont.hasChoice, RDF.type, owl.ObjectProperty))


                    if "desc" in option:
                        graph.add((choice_individual, rdfs.comment, Literal(option["desc"])))
                    if "choose" in option:
                        graph.add((choice_individual, ont.choose, Literal(option["choose"])))


                    if "from" in option and "options" in option["from"]:
                        options = option["from"]["options"]
                        for j, sub_option in enumerate(options):
                            if sub_option["option_type"] == "counted_reference":
                                sub_option_individual = ns[sub_option["of"]["index"]]
                                graph.add((options_array_individual, ont.hasOption, sub_option_individual))
                                graph.add((ont.hasOption, RDF.type, owl.ObjectProperty))
                                graph.add((sub_option_individual, RDF.type, ont.DnD_Entity))
                                graph.add((sub_option_individual, ont.optionType, Literal(sub_option["option_type"])))
                                graph.add((sub_option_individual, rdfs.label, Literal(sub_option["of"]["name"])))
                                graph.add((sub_option_individual, ont.url, Literal(sub_option["of"]["url"])))
                                graph.add((sub_option_individual, ont.count, Literal(sub_option["count"])))

                                graph.add((ont.count, RDF.type, owl.DatatypeProperty))


                            elif sub_option["option_type"] == "choice":
                                sub_choice_individual = ns[index + "_starting_equipment_option_" + str(i+1) + "_choice_" + str(j+1)]
                                graph.add((options_array_individual, ont.hasChoice, sub_choice_individual))
                                graph.add((sub_choice_individual, RDF.type, ont.DnD_Entity))
                                graph.add((sub_choice_individual, rdfs.comment, Literal(sub_option["choice"]["desc"])))
                                graph.add((sub_choice_individual, ont.choose, Literal(sub_option["choice"]["choose"])))


                                if "equipment_category" in sub_option["choice"]["from"] and "options" in sub_option["choice"]["from"]["equipment_category"]:
                                    sub_choice_options = sub_option["choice"]["from"]["equipment_category"]["options"]
                                    for k, sub_choice_option in enumerate(sub_choice_options):
                                        sub_choice_option_individual = ns[sub_choice_option["index"]]
                                        graph.add((sub_choice_individual, ont.hasOption, sub_choice_option_individual))
                                        graph.add((sub_choice_option_individual, RDF.type, ont.DnD_Entity))
                                        graph.add((sub_choice_option_individual, ont.optionType, Literal(sub_choice_option["option_type"])))
                                        graph.add((sub_choice_option_individual, rdfs.label, Literal(sub_choice_option["name"])))
                                        graph.add((sub_choice_option_individual, ont.url, Literal(sub_choice_option["url"])))


                                        if "item" in sub_choice_option:
                                            option_individual = ns[sub_choice_option["item"]["index"]]
                                            graph.add((sub_choice_option_individual, ont.hasItem, option_individual))
                                            graph.add((option_individual, RDF.type, ont.DnD_Entity))
                                            graph.add((option_individual, rdfs.label, Literal(sub_choice_option["item"]["name"])))
                                            graph.add((option_individual, ont.url, Literal(sub_choice_option["item"]["url"])))







    # Serialize the graph to Turtle format
    ontology_turtle = graph.serialize(format='turtle', encoding="utf-8").decode("utf-8")

    return ontology_turtle

# Example usage
json_file = "/Users/sdg/Desktop/D&D/dnd_classes.json"

dnd_ontology = generate_ontology(json_file)

output_file = "/Users/sdg/Desktop/D&D/dnd_classes_ontology.ttl"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(dnd_ontology)

print(dnd_ontology)
