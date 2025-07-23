document.addEventListener("DOMContentLoaded", function() { //Evento que dispara quando o html for todo carregado
    const emojis = ['🍉','🎃','🏓','🏝️','☂️','🔥','🚀','🍕', '📚', '⚡'];
    const randomEmoji = document.getElementById('randomEmoji'); //Busca no html o id randomEmoji

    const randomNum = Math.floor(Math.random() * emojis.length); //Arredonda pra baixo um número aleatório entre 0 e 1 * a quantidade de emojis
    randomEmoji.textContent = emojis[randomNum]; //Define o conteudo do texto como o emoji na posição aleatória
    
    const data = new Date()
    const hoje = new Date().getDay(); //Pegamos o dia atual (0-6)
    const dayCards = document.querySelectorAll('.day-card'); //Selecionamos todos os elementos da classe day-card

    //Roda um for por todos os cards (para cada)
    dayCards.forEach((card, index)=> {
        const diff = hoje - index - 1; //Quantos dias tem de hoje para o dia do card
        const cardData = new Date(data); //Cópia da data de hoje
        cardData.setDate(data.getDate() - diff) //Define a data do card como essa diferença
        //Ex.
        //Hoje é sabado portanto hoje = 6, o laço vai rodar e o index do primerio card(segunda) vai ser 0, a diff vai
        //ser 6-0-1 = 5, o cardData então vai ser definido para o dia de hoje(19) - diff(5),logo, 
        //19-5 = 14, que é o dia de segunda

        const numDia = cardData.getDate() //Pega apenas o dia 

        card.querySelector('.day-num').textContent = numDia; //Atualiza o html

        //Se o número do card == ao dia de hoje(0-6), caso sim adiciona 'today' a classe
        if (index === (hoje - 1)) {
            card.classList.add('today');
        }
    });

    const cores_card_task = [
        '#ff6961', //Vermelho Pastel
        '#77dd77d3', //Verde Pastel
        '#fdfd96', //Amarelo Pastel
        '#84b6f4', //Azul Pastel
        '#fdcae1',  //Rosa Pastel
    ]

    function getCorRandom() {
        const index = Math.floor(Math.random() * cores_card_task.length);
        return cores_card_task[index];
    }

    document.querySelectorAll('.card-task').forEach(card => {
        var cor = getCorRandom();
        card.style.backgroundColor = cor;
    });

});


const popup = document.getElementById('popup');

//Ao clicar muda o style display para a div ser visível na página
document.querySelectorAll('.btnOpen').forEach(btn => {
    btn.addEventListener('click', () => {
        const idx = btn.dataset.index;
        document.getElementById('popup-idx1').value = idx;
        document.getElementById('popup-idx2').value = idx;

        popup.style.display = 'flex'
    });
});

//Volta ao display none(invisível)
btnClose.addEventListener('click', () => {
    popup.style.display = 'none';
  });