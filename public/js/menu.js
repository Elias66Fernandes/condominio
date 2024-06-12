var menuItem = document.querySelectorAll('.itens-menu');

function selectLink() {
    menuItem.forEach((item) => item.classList.remove('ativo'));
    this.classList.add('ativo');

    var sectionId = this.getAttribute('data-section');
    var sections = document.querySelectorAll('.section');
    sections.forEach((section) => section.classList.remove('active'));

    var activeSection = document.getElementById(sectionId);
    activeSection.classList.add('active');
}

menuItem.forEach((item) => item.addEventListener('click', selectLink));

var btnExp = document.querySelector('#btn-exp');
var menuSide = document.querySelector('.menu-lateral');

btnExp.addEventListener('click', function() {
    menuSide.classList.toggle('expandir');
});

// Adiciona a funcionalidade para trocar as telas dentro de "Gerenciar Usuários"
function showScreen(screenId) {
    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => {
        if (screen.id === screenId) {
            screen.classList.add('active');
        } else {
            screen.classList.remove('active');
        }
    });
}

// Adiciona o evento de clique aos botões de gerenciamento de usuários
document.querySelectorAll('.buttons button').forEach(button => {
    button.addEventListener('click', function() {
        const screenId = this.getAttribute('onclick').replace('showScreen(\'', '').replace('\')', '');
        showScreen(screenId);
    });
});
