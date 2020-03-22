const todosContainer = document.querySelector('.todos');
const form = document.querySelector('.todo-form');

let todos = [];

console.log("Hello world")

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
            ${todo.todo_text}
            <i class="material-icons secondary-content text-red todo-delete" data-id="${todo.id}">delete</i>
        </p>
    `
};

const todosDeleteListener = () => {
    todosContainer.addEventListener('click', e => {
        console.log(e.target);
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