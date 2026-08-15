from langgraph.graph import StateGraph,START,END

from graph.state import ProjectState
from graph.tester_node import tester_node
graph=StateGraph(ProjectState)
graph.add_node('tester',tester_node)
graph.add_edge(START,'tester')
graph.add_edge('tester',END)
app=graph.compile()
initial_state:ProjectState={
    'project_path':"sample_projects/buggy_calculator",
    'files':[
        'calculator.py'
        'test_calculator.py'
    ],
    'test_output':'',
    'tests_passed':False,
    'itertaion':1
}
result=app.invoke(initial_state)
print('tests passed:',result['tests_passed'])
print('\n-----test output----')
print(result['test_output'])