const todosContainer = document.querySelector('.todos');
const form = document.querySelector('.todo-form');

let todos = [];

async function main() {
    todosDeleteListener();
    todosCreateListener();
    res = await axios.get('/todo/');
    todos = res.data;
    renderTodos();
}

const renderTodos = () => {
    todosContainer.innerHTML = '';
    for (let todo of todos) {
      renderTodo(todo);
    }
};

const renderTodo = todo => {
    todosContainer.innerHTML += `
        <p class="collection-item todo">
            <span data-id="${todo.id}" class="todo-text ${todo.is_done ? 'line-through' : ''}">${todo.todo_text}</span>
            <i class="material-icons secondary-content text-red todo-delete" data-id="${todo.id}">delete</i>
        </p>
    `
};

const todosDeleteListener = () => {
    todosContainer.addEventListener('click', async e => {
        if(Array.from(e.target.classList).includes('todo-delete')) {
            const todo_id = parseInt(e.target.getAttribute('data-id'));
            todos = todos.filter(todo => todo.id !== todo_id);
            renderTodos();
            try {
                await axios.delete(`/todo/${todo_id}`);
            }
            catch(e) {
                console.log(e);
            }
        }
        if (Array.from(e.target.classList).includes('todo-text')) {
            const todo_id = parseInt(e.target.getAttribute('data-id'));
            todos = todos.map(todo =>
                todo.id === todo_id ? {...todo, is_done: !todo.is_done}: todo);
            renderTodos();

            try {
                await axios.put(`/todo/${todo_id}/`, todos.find(
                    todo => todo.id === todo_id));
            }
            catch(e) {
                console.log(e);
            }
        }
    });
};

const todosCreateListener = () => {
    form.addEventListener('submit', async e => {
        e.preventDefault();
        const todo_text = form.todo_text.value;
        e.target.reset();
        try {
            if(todo_text) {
                const {data: todo} = await axios.post('/todo/', {
                    todo_text
                });
                todos.unshift(todo);
                renderTodos();
            }
        }
        catch(e) {
            console.log(e);
        }
    })
};

main();