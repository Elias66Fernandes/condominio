var dados_API = []
function atualizarUsuario(jsonUsuario) {
    
    var divDependentes = document.getElementById('dependentesAlterar');
    var dependentes = jsonUsuario.dependentes;
    divDependentes.innerHTML = '';
    dependentes.forEach(function(dependente, index) {
        var novoDependente = document.createElement('div');
        
        novoDependente.innerHTML = `
            <label for="dependente_nome_${index + 1}">Nome do Dependente ${index + 1}</label>
            <input type="text" id="dependente_alterar_nome_${index + 1}" name="dependente_nome_${index + 1}" value="${dependente.nome}" required>
            <label for="dependente_cpf_${index + 1}">CPF do Dependente ${index + 1}</label>
            <input type="text" id="dependente_alterar_cpf_${index + 1}" name="dependente_cpf_${index + 1}" value="${dependente.cpf}" required>
        `;
        divDependentes.appendChild(novoDependente);
    });
    console.log(divDependentes)
}
function adicionarDependente() {
    var divDependentes = document.getElementById('dependentes');
    var contador = divDependentes.children.length + 1;

    var novoDependente = document.createElement('div');
    novoDependente.innerHTML = `
        <label for="dependente_nome_${contador}">Nome do Dependente ${contador}</label>
        <input type="text" id="dependente_nome_${contador}" name="dependente_nome_${contador}" required>
        <label for="dependente_cpf_${contador}">CPF do Dependente ${contador}</label>
        <input type="text" id="dependente_cpf_${contador}" name="dependente_cpf_${contador}" required>
    `;

    divDependentes.appendChild(novoDependente);
}
function excluirUltimoDependente() {
    var divDependentes = document.getElementById('dependentes');
    if (divDependentes.children.length > 0) {
        divDependentes.removeChild(divDependentes.lastElementChild);
    } else {
        alert("Não há dependentes para excluir.");
    }
}

function adicionarDependenteAlterar() {
    var divDependentes = document.getElementById('dependentesAlterar');
    var contador = divDependentes.children.length + 1;

    var novoDependente = document.createElement('div');
    novoDependente.innerHTML = `
        <label for="dependente_nome_${contador}">Nome do Dependente ${contador}</label>
        <input type="text" id="dependente_nome_alterar_${contador}" name="dependente_nome_${contador}" required>
        <label for="dependente_cpf_${contador}">CPF do Dependente ${contador}</label>
        <input type="text" id="dependente_cpf_alterar_${contador}" name="dependente_cpf_${contador}" required>
    `;

    divDependentes.appendChild(novoDependente);
}
function excluirUltimoDependenteAlterar() {
    var divDependentes = document.getElementById('dependentesAlterar');
    if (divDependentes.children.length > 0) {
        divDependentes.removeChild(divDependentes.lastElementChild);
    } else {
        alert("Não há dependentes para excluir.");
    }
}

