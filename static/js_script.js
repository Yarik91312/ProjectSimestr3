console.log('Я працюю');
const routes = [
    { path: '/signup', handler: signupHandler },
    { path: '/login', handler: loginHandler }



];
function RequestToServer(target, url) {
    return fetch(url, {
        method: 'POST',
        body: new FormData(target)
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error));
}

function signupHandler() {
    const Form = document.querySelector('#signup-form');
    const res = document.getElementById('result');
    const urlSignup = '/signup';
    console.log('Я signupHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlSignup)
        .then(response => {
        res.innerHTML = `<p>${response.message}</p>`});
    });
};





function loginHandler() {
    const Form = document.querySelector('#login-form');
    const res = document.getElementById('result');

    const urlLogin = '/login';
    console.log('Я loginHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlLogin)
        .then(response => {
            res.innerHTML = `<p>${response.message}</p>`;
        });
    });
};




function handleRoutes() {
    const currentPath = window.location.pathname;
    console.log('Я handleRoutes');
    const routeData = routes.find(route => route.path === currentPath);

    if (routeData && routeData.handler) {
        routeData.handler();
    } else {
        console.log('Маршрут не знайдено');
    }
};

document.addEventListener("DOMContentLoaded", function() {
    handleRoutes();
});



