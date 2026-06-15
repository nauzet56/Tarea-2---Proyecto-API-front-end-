const URL_API = 'http://localhost:5000/formularios';

document.getElementById('formularioContacto').addEventListener('submit', async (e) => {
    e.preventDefault();

    const datos = {
        nombre: document.getElementById('nombre').value,
        email: document.getElementById('email').value,
        asunto: document.getElementById('asunto').value,
        mensaje: document.getElementById('mensaje').value
    };

    try {
        const respuesta = await fetch(URL_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        if (respuesta.ok) {
            alert('¡Formulario enviado con éxito a PostgreSQL!');
            document.getElementById('formularioContacto').reset();
            cargarFormularios();
        } else {
            alert('Hubo un error al enviar el formulario.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('No se pudo conectar con el servidor.');
    }
});

async function cargarFormularios() {
    const lista = document.getElementById('listaMensajes');
    lista.innerHTML = '<p>Cargando mensajes...</p>';

    try {
        const respuesta = await fetch(URL_API);
        const formularios = await respuesta.json();

        lista.innerHTML = '';

        if(formularios.length === 0) {
            lista.innerHTML = '<p>No hay registros en la base de datos.</p>';
            return;
        }

        formularios.forEach(form => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h3> ${form.nombre} (${form.email})</h3>
                <p><strong>Asunto:</strong> ${form.asunto}</p>
                <p><strong>Mensaje:</strong> ${form.mensaje}</p>
                <small> ${new Date(form.fecha_creacion).toLocaleString()}</small>
            `;
            lista.appendChild(card);
        });
    } catch (error) {
        console.error('Error al cargar:', error);
        lista.innerHTML = '<p style="color: red;">Error al conectar con el servidor.</p>';
    }
}

document.getElementById('btnCargar').addEventListener('click', cargarFormularios);
window.onload = cargarFormularios;
