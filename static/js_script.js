console.log('Я працюю');
const routes = [
    { path: '/signup', handler: signupHandler },
    { path: '/login', handler: loginHandler }



];
function RequestToServer(form, url) {
    const formData = new FormData(form);
    console.log('Я RequestToServer');
    formData.append('key1', 'value1');

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            resolve(data);
        });
    });
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


