function carregarBoleto() {
    const boletoId = '1'; // ID real do boleto cria uma func com back em python
    const boletoURL = `/api/boleto/${boletoId}`;

    fetch(boletoURL)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao baixar o boleto.');
            }
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);

            const embed = document.createElement('embed');
            embed.src = url;
            embed.type = 'application/pdf';
            embed.width = '100%';
            embed.height = '600px';

            const boletoContainer = document.getElementById('boleto_container');
            boletoContainer.innerHTML = ''; // Limpar o conteúdo anterior
            boletoContainer.appendChild(embed);

            const downloadButton = document.getElementById('download_button');
            downloadButton.onclick = function() {
                const link = document.createElement('a');
                link.href = url;
                link.download = `boleto_${boletoId}.pdf`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            };
        })
        .catch(error => {
            console.error('Erro ao baixar o boleto:', error);
            const boletoContainer = document.getElementById('boleto_container');
            boletoContainer.innerHTML = '<p>Erro ao carregar o boleto.</p>';
        });
}

window.onload = carregarBoleto;


function carregarDocumentacao() {
    const docId = '1'; // O mesmo da func anterior
    const docURL = `/api/doc/${docId}`;

    fetch(docURL)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao baixar a documentação.');
            }
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);

            const embed = document.createElement('embed');
            embed.src = url;
            embed.type = 'application/pdf';
            embed.width = '100%';
            embed.height = '600px';

            const docContainer = document.getElementById('doc_container');
            docContainer.innerHTML = ''; // Limpar o conteúdo anterior
            docContainer.appendChild(embed);

            const downloadButton = document.getElementById('download_doc_button');
            downloadButton.onclick = function() {
                const link = document.createElement('a');
                link.href = url;
                link.download = `documentacao_${docId}.pdf`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            };
        })
        .catch(error => {
            console.error('Erro ao baixar a documentação:', error);
            const docContainer = document.getElementById('doc_container');
            docContainer.innerHTML = '<p>Erro ao carregar a documentação.</p>';
        });
}

window.onload = carregarDocumentacao;
