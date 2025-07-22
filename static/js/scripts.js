function mostrarDetalhes(id) {
    document.getElementById(`detalhes-${id}`).classList.add('mostrar');
}

function fecharDetalhes(id) {
    document.getElementById(`detalhes-${id}`).classList.remove('mostrar');
}
