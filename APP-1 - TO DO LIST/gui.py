import functions
import time
import PySimpleGUI as p
import os


if not os.path.exists('todos.txt'):
    with open('todos.txt','w') as file:
        pass
    
    
p.theme('DarkGreen3')
clock=p.Text('',key='clock')
label= p.Text("Type in a todo")
input_box=p.InputText(tooltip="enter todo",key='todo')
add_button=p.Button("Add")
list_box=p.Listbox(values=functions.get_todos(),key='todos',
                  enable_events=True,size=[45,10])
edit_button=p.Button("Edit")
complete_button=p.Button('Complete')
exit_button=p.Button('Exit')

window=p.Window('my todo app',
                layout=[[clock],
                        [label],
                        [input_box,add_button],
                       [list_box,edit_button,complete_button],
                       [exit_button]],
                font=('Helvetica','20'))

while True:
    event,values=window.read(timeout=10)
    window['clock'].update(value=time.strftime("%b %d, %Y %H:%M:%S"))
    if event=="Add":
        todos=functions.get_todos()
        new_todo=values['todo'] +"\n"
        todos.append(new_todo)
        functions.write_todos(todos)
        window['todos'].update(values=todos)
    elif event=='Edit':
        try:
            todo_to_edit=values['todos'][0]
            new_todo=values['todo']
            todos=functions.get_todos()
            index=todos.index(todo_to_edit)
            todos[index]=new_todo
            functions.write_todos(todos)
            window['todos'].update(values=todos)
        except IndexError:
            p.popup("Please select an item first")
            
    elif event=='todos':
        window['todo'].update(value=values['todos'][0])
        
    
    elif event=='Complete':
        try:
            todos_to_complete=values['todos'][0]
            todos=functions.get_todos()
            todos.remove(todos_to_complete)
            functions.write_todos(todos)
            window['todos'].update(values=todos)
            window['todo'].update(value='')
        except IndexError:
            p.popup("Please select an item first")
            
    elif event=='Exit':
        break
    
    elif event==p.WIN_CLOSED:
        break
 
window.close()