import DFA, NFA, AFW
import json
import graphviz
import pydot


# ###
# TO-DO
# TODO correctness check of json imported automata

# Export a dfa "object" to a json file
# TODO dfa_to_json
def dfa_to_json(dfa):
    return


# Export a dfa "object" to a DOT file
# TODO dfa_to_dot
def dfa_to_dot(dfa):
    return


# Import a dfa from a json file
def dfa_json_importer(input_file):
    file = open(input_file)
    json_file = json.load(file)
    # TODO exception handling while JSON deconding/IO error
    alphabet = set(json_file['alphabet'])
    states = set(json_file['states'])
    initial_state = json_file['initial_state']
    accepting_states = set(json_file['accepting_states'])
    transitions = {}  # key [state ∈ states, action ∈ alphabet] value [arriving state ∈ states]
    for p in json_file['transitions']:
        transitions[p[0], p[1]] = p[2]

    # return list
    # return [alphabet, states, initial_state, accepting_states, transitions]

    # return map
    dfa = {}
    dfa['alphabet'] = alphabet
    dfa['states'] = states
    dfa['initial_state'] = initial_state
    dfa['accepting_states'] = accepting_states
    dfa['transitions'] = transitions
    return dfa


# Import a dfa from a DOT file
def dfa_dot_importer(input_file: str) -> dict:
    """ Import a dfa from a .dot file

    Of .dot files are recognized the following attributes

        nodeX   shape=doublecircle -> accepting node
        nodeX   root=true -> initial node
        edgeX   label="a" -> action in alphabet
        fake [style=invisible] -> skip this node, fake invisible one to initial state arrow
        fake -> S [style=bold] -> skip this transition, just initial state arrow for graphical purpose

    :param input_file: path to the .dot file
    :return: dict representing a dfa
    """

    # #pyDot Object
    g = pydot.graph_from_dot_file(input_file)[0]

    states = set()
    initial_state = 0
    accepting_states = set()
    for node in g.get_nodes():
        if node.get_name() == 'fake':
            continue
        states.add(node.get_name())
        for attribute in node.get_attributes():
            if attribute == 'root':
                # if initial_state!=0:
                #   TODO raise exception for wrong formatted dfa: dfa accepts only one initial state
                initial_state = node.get_name()
            if attribute == 'shape' and node.get_attributes()['shape'] == 'doublecircle':
                accepting_states.add(node.get_name())

    alphabet = set()
    transitions = {}
    for edge in g.get_edges():
        if edge.get_source() == 'fake':
            continue
        alphabet.add(edge.get_label().replace('"', ''))
        # if (edge.get_source(), edge.get_label().replace('"', '')) in transitions:
        #   TODO raise exception for wrong formatted dfa: dfa accepts only one transition from a state given a letter
        transitions[edge.get_source(), edge.get_label().replace('"', '')] = edge.get_destination()

    # if len(initial_state) == 0:
    #   TODO raise exception for wrong formatted dfa: there must be an initial state

    # if len(accepting_states)==0:
    #     TODO raise exception for wrong formatted dfa: there must be at least an accepting state

    # return map
    dfa = {}
    dfa['alphabet'] = alphabet
    dfa['states'] = states
    dfa['initial_state'] = initial_state
    dfa['accepting_states'] = accepting_states
    dfa['transitions'] = transitions
    return dfa


# Export a nfa "object" to a json file
# TODO nfa_to_json
def nfa_to_json(nfa):
    return


# Export a dfa "object" to a DOT file
# TODO dfa_to_dot
def nfa_to_dot(dfa):
    return


