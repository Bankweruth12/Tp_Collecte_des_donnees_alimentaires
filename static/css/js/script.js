// Attendre que la page soit complètement chargée
document.addEventListener('DOMContentLoaded', function() {

    // --- 1. AFFICHER LA VALEUR DU CURSEUR (Faim et Satisfaction) ---
    // Quand on bouge le curseur, ça affiche le chiffre en temps réel
    const rangeInputs = document.querySelectorAll('input[type="range"]');
    
    rangeInputs.forEach(input => {
        input.addEventListener('input', function() {
            // On cherche le label associé pour y ajouter la valeur
            const label = this.previousElementSibling;
            // On remplace l'ancienne valeur par la nouvelle
            const labelText = label.textContent.split(':')[0];
            label.innerHTML = labelText + ` : <strong>${this.value} / 5</strong>`;
        });
    });

    // --- 2. VERIFICATION QUE TOUT EST REMPLI ---
    const formulaire = document.querySelector('form');
    
    formulaire.addEventListener('submit', function(e) {
        const date = document.querySelector('input[name="date"]').value;
        const heure = document.querySelector('input[name="heure"]').value;
        const aliments = document.querySelector('textarea[name="aliments"]').value;

        if(date === "" || heure === "" || aliments === "") {
            alert("⚠️ Veuillez remplir tous les champs obligatoires !");
            e.preventDefault(); // Bloque l'envoi du formulaire
        } else {
            // Message de confirmation optionnel
            const confirmation = confirm("✅ Es-tu sûr de vouloir envoyer ces informations ?");
            if(!confirmation){
                e.preventDefault();
            }
        }
    });

    // --- 3. DISPARITION AUTOMATIQUE DU MESSAGE DE SUCCES ---
    const messageBox = document.querySelector('.alert');
    if(messageBox) {
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 4000); // Disparaît après 4 secondes
    }

    console.log("📝 Script Alimentation chargé !");
});