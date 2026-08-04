// Database / JSON එකෙන් Data ගන්න Function එක
async function fetchLotteryResults() {
    try {
        const response = await fetch('results.json');
        const data = await response.json();
        
        const container = document.getElementById('results-container');
        container.innerHTML = ''; // පැරණි Data අයින් කිරීම

        data.forEach(item => {
            const card = document.createElement('div');
            card.className = `result-card ${item.type} bg-gradient-to-br ${item.bgGradient} text-white p-5 rounded-2xl shadow-lg border border-white/10`;
            
            // Numbers HTML
            let numbersHtml = `<div class="w-10 h-10 sm:w-11 sm:h-11 bg-amber-400 text-slate-900 font-bold flex items-center justify-center rounded-full text-lg shadow-md ring-2 ring-amber-300/50">${item.letter}</div>`;
            
            item.numbers.forEach(num => {
                numbersHtml += `<div class="w-10 h-10 sm:w-11 sm:h-11 bg-white text-slate-900 font-bold flex items-center justify-center rounded-full text-base shadow-md">${num}</div>`;
            });

            card.innerHTML = `
                <div class="flex justify-between items-center mb-4">
                    <div>
                        <h3 class="text-xl font-bold">${item.name}</h3>
                        <p class="text-xs opacity-80 mt-0.5">${item.board}</p>
                    </div>
                    <span class="bg-white/10 backdrop-blur-md text-xs px-3 py-1.5 rounded-lg border border-white/10 font-mono">Draw: #${item.drawNo}</span>
                </div>
                <div class="flex items-center space-x-2 sm:space-x-3">
                    ${numbersHtml}
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Data load කිරීමට නොහැකි විය:", error);
    }
}

// Page එක Load වෙද්දී Data Fetch කිරීම
document.addEventListener('DOMContentLoaded', fetchLotteryResults);