document.getElementById('registerForm').addEventListener('submit', function(event) {
    var form = event.target;
    var inputs = form.querySelectorAll('input, select');
    var valid = true;

    inputs.forEach(function(input) {
        if (!input.value) {
            valid = false;
            input.style.borderColor = 'red'; // Adiciona uma borda vermelha para indicar o campo obrigatório
        } else {
            input.style.borderColor = ''; // Remove a borda vermelha se o campo estiver preenchido
        }
    });

    if (!valid) {
        event.preventDefault(); // Impede o envio do formulário se algum campo estiver vazio
        alert('Por favor, preencha todos os campos.');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    fetch('/usuario') // Substitua pela URL da sua API
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            dados_API=data
            console.log(data)
            inserirDadosNaTabela(data)
            // Você pode atualizar o DOM ou realizar outras operações com os dados
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
});

function inserirDadosNaTabela(dados) {
    var tabelaCorpo = document.getElementById('tabela-corpo');
    tabelaCorpo.innerHTML = ''; // Limpa o corpo da tabela antes de inserir novos dados

    dados.forEach(item => {
        var linha = document.createElement('tr');
        linha.innerHTML = `

            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.contato}</td>
            <td>${item.cpf}</td>
            <td>${getIdentificador(item.identificador)}</td>
            <td>${item.username}</td>
            <td><button onclick="excluirLinha(${item.id})">Excluir</button></td>
        `;
        tabelaCorpo.appendChild(linha);
    });
}

function excluirLinha(id) {
    // Faz a chamada à API para excluir o item
    fetch(`/usuario/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (response.ok) {
            console.log(response)
            location.reload();
            // Opcional: Atualizar a tabela após a exclusão
            // Você pode recarregar os dados e chamar inserirDadosNaTabela novamente
        } else {
            alert('Erro ao excluir o item.');
        }
    })
    .catch(error => {
        console.error('Erro ao excluir o item:', error);
        alert('Erro ao excluir o item.');
    });
}


function getIdentificador(valor) {
    switch(valor) {
        case 1:
            return "Administrador";
        case 2:
            return "Condômino";
        case 3:
            return "Porteiro";
        default:
            return "Valor inválido";
    }
}
function excluirUsuario() {
    var idUsuario = document.getElementById('idUsuarioExcluir').value;
    
    if (!idUsuario) {
        alert('Por favor, insira um ID de usuário.');
        return;
    }

    fetch(`/usuario/${idUsuario}`, {
        method: 'DELETE' // Especifica o método DELETE
    }) // Substitua pela URL da sua API
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            inserirDadosNaTabela(data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            alert('Usuário não encontrado.');
        });
}
function buscarUsuario() {
        var idUsuario = document.getElementById('idUsuarioExcluir').value;
        if (!idUsuario) {
            alert('Por favor, insira um ID de usuário.');
            return;
        }

        fetch(`/usuario/${idUsuario}`) // Substitua pela URL da sua API
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
        .then(data => {
            var divInformacoes = document.getElementById("informacoes");

            // Preenche os dados do usuário nos elementos <p>
            divInformacoes.innerHTML = `
                <p><strong>E-mail:</strong> ${data.email}</p>
                <p><strong>Nome:</strong> ${data.name}</p>
                <p><strong>CPF:</strong> ${data.cpf}</p>
                <p><strong>Data de Nascimento:</strong> ${data.dataNascimento}</p>
                <p><strong>Identificador:</strong> ${data.identificador}</p>
            `;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            alert('Usuário não encontrado.');
        });
}
function buscarAlterarUsuario() {
    var idUsuario = document.getElementById('idUsuarioAlterar').value;
    console.log(idUsuario)
    if (!idUsuario) {
        alert('Por favor, insira um ID de usuário.');
        return;
    }

    fetch(`/usuario/${idUsuario}`) // Substitua pela URL da sua API
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            document.getElementById("idAlterar").value = data.id;
            document.getElementById("nomeAlterar").value = data.name;
            document.getElementById("emailAlterar").value = data.email;
            document.getElementById("usernameAlterar").value = data.username;
            document.getElementById("cpfAlterar").value = data.cpf;
            document.getElementById("data_nascimentoAlterar").value = new Date(data.dataNascimento).toISOString().split('T')[0];
            document.getElementById("cttAlterar").value = data.contato;
            document.getElementById("senhaAlterar").value = ''; // Você pode decidir se deseja preencher a senha ou não
            var select = document.getElementById('identificadorAlterar');

            // Itera sobre as opções para encontrar aquela com o valor correspondente
            for (var i = 0; i < select.options.length; i++) {
                if (select.options[i].value == data.identificador) {
                    select.selectedIndex = i;
                    break;
                }
            }
            atualizarUsuario(data)
            //document.getElementById("dependentesAlterar").value = data.dependentes;
            document.getElementById("admissaoAlterar").value = new Date(data.admissao).toISOString().split('T')[0];
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            alert('Usuário não encontrado.');
        });
}

    function excluirUsuario() {
    // Obtém o ID do usuário a ser excluído
    var idUsuario = document.getElementById("idUsuarioExcluir").value;

    // Faz a solicitação DELETE para a API
    fetch(`/usuario/${idUsuario}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        alert(data.message); // Exibe uma mensagem informando que o usuário foi excluído com sucesso
    })
    .catch(error => {
        console.error('Houve um problema com sua operação de exclusão:', error);
        alert('Usuário não encontrado ou ocorreu um erro ao excluir o usuário.');
    });
    }

document.addEventListener("DOMContentLoaded", function() {
    const txtConsulta = document.getElementById('txt_consulta');
    const tabelaCorpo = document.getElementById('tabela-corpo');

    // Função para filtrar os dados da tabela
    function filtrarTabela() {
        const termo = txtConsulta.value.trim().toLowerCase(); // Obtém o termo de busca em minúsculas
        
        Array.from(tabelaCorpo.getElementsByTagName('tr')).forEach(function(linha) {
            const colunas = linha.getElementsByTagName('td');
            let encontrou = false;
            
            // Verifica cada coluna da linha se contém o termo de busca
            Array.from(colunas).forEach(function(coluna, index) {
                if (coluna.textContent.toLowerCase().includes(termo)) {
                    encontrou = true;
                    return;
                }
            });

            // Exibe ou oculta a linha com base no resultado da busca
            if (encontrou) {
                linha.style.display = '';
            } else {
                linha.style.display = 'none';
            }
        });
    }

    // Adiciona um evento de input ao campo de busca
    txtConsulta.addEventListener('input', filtrarTabela);
});