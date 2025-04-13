document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_symptoms')
        .then(res => res.json())
        .then(symptoms => {
            const container = document.getElementById('symptoms-list');
            symptoms.forEach(symptom => {
                const div = document.createElement('div');
                div.innerHTML = `
                    <input type="checkbox" id="${symptom}">
                    <label for="${symptom}">${symptom}</label>
                `;
                container.appendChild(div);
            });
        });
});

function analyze() {
    const symptoms = {};
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        symptoms[checkbox.id] = checkbox.checked ? 1 : 0;
    });

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(symptoms)
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('results').style.display = 'block';
        document.getElementById('disease').textContent = `Possible Condition: ${data.disease}`;
        document.getElementById('doctor').textContent = `See: ${data.doctor}`;
        document.getElementById('diet').textContent = `Eat: ${data.diet}`;
        document.getElementById('confidence').value = data.confidence;
        document.getElementById('confidence-value').textContent = `${data.confidence}%`;
    });
}