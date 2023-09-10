class BoggleGame {


    constructor(boardId, secs=60) {
        this.secs = secs; // game duration: 1 min; 60 secs
        this.showTimer(); // create timer

        this.score = 0; // set score to 0
        this.words=  new Set(); // new set of words
        this.board = $("#" + boardId); // create board_Id

        // the timer ticks every 1000ms
        this.timer = setInterval(this.tick.bind(this), 1000);

        // add .add-word class to this.board object using handleSubmit on 'this' object
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    // display word in list of words

    showWord(word) {
        $(".words", this.board).append($("<li>", { text: word }));
    }    

    // show core in html
    showScore() {
        $(".score", this.board).text(this.score);
    }

    // display status message 
    showMessage(msg, cls) {
        $(".msg", this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }

    // handle submission of word: if unique & valid, score & show.
    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $(".word", this.board);
        
        let word = $word.val();
        // if word is not found in dictionary: return undefined
        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`Already found ${word}`, "err");
            return;
        }

        // check server validity
        const resp = await axios.get("/check-word", { params: { word: word }});
        if (resp.data.result === "not-word") {
          this.showMessage(`${word} is not a valid English word`, "err");
        } else if (resp.data.result === "not-on-board") {
          this.showMessage(`${word} is not a valid word on this board`, "err");
        } else {
          this.showWord(word);
          this.score += word.length;
          this.showScore();
          this.words.add(word);
          this.showMessage(`Added: ${word}`, "ok");
        }

        $word.val("").focus();
    }

    // update DOM timer

    showTimer() {
        $(".timer", this.board).text(this.secs);
    }

    async tick() {
        this.secs -= 1;
        this.showTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    async scoreGame() {
        $(".add-word", this.board).hide();

        const resp = await axios.post("/post-score", {score: this.score});
        if (resp.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final score: ${this.score}`, "ok");
        }
    }
}