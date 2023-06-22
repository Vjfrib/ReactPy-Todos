from reactpy import (
    component, # wrapper for creating ReactPy components
    html, # contains all html elements to use
    hooks # contains the use_state function
)
from reactpy.backend.flask import configure # to configure Flask server
from flask import Flask # to create a Flask app

@component
def Header():
    """Shown at the top of the page."""
    toggle, set_toggle = hooks.use_state(True) # init var for toggling info

    def handle_click(event):
        """Runs when Toggle Info button is clicked"""
        set_toggle(not toggle) # flip 
    
    return html.div(
        html.h1("ReactPy ToDo"), # title
        html.hr(), # hr element
        html.button({'on_click': handle_click}, 'Toggle Info'),
        # info div below
        html.div(
            {'style': {
                'display': ('block' if toggle else 'none')
            }}, # hide if toggle is set to 0

            html.h3('Info'),
            html.p('This is a simple ToDo app, demonstrating the capabilities of the ', html.a({'href': 'https://reactpy.dev'}, 'ReactPy'), ' python framework.'),
            html.p('The ReactPy framework allows you to design web apps in python using react-like syntax and features (such as: use_state).'),
            html.p('It also means that the client will update automatically after server changes, which is pretty neat!'),
            html.p('As is the tradition when showcasing any new web-app framework, I have created a simple ToDo app.'),

            html.h3('Usage'),
            html.p('Click on an item to remove it from the list, or hold shift while clicking to edit.'),
            html.hr()
        )
    )

@component
def ToDoItem(text: str, remove_todo: callable, update_todo: callable):
    """Represents a single todo on the list.
        :param text: str - todo text
        :param remove_todo: callable - function to remove todo, takes text as argument
        :param update_todo: callable - function to update todo item, takes two arguments, oldTodo, and newTodo
    """
    editing, set_editing = hooks.use_state(False)
    newText, set_newText = hooks.use_state("")
    
    def handle_click(event):
        """Is called when the todo is clicked."""
        if event['shiftKey']: # if shift is held while clicked
            set_editing(True) # toggle editing mode
        else:
            remove_todo(text) # remove this item

    def handle_update_click(event):
        """Is called when the Update button is clicked"""
        if newText: # if text edited
            update_todo(text, newText) # replace todo in list
            set_newText('') # clear input
            set_editing(False) # turn off editing mode
        else: # cancel operation
            set_newText('')
            set_editing(False)

    def handle_keypress(event):
        if event['key'] == 'Enter':
            handle_update_click(event)

    def handle_change(event):
        """Is called when the input for editing item is updated."""
        set_newText(event['target']['value'])

    if not editing:
        return html.p(
            html.button({'on_click': handle_click}, text), # button displaying todo text
            html.br() # br element - spacer
        )
    else:
        return html.div(
            html.label('Update: ', html.input({'on_change': handle_change, 'value': newText, 'on_key_press': handle_keypress})),
            html.button({'on_click': handle_update_click}, 'Save'),
            html.br()
        )

@component
def ToDo():
    """The main ToDo app."""
    todos, set_todos = hooks.use_state([]) # initialize empty todo list
    currentInput, set_input = hooks.use_state("") # init empty str input
    
    def add_todo(event):
        """Gets called when the New button is clicked."""
        if (currentInput): # if a todo is written
            set_todos([*todos, currentInput]) # update list of todos
            set_input("") # clear the input

    def handle_keypress(event):
        if event['key'] == 'Enter':
            add_todo(event)
            
    def remove_todo(todo: str):
        """Function to remove an item from the todo list.
            :param todo: str - todo item text (to remove)
        """
        set_todos([t for t in todos if not t == todo]) # update todo list

    def update_todo(oldTodo: str, newTodo: str):
        """Function to replace an item in the todo list.
            :param oldTodo: str - old todo text
            :param newTodo: str - new todo text
        """
        set_todos([(t if not t == oldTodo else newTodo) for t in todos])
        
    def set_currentInput(event):
        """Updates the currentInput with value from input elm"""
        set_input(event['target']['value'])

    todoList = [
        ToDoItem(todo, remove_todo, update_todo) # create list item component
        for todo in todos # for every todo on the list
    ]
    return html.div(
        html.h2('ToDo:'), # title
        html.ul(*todoList), # display todos
        html.br(), # br elm - spacer
        html.label(
            html.button({'on_click': add_todo}, 'New: '), # New button
            html.input({'on_change': set_currentInput, 'value': currentInput, 'on_key_press': handle_keypress}) # input elm, setting value to currentInput so we can clear it after New is clicked
        )
    )

@component
def App():
    """The entire app."""
    return html.div(
        Header(), # header component
        ToDo() # todo app component
    )

app = Flask(__name__) # my chosen backend is Flask
configure(app, App) # configure it for ReactPy

if __name__ == '__main__': # if running repl
    app.run(host='0.0.0.0', port=8080) # start the web server