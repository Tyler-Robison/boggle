const resultPara = document.querySelector('#result-para')
const timerPara = document.querySelector('#timer-para')

class BoggleGame {
    constructor(secs = 30) {
        this.secs = secs
        this.total = 0
        this.words = []
        this.addListener()
        this.displayTimer()
    }

    //When this.click is run, it runs submitGuess with bound value of this
    addListener() {
        this.click = this.submitGuess.bind(this)
        $('#guess-button').on('click', this.click)
    }

    async submitGuess(e) {
        e.preventDefault()

        const guess = document.querySelector('#guess-form').value
        if (!guess) return;

        const response = await axios.get('/check-guess', { params: { word: guess } });
        const result = response.data.result

        document.querySelector('#guess-form').value = ''

        this.displayResult(result, guess)
    }

    displayResult(result, guess) {
        if (result === 'ok') {
            if (this.words.includes(guess)) {
                resultPara.innerText = 'You already Guessed that!'
            } else {
                resultPara.innerText = 'Valid Word'
                this.updateScore(guess)
                this.words.unshift(guess)
            }

        }
        else if (result === 'not-on-board') {
            resultPara.innerText = 'Board does not contain that word'
        }
        else if (result === 'not-word') {
            resultPara.innerText = 'Not a word'
        }
        // consider clearing this
    }

    updateScore(guess) {
        const score = guess.length;
        this.total += score;
        document.querySelector('#score-span').innerText = this.total
    }

    displayTimer() {
        let time = this.secs
        const id = setInterval(() => {
            if (time > 0) {
                time--;
                timerPara.innerText = time
            } else {
                this.gameEnd(id)
            }
        }, 1000);
    }

    async gameEnd(id) {
        clearInterval(id)
        timerPara.innerText = 'Time is up!'
        $('#guess-button').off()

        const res = await axios.post('/check-score', { score: this.total });
        console.log('response: ', res)
        if (res.data === 'highscore'){
            document.querySelector('#highscore-para').innerText = 'New Record!'
        } else {
            document.querySelector('#highscore-para').innerText = 'Not Record!'
        }


    }


}

let game = new BoggleGame();