# Import a nfa from a json file
def nfa_json_importer(input_file):
    file = open(input_file)
    json_file = json.load(file)
    # TODO exception handling while JSON deconding/IO error
    alphabet = set(json_file['alphabet'])
    states = set(json_file['states'])
    initial_states = set(json_file['initial_states'])
    accepting_states = set(json_file['accepting_states'])
    transitions = {}  # key [state in states, action in alphabet] value [et of arriving states in states]
    for p in json_file['transitions']:
        transitions.setdefault((p[0], p[1]), set()).add(p[2])

    # return list
    # return [alphabet, states, initial_states, accepting_states, transitions]

    # return map
    nfa = {}
    nfa['alphabet'] = alphabet
    nfa['states'] = states
    nfa['initial_states'] = initial_states
    nfa['accepting_states'] = accepting_states
    nfa['transitions'] = transitions
    return nfa


# Import a nfa from a dot file
# TODO
def nfa_dot_importer(input_file):
    nfa = {}
    return nfa


# Export a afw "object" to a json file
# TODO afw_to_json
def afw_to_json(afw):
    return


# Import a afw from a json file
def afw_json_importer(input_file):
    file = open(input_file)
    json_file = json.load(file)
    # TODO exception handling while JSON deconding/IO error
    alphabet = set(json_file['alphabet'])
    states = set(json_file['states'])
    initial_state = json_file['initial_state']
    accepting_states = set(json_file['accepting_states'])

    transitions = {}  # key [state in states, action in alphabet] value [string representing boolean expression]
    for p in json_file['transitions']:
        transitions[p[0], p[1]] = p[2]

    # return list
    # return [alphabet, states, initial_state, accepting_states, transitions]

    # return map
    afw = {}
    afw['alphabet'] = alphabet
    afw['states'] = states
    afw['initial_state'] = initial_state
    afw['accepting_states'] = accepting_states
    afw['transitions'] = transitions
    return afw


# Print in output a DOT file and an image of the given DFA
# pydot library
def pydot_dfa_render(dfa, name):
    # TODO special view for sink node?
    g = pydot.Dot(graph_type='digraph')

    fake = pydot.Node('fake', style='invisible')
    g.add_node(fake)
    for state in dfa['states']:
        node = pydot.Node(str(state))
        if state == dfa['initial_state']:
            node.set_root(True)
            g.add_edge(pydot.Edge(fake, node, style='bold'))

        if state in dfa['accepting_states']:
            node.set_shape('doublecircle')
        g.add_node(node)

    for transition in dfa['transitions']:
        g.add_edge(pydot.Edge(str(transition[0]), str(dfa['transitions'][transition]), label=transition[1]))

    g.write_svg('img/' + name + '.svg')
    g.write_dot('img/' + name + '.dot')


# Print in output a DOT file and an image of the given DFA
# graphviz library
def graphviz_dfa_render(dfa, name):
    g = graphviz.Digraph(format='svg')
    g.node('fake', style='invisible')
    for state in dfa['states']:
        if state == dfa['initial_state']:
            if state in dfa['accepting_states']:
                g.node(str(state), root='true', shape='doublecircle')
            else:
                g.node(str(state), root='true')
        elif state in dfa['accepting_states']:
            g.node(str(state), shape='doublecircle')
        else:
            g.node(str(state))

    g.edge('fake', str(dfa['initial_state']), style='bold')
    for transition in dfa['transitions']:
        g.edge(str(transition[0]), str(dfa['transitions'][transition]), label=transition[1])

    g.render(filename='img/' + name + '.dot')


def nfa_render(nfa, name):
    g = pydot.Dot(graph_type='digraph')

    fake = pydot.Node('fake', style='invisible')
    g.add_node(fake)
    for state in nfa['states']:
        node = pydot.Node(state)
        if state in nfa['initial_states']:
            node.set_root(True)
            g.add_edge(pydot.Edge(fake, node, style='bold'))

        if state in nfa['accepting_states']:
            node.set_shape('doublecircle')
        g.add_node(node)

    for transition in nfa['transitions']:
        for dest in nfa['transitions'][transition]:
            g.add_edge(pydot.Edge(transition[0], dest, label=transition[1]))

    g.write_svg('img/' + name + '.svg')
    g.write_dot('img/' + name + '.dot')
    return
