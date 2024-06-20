document.addEventListener('DOMContentLoaded', function() {
    fetchEspacosComuns();
});

function fetchEspacosComuns() {
    fetch('/espacoscomuns') // Substitua pela URL correta da sua API
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            preencherSelectEspacosComuns(data);
            preencherTabelaEspacosComuns(data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

function preencherSelectEspacosComuns(espacos) {
    var selectEspacoComum = document.getElementById('select-espaco-comum');

    espacos.forEach(espaco => {
        var option = document.createElement('option');
        option.value = espaco.id;
        option.textContent = espaco.name;
        selectEspacoComum.appendChild(option);
    });
}

function preencherTabelaEspacosComuns(espacos) {
    var tabelaCorpo = document.getElementById('tabela-corpo-espaco');
    tabelaCorpo.innerHTML = ''; // Limpar tabela antes de preencher

    espacos.forEach(espaco => {
        var row = document.createElement('tr');
        
        var cellId = document.createElement('td');
        cellId.textContent = espaco.id;
        row.appendChild(cellId);

        var cellName = document.createElement('td');
        cellName.textContent = espaco.name;
        row.appendChild(cellName);

        var cellActions = document.createElement('td');

        // Botão de atualizar
        var btnUpdate = document.createElement('button');
        btnUpdate.textContent = 'Atualizar';
        btnUpdate.addEventListener('click', function() {
            // Chamar a função de atualização passando o espaco.id
            var form = document.getElementById('formCadastroEspaco');
            form.action = '/espacoscomuns/atualizar';
            // Preencher o campo nome_espaco com o nome do espaço
            var inputNomeEspaco = document.getElementById('nome_espaco');
            inputNomeEspaco.value = espaco.name;

            var inputIdEspaco = document.getElementById('id_espaco');
            inputIdEspaco.value = espaco.id;
            
        });
        cellActions.appendChild(btnUpdate);

        // Botão de deletar
        var btnDelete = document.createElement('button');
        btnDelete.textContent = 'Deletar';
        btnDelete.addEventListener('click', function() {
            // Chamar a função de deletar passando o espaco.id
            deletarEspaco(espaco.id);
        });
        cellActions.appendChild(btnDelete);
        row.appendChild(cellActions);

        tabelaCorpo.appendChild(row);
});}


// Função de exemplo para deletar um espaço
function deletarEspaco(id) {
    fetch('/espacoscomuns/' + id, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao excluir o espaço');
        }
        console.log('Espaço excluído com sucesso');
        location.reload();
        // Aqui você pode adicionar lógica adicional após a exclusão do espaço
    })
    .catch(error => {
        console.error('Erro ao excluir o espaço:', error);
        // Aqui você pode lidar com o erro, por exemplo, exibir uma mensagem de erro na interface
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const txtConsulta = document.getElementById('txt_consulta_espaco');
    const tabelaCorpoEspaco = document.getElementById('tabela-corpo-espaco');
    // Função para filtrar os dados da tabela
    function filtrarTabelaEspaco() {
        const termo = txtConsulta.value.trim().toLowerCase(); // Obtém o termo de busca em minúsculas
        
        Array.from(tabelaCorpoEspaco.getElementsByTagName('tr')).forEach(function(linha) {
            const colunas = linha.getElementsByTagName('td');
            let encontrou = false;
            
            // Verifica cada coluna da linha se contém o termo de busca
            Array.from(colunas).forEach(function(coluna, index) {
                console.log(coluna.textContent)
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
    txtConsulta.addEventListener('input', filtrarTabelaEspaco);
});

function buscarNomePorId(locais, idProcurado) {
    for (var i = 0; i < locais.length; i++) {
        if (locais[i]['id'] === idProcurado) {
            return locais[i]['nome'];
        }
    }
    return null;  // Retorna null se o ID não for encontrado
}
function buscarIdPorNome(locais, nome){

}

var agendamentos = [];
var locais = [];

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    // Primeira requisição para obter os espaços comuns
    $.ajax({
        url: '/espacoscomuns', // URL da API para obter os eventos
        type: 'GET',
        success: function(response) {
            // Manipular os eventos obtidos da API aqui
            for (var indice in response) {
                locais.push({'id': response[indice]['id'], 'nome': response[indice]['name']});
            }

            // Segunda requisição para obter os agendamentos
            $.ajax({
                url: '/agendamento', // URL da API para obter os eventos
                type: 'GET',
                success: function(response) {
                    // Manipular os eventos obtidos da API aqui
                    for (var indice in response) {
                        agendamentos.push({
                            'title': buscarNomePorId(locais, response[indice]['espaco_id']),
                            'start': response[indice]['data_inicio'],
                            'end': response[indice]['data_fim'],
                            'backgroundColor': '#ffcc00',
                            'id':response[indice]['espaco_id']
                        });
                    }
                    // Cria o calendário com os agendamentos carregados
                    criarCalendario(agendamentos);
                },
                error: function(xhr, status, error) {
                    // Manipular erros aqui
                    console.error(xhr.responseText);
                }
            });
        },
        error: function(xhr, status, error) {
            // Manipular erros aqui
            console.error(xhr.responseText);
        }
    });
    function dataFormato(date){
        let year = date.getFullYear();
        let month = String(date.getMonth() + 1).padStart(2, '0');
        let day = String(date.getDate()).padStart(2, '0');
        let hours = String(date.getHours()).padStart(2, '0');
        let minutes = String(date.getMinutes()).padStart(2, '0');

        // Monta a string no formato desejado "yyyy-MM-dd'T'HH:mm"
        let formattedDate = `${year}-${month}-${day}T${hours}:${minutes}`;
        return formattedDate
    }
    function criarCalendario(eventos) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: eventos,
            eventClick: function (info) {

                var startDate= dataFormato(new Date(info.event.start))
                var endDate=dataFormato(new Date(info.event.end))
                console.log(endDate)
                 
                document.getElementById('usuarios_id').value = info.event.extendedProps.usuarios_id;

                document.getElementById('data_inicio').value  = startDate
                document.getElementById('data_fim').value = endDate
                document.getElementById('old_data_inicio').value = startDate
                document.getElementById('old_data_fim').value = endDate
                document.getElementById('old_espaco_id').value = info.event.id;

                
                document.getElementById('old_usuarios_id').value = info.event.extendedProps.usuarios_id;

                var selectEspacoComum = document.getElementById('select-espaco-comum');
                        for (var i = 0; i < selectEspacoComum.options.length; i++) {
                            if (selectEspacoComum.options[i].value == info.event.extendedProps.title) {
                                selectEspacoComum.options[i].selected = true;
                                break;
                            }
                        }

                        // Altera a ação do formulário
                        document.getElementById('formAgendamento').action = '/agendamento/alterar';

                        // Altera o texto do botão de submissão
                        document.getElementById('submitButton').value = 'Alterar Agendamento';

            }
        });
        calendar.render();
    }
});