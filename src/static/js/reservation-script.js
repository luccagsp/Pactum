document.addEventListener("DOMContentLoaded", function () {
  const calendar = document.getElementById("calendar");
  const dateInput = document.getElementById("date");
  const horariosSelect = document.getElementById("time");

  // Mostrar fecha actual en el calendario inicialmente
  const today = new Date();
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  calendar.innerHTML = `<h3>${today.toLocaleDateString('es-ES', options)}</h3>`;

  // Función para deshabilitar ciertas fechas
  function disableDates(date) {
      const disabledDays = [0, 6]; // Deshabilitar fines de semana (Domingo=0, Sábado=6)
      const disabledSpecificDates = [
          '2024-10-15',
          '2024-12-25'
      ];

      const formattedDate = date.toISOString().split('T')[0];
      return disabledDays.includes(date.getDay()) || disabledSpecificDates.includes(formattedDate);
  }

  // Actualizar la visualización del calendario con la fecha y el horario seleccionados
  function updateCalendarDisplay() {
      const selectedDateArray = dateInput.value.split('-');
      const selectedDate = new Date(selectedDateArray[0], selectedDateArray[1] - 1, selectedDateArray[2]);
      const selectedTime = horariosSelect.value;

      if (disableDates(selectedDate)) {
          alert("La fecha seleccionada no está disponible. Por favor, elige otra.");
          dateInput.value = ''; // Limpiar la fecha seleccionada
          calendar.innerHTML = `<h3>${today.toLocaleDateString('es-ES', options)}</h3>`; // Mostrar la fecha actual si la selección es inválida
      } else {
          const selectedOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
          calendar.innerHTML = `
              <h3>${selectedDate.toLocaleDateString('es-ES', selectedOptions)}</h3>          `;
      }
  }

  // Escuchar cambios en la fecha
  dateInput.addEventListener("change", updateCalendarDisplay);

  // Escuchar cambios en el horario
  horariosSelect.addEventListener("change", updateCalendarDisplay);

  // Drag and Drop
  const dragDropArea = document.getElementById("drag-drop-area");
  const fileInput = document.getElementById("fileInput");

  dragDropArea.addEventListener("click", () => {
      fileInput.click();
  });

  dragDropArea.addEventListener("dragover", (e) => {
      e.preventDefault();
      dragDropArea.classList.add("dragging");
  });

  dragDropArea.addEventListener("dragleave", () => {
      dragDropArea.classList.remove("dragging");
  });

  dragDropArea.addEventListener("drop", (e) => {
      e.preventDefault();
      dragDropArea.classList.remove("dragging");
      const files = e.dataTransfer.files;
      handleFiles(files);
  });

  fileInput.addEventListener("change", (e) => {
      const files = e.target.files;
      handleFiles(files);
  });

  function handleFiles(files) {
      for (let i = 0; i < files.length; i++) {
          const file = files[i];
          const p = document.createElement("p");
          p.textContent = `Archivo subido: ${file.name}`;
          dragDropArea.appendChild(p);
      }
  }
});